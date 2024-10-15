# %%
import os

from fastapi import UploadFile
from typing import Any

from .v_and_v import does_s3_bucket_exist
from ....exceptions import S3UploadError

# %%
def upload_file_to_s3(
  file: UploadFile,
  object_name: str,
  s3_client: Any
) -> str:
  try:
		# If no custom object name is provided, use the file"s name.
    if object_name is None:
      object_name = file.filename

    # Check if the S3 bucket exists and is accessible.
    does_s3_bucket_exist(os.getenv("AWS_S3_BUCKET_NAME"), s3_client)

    # Upload the file to S3 using the file"s file-like object.
    s3_client.upload_fileobj(file.file, os.getenv("AWS_S3_BUCKET_NAME"), object_name)

    # Return the S3 URI of the uploaded file.
    return f"s3://{os.getenv('AWS_S3_BUCKET_NAME')}/{object_name}"
  except Exception as e:
    raise S3UploadError("An error occurred while uploading the file to S3.") from e
