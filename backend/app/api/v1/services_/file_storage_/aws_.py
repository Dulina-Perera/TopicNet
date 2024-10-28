# %%
# Import the required libraries, modules, classes, and functions.
import os

from fastapi import UploadFile
from typing import Any, Optional

from ..verification_and_validation_ import does_s3_bucket_exist
from .....exceptions_ import S3UploadError

# %%
async def upload_file_to_s3(
  file: UploadFile,
  object_name: Optional[str],
  s3_client: Any
) -> str:
  """
  Upload a file to an S3 bucket.

  :param file: The file to upload
  :type file: UploadFile

  :param object_name: The name of the object in the S3 bucket
  :type object_name: Optional[str]

  :param s3_client: The S3 client to use
  :type s3_client: Any

  :return: The S3 URI of the uploaded file
  :rtype: str

  :raises S3UploadError: An error occurred while uploading the file to S3
	"""
  try:
    # If no custom object name is provided, use the file's name.
    if object_name is None:
      object_name = file.filename

    # Check if the S3 bucket exists and is accessible.
    await does_s3_bucket_exist(os.getenv("AWS_S3_BUCKET_NAME"), s3_client)

    # Upload the file to S3 using the file's file-like object.
    await s3_client.upload_fileobj(file.file, os.getenv("AWS_S3_BUCKET_NAME"), object_name)

    # Return the S3 URI of the uploaded file.
    return f"s3://{os.getenv('AWS_S3_BUCKET_NAME')}/{object_name}"
  except Exception as e:
    raise S3UploadError() from e

