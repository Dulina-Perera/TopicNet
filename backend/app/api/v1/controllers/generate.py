# %%
# Import the required modules.
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from logging import Logger
from secrets import token_urlsafe
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from typing import Any, Dict, Union, Tuple

from ..services import (
  is_file_format_allowed,
  is_file_not_none,
  save_s3_uri,
  upload_file_to_s3
)
from ....core import get_db_session, get_logger, get_s3_client
from ....exceptions import (
	InvalidFileFormatError,
	NoFileSubmittedError
)

# %%
# Router for the generate endpoint
generate_router: APIRouter = APIRouter()

# %%
@generate_router.post("/base")
async def generate_base(
  file: Union[UploadFile, None] = File(default=None),
	db_session: scoped_session[Session] = Depends(get_db_session),
  s3_client: Any = Depends(get_s3_client),
  logger: Logger = Depends(get_logger)
) -> Dict:
  try:
    # Check if a file was submitted.
    if not is_file_not_none(file):
      raise NoFileSubmittedError("No file was submitted.")

    # Check if the file format is allowed.
    ALLOWED_FILE_FORMATS: Tuple[str, ...] = ("application/pdf",)
    if not is_file_format_allowed(file, ALLOWED_FILE_FORMATS):
      raise InvalidFileFormatError(f"Invalid file format. Only {', '.join(ALLOWED_FILE_FORMATS)} files are supported.")

    # Upload the file to S3 and store the file's S3 URI in the database.
    s3_uri: str = upload_file_to_s3(file, token_urlsafe(16), s3_client)
    if save_s3_uri(
      s3_uri,
      db_session,
      s3_client,
    ):
      return {
				"message": "The file was successfully uploaded to S3 and the file URI was stored in the database."
			}
    else:
      return {
				"message": "The file was successfully uploaded to S3, but an error occurred while storing the file URI in the database."
			}
  except NoFileSubmittedError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except InvalidFileFormatError as e:
    raise HTTPException(status_code=415, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
