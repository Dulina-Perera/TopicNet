# %%
# Import the necessary modules.
from fastapi import APIRouter, File, HTTPException, UploadFile
from secrets import token_urlsafe
from typing import Union

from ..services import (
  AWSEnvironmentVariableNotSetError,
  InvalidFileFormatError,
  InvalidURIError,
  NoSubmittedFileError,
  NoSuchS3BucketError,
  NoSuchS3FileError,
  S3UploadError,
  store_s3_file_uri,
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

    # Upload the file to S3 and store the file URI in the database.
    file_uri: str = upload_pdf_to_s3(
			file,
			token_urlsafe(16),
			"topicnet"
		)
    if store_s3_file_uri(file_uri):
      return {
				"message": "The file was successfully uploaded to S3 and the file URI was stored in the database."
			}
    else:
      return {
				"message": "The file was successfully uploaded to S3, but an error occurred while storing the file URI in the database."
			}
  except (
		AWSEnvironmentVariableNotSetError,
  	InvalidURIError,
		NoSuchS3BucketError,
		NoSuchS3FileError,
		S3UploadError
	) as e:
    raise HTTPException(status_code=500, detail=str(e))
  except NoSubmittedFileError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except InvalidFileFormatError as e:
    raise HTTPException(status_code=415, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
