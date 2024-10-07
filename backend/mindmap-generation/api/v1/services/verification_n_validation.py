# %%
import boto3
import os

from botocore.exceptions import ClientError
from fastapi import File, UploadFile
from typing import Dict, Union

from .exceptions import AWSEnvironmentVariableNotSetError, InvalidFileFormatError, NoSubmittedFileError

# %%
def verify_file_format(
  file: Union[UploadFile, None],
  file_format: str
) -> bool:
  if file is None:
    raise NoSubmittedFileError('No file was submitted.')

  if file.content_type != file_format:
    raise InvalidFileFormatError('Invalid file format. Only PDF files are supported.')

  return True

# %%
def validate_bucket_head(bucket_name: str) -> Dict[str, Union[bool, str]]:
  try:
    error_values: Dict[str, bool] = {
			"400": True,
			"403": True,
			"404": False
		}

    result: Dict[str, Union[bool, str]] = {
			"bucketName": bucket_name,
			"bucketUri": f"http://{bucket_name}.s3.amazonaws.com",
			"arn": f"arn:aws:s3:::{bucket_name}",
			'exists': False
		}

    if not all([
			os.getenv('AWS_REGION'),
			os.getenv('AWS_ACCESS_KEY_ID'),
			os.getenv('AWS_SECRET_ACCESS_KEY')
		]):
      raise AWSEnvironmentVariableNotSetError('AWS environment variables are not set.')

    s3_client: boto3.client = boto3.client(
			service_name='s3',
			region_name=os.getenv('AWS_REGION'),
			aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
		)

    s3_client.head_bucket(Bucket=bucket_name)
    result['exists'] = True
    return result
  except AWSEnvironmentVariableNotSetError as e:
    raise
  except ClientError as e:
    result['exists'] = error_values[e.response['Error']['Code']]
    return result
