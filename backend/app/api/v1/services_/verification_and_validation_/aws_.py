# %%
import re
import os

from botocore.exceptions import ClientError
from re import Match
from typing import Any, Optional

from .....exceptions_ import AWSError, NoSuchS3BucketError, NoSuchS3FileError

# %%
def is_s3_uri_valid(s3_uri: Optional[str]) -> bool:
  """
	Check if an S3 URI is valid.

	:param s3_uri: The S3 URI to validate
	:type s3_uri: Optional[str]

	:return: True if the S3 URI is valid; False otherwise
	:rtype: bool
  """
  if s3_uri is None:
    return False
  elif not re.match(r"s3://[a-zA-Z0-9.\-_]+(/[a-zA-Z0-9.\-_]+)*", s3_uri):
    return False

  return True


async def does_s3_bucket_exist(
  bucket_name: str,
  s3_client: Any
) -> bool:
  """
	Check if an S3 bucket exists.

	:param bucket_name: The name of the S3 bucket to check
	:type bucket_name: str

	:param s3_client: The AWS S3 client to use
	:type s3_client: Any

	:return: True if the S3 bucket exists; False otherwise
	:rtype: bool

	:raises NoSuchS3BucketError: If the S3 bucket does not exist or the user does not have access to it
	:raises AWSError: If an unknown error occurs while verifying the existence of the S3 bucket
	"""
  try:
    await s3_client.head_bucket(Bucket=bucket_name)
    return True
  except ClientError as e:
    if e.response["Error"]["Code"] in ["403", "404"]:
      raise NoSuchS3BucketError(f"Bucket '{bucket_name}' does not exist or you do not have access to it.")
    else:
      raise AWSError(f"An unknown error occurred while verifying the existence of bucket '{bucket_name}'.")


async def does_s3_object_exist(
  s3_uri: str,
  s3_client: Any
) -> bool:
  """
	Check if an S3 file exists.

	:param s3_uri: The S3 URI of the file to check
	:type s3_uri: str

	:param s3_client: The AWS S3 client to use
	:type s3_client: Any

	:return: True if the S3 file exists; False otherwise
	:rtype: bool

	:raises NoSuchS3FileError: If the S3 file does not exist or the user does not have access to it
	:raises AWSError: If an unknown error occurs while verifying the existence of the S3 file
	"""
  match: Match = re.match(r"s3://([^/]+)/(.+)", s3_uri)
  bucket_name: str = match.group(1)
  object_name: str = match.group(2)

  try:
    await s3_client.head_object(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Key=object_name)
    return True
  except ClientError as e:
    if e.response['Error']['Code'] == ["403", "404"]:
      raise NoSuchS3FileError(object_name, bucket_name)
    else:
      raise AWSError(f"An unknown error occurred while verifying the existence of file '{object_name}' in bucket '{bucket_name}'.")
