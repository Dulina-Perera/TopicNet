# %%
import boto3
import os

from fastapi import UploadFile
from typing import Dict, Union

from .exceptions import AWSEnvironmentVariableNotSetError, InvalidFileFormatError, NoSubmittedFileError, NoSuchS3BucketError, S3UploadError
from .verification_n_validation import does_s3_bucket_exist, verify_file_format

# %%
def upload_pdf_to_s3(
  file: Union[UploadFile, None],
  object_name: str,
  bucket_name: str
) -> str:
  try:
		# Verify that a file was submitted and that it is a PDF file.
    verify_file_format(
			file,
			'application/pdf'
		)

    # If no custom object name is provided, use the file's name.
    if object_name is None:
      object_name = file.filename

    # Make sure that the AWS environment variables are set.
    if not all([
			os.getenv('AWS_REGION'),
			os.getenv('AWS_ACCESS_KEY_ID'),
			os.getenv('AWS_SECRET_ACCESS_KEY')
		]):
      raise AWSEnvironmentVariableNotSetError('AWS environment variables are not set.')

    # Initialize the S3 client with credentials and region.
    s3_client: boto3.client = boto3.client(
			service_name='s3',
			region_name=os.getenv('AWS_REGION'),
			aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
		)

    # Make sure that the bucket exists and that the user has access to it.
    does_s3_bucket_exist(bucket_name)

    # Upload the file to S3 using the file's file-like object.
    s3_client.upload_fileobj(file.file, bucket_name, object_name)

    # Return the S3 URL of the uploaded file.
    return f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{object_name}"
  except (
    AWSEnvironmentVariableNotSetError,
    InvalidFileFormatError,
    NoSubmittedFileError,
    NoSuchS3BucketError
  ) as e:
    raise
  except Exception as e:
    raise S3UploadError('An error occurred while uploading the file to S3.') from e
