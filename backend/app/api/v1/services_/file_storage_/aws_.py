# %%
# Import the required libraries, modules, classes, and functions.
import os

from fastapi import UploadFile
from typing import Any, Optional

from ..verification_and_validation_ import does_s3_bucket_exist
from .....exceptions_ import S3DownloadError, S3UploadError

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


async def download_file_from_s3_(
	s3_uri_: str,
	s3_client_: Any
) -> bytes:
	"""
	Download a file from an S3 bucket.

	:param s3_uri_: The S3 URI of the file to download
	:type s3_uri_: str

	:param s3_client_: The S3 client to use
	:type s3_client_: Any

	:return: The file's content
	:rtype: bytes

	:raises S3DownloadError: An error occurred while downloading the file from S3
	"""
	try:
		# Extract the bucket name and object name from the S3 URI.
		bucket_name_: str; object_name_: str
		bucket_name_, object_name_ = s3_uri_.replace("s3://", "").split("/", 1)

		# Download the file from S3.
		file_path_: str = f"/tmp/{object_name_}"
		with open(file_path_, "wb") as f:
			await s3_client_.download_fileobj(bucket_name_, object_name_, f)

		# Return the file path.
		return file_path_
	except Exception as e:
		raise S3DownloadError() from e
