# %%
from fastapi import APIRouter, File, HTTPException, UploadFile
from secrets import token_urlsafe
from typing import Union

from ..services import (
  AWSEnvironmentVariableNotSetError,
  InvalidFileFormatError,
  NoSubmittedFileError,
  NoSuchBucketError,
  S3UploadError,
  upload_pdf_to_s3,
  verify_file_format
)

# %%
generate_router: APIRouter = APIRouter()

# %%
@generate_router.post("/base")
async def endpoint_generate_base(file: Union[UploadFile, None] = File(default=None)):
  try:
    # Verify that a file was submitted and that it is a PDF file.
    verify_file_format(
      file,
      "application/pdf"
    )

    # Upload the file to S3.
    file_uri: str = upload_pdf_to_s3(
			file,
			token_urlsafe(16),
			"topicnet"
		)

    return {"message": f"File uploaded to {file_uri}"}
  except (
		AWSEnvironmentVariableNotSetError,
		NoSuchBucketError,
		S3UploadError
	) as e:
    raise HTTPException(status_code=500, detail=str(e))
  except NoSubmittedFileError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except InvalidFileFormatError as e:
    raise HTTPException(status_code=415, detail=str(e))
