# %%
import re
import os

from botocore.exceptions import ClientError
from fastapi import UploadFile
from typing import Any, Tuple, Union

from ....exceptions import NoSuchS3BucketError, NoSuchS3FileError

# %%
def is_file_not_none(file: Union[UploadFile, None]) -> bool:
  if file is None:
    return False

  return True


def is_file_format_allowed(
  file: UploadFile,
	allowed_file_formats: Tuple[str, ...]
) -> bool:
	if file.content_type not in allowed_file_formats:
		return False

	return True


def is_s3_uri_valid(s3_uri: Union[str, None]) -> bool:
	if s3_uri is None:
		return False
	elif not re.match(r"s3://\w+/\w+", s3_uri):
		return False

	return True


def does_s3_bucket_exist(
  bucket_name: str,
  s3_client: Any
) -> bool:
  try:
    s3_client.head_bucket(Bucket=bucket_name)
    return True
  except ClientError as e:
    if e.response["Error"]["Code"] in ["403", "404"]:
      raise NoSuchS3BucketError(f"Bucket '{bucket_name}' does not exist or you do not have access to it.")
    else:
      raise Exception(f"An unknown error occurred while verifying the existence of bucket '{bucket_name}'.")


def does_s3_file_exist(
  s3_uri: str,
  s3_client: Any
) -> bool:
  match = re.match(r"s3://([^/]+)/(.+)", s3_uri)
  bucket_name: str = match.group(1)
  object_name: str = match.group(2)

  try:
    s3_client.head_object(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Key=object_name)
    return True
  except ClientError as e:
    if e.response['Error']['Code'] == "404":
      raise NoSuchS3FileError(f"File '{object_name}' does not exist in bucket '{bucket_name}' or you do not have access to it.")
    else:
      raise Exception(f"An unknown error occurred while verifying the existence of file '{object_name}' in bucket '{bucket_name}'.")

