# %%
# Import the required libraries, modules, classes and functions.
from fastapi import APIRouter, Depends, File, Request, Response, UploadFile
from logging import Logger
from pydantic import BaseModel
from secrets import token_urlsafe
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from typing import Any, Optional, Tuple

from ..services_ import is_file_format_allowed, is_file_not_none, upload_file_to_s3
from ....core_ import create_document_, get_aws_s3_client, get_db_session, get_logger, read_user_id_by_session_id_
from ....exceptions_ import InvalidFileFormatError, NoFileSubmittedError

# %%
upload_router_: APIRouter = APIRouter()

# %%
class DocumentResponse(BaseModel):
	id: int
	user_id: str
	name: str
	type: str
	path: str

	class Config:
		from_attributes: bool = True
		orm_mode: bool = True

# %%
@upload_router_.post("/")
async def upload_file_(
  request_: Request,
  file_: Optional[UploadFile] = File(default=None),
	db_session_: async_scoped_session[AsyncSession] = Depends(get_db_session),
	s3_client_: Any = Depends(get_aws_s3_client),
	logger_: Logger = Depends(get_logger)
):
  # ################################################################################################
  # Extract the `session_id` from the request cookies.
  session_id_: str = request_.cookies.get("auth_session")

  # Read the `user_id` from the database using the `session_id`.
  user_id_: int = await read_user_id_by_session_id_(db_session_, session_id_)

  # ################################################################################################
  # Check if a file was submitted.
  if not is_file_not_none(file_):
    raise NoFileSubmittedError()

  # Check if the file format is allowed.
  ALLOWED_FILE_FORMATS_: Tuple[str, ...] = ("application/pdf",)
  if not is_file_format_allowed(file_, ALLOWED_FILE_FORMATS_):
    raise InvalidFileFormatError(ALLOWED_FILE_FORMATS_)

  logger_.info(f"Received {file_.filename} with content type {file_.content_type} and size {file_.size} bytes.")

  # ################################################################################################
  # Extract the file name and file's content type.
  file_name_: str = file_.filename
  content_type_: str = file_.content_type

  # Save the file to S3 and retrieve the S3 URI.
  path_: str = await upload_file_to_s3(file_, token_urlsafe(16), s3_client_)

  logger_.info(f"Uploaded the file to S3 with URI {path_}.")

  # # ################################################################################################
  # # Insert the document metadata into the database.
  document_: Any = await create_document_(db_session_, user_id_, file_name_, content_type_, path_)

  logger_.info(f"Inserted the document metadata into the database with ID {document_.id}.")

  # Create a response object.
  response_: DocumentResponse = DocumentResponse.model_validate(document_)

  # Return the response object.
  return Response(
    status_code=201,
    content=response_.model_dump_json(),
    media_type="application/json"
  )
