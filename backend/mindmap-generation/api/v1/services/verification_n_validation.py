# %%
import boto3
import re
import os

from botocore.exceptions import ClientError
from fastapi import UploadFile
from typing import Union

from .exceptions import (
  AWSEnvironmentVariableNotSetError,
  InvalidFileFormatError,
  NoSubmittedFileError,
  NoSuchS3BucketError,
  NoSuchS3FileError
)

# %%
def verify_file_format(
  file: Union[UploadFile, None],
  file_format: str
) -> bool:
  if file is None:
    raise NoSubmittedFileError("No file was submitted.")

  if file.content_type != file_format:
    raise InvalidFileFormatError("Invalid file format. Only PDF files are supported.")

  return True


def does_s3_bucket_exist(bucket_name: str) -> bool:
  try:
    if not all([
			os.getenv("AWS_REGION"),
			os.getenv("AWS_ACCESS_KEY_ID"),
			os.getenv("AWS_SECRET_ACCESS_KEY")
		]):
      raise AWSEnvironmentVariableNotSetError("AWS environment variables are not set.")

    s3_client: boto3.client = boto3.client(
			service_name="s3",
			region_name=os.getenv("AWS_REGION"),
			aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
			aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
		)

    s3_client.head_bucket(Bucket=bucket_name)
    return True
  except AWSEnvironmentVariableNotSetError as e:
    raise
  except ClientError as e:
    if e.response['Error']['Code'] in ["403", "404"]:
      raise NoSuchS3BucketError(f"Bucket '{bucket_name}' does not exist or you do not have access to it.")
    else:
      raise Exception(f"An unknown error occurred while verifying the existence of bucket '{bucket_name}'.")


def does_s3_file_exist(
  file_uri: Union[str, None],
  bucket_name: str
) -> bool:
  if file_uri is None:
    return False
  else:
    try:
      if not all([
				os.getenv("AWS_REGION"),
				os.getenv("AWS_ACCESS_KEY_ID"),
				os.getenv("AWS_SECRET_ACCESS_KEY")
			]):
        raise AWSEnvironmentVariableNotSetError("AWS environment variables are not set.")

      s3_client: boto3.client = boto3.client(
				service_name='s3',
				region_name=os.getenv('AWS_REGION'),
				aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
				aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
			)

      s3_client.head_object(Bucket=bucket_name, Key=re.sub(r"https://\w+\.s3\.\w+-\w+-\d+\.amazonaws\.com/", "", file_uri))
      return True
    except AWSEnvironmentVariableNotSetError as e:
      raise
    except ClientError as e:
      if e.response['Error']['Code'] == "404":
        raise NoSuchS3FileError(f"File '{file_uri}' does not exist in bucket '{os.getenv('S3_BUCKET')}' or you do not have access to it.")
      else:
        raise Exception(f"An unknown error occurred while verifying the existence of file '{file_uri}' in bucket '{bucket}'.")
