# %%
class AWSError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class InvalidS3URIError(AWSError):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class NoSuchS3BucketError(AWSError):
  def __init__(self, bucket_name: str) -> None:
    super().__init__(f"Bucket '{bucket_name}' does not exist or you do not have access to it.")

class NoSuchS3FileError(AWSError):
	def __init__(self, object_name: str, bucket_name: str) -> None:
		super().__init__(f"File '{object_name}' does not exist in bucket '{bucket_name}' or you do not have access to it.")

class S3UploadError(AWSError):
	def __init__(self) -> None:
		super().__init__("An error occurred while uploading the file to S3.")

class UndefinedAWSEnvironmentVariableError(AWSError):
  def __init__(self, message: str) -> None:
    super().__init__(message)
