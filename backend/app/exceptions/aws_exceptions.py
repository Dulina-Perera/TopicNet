# %%
class InvalidS3URIError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class NoSuchS3BucketError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class NoSuchS3FileError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class S3UploadError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class UndefinedAWSEnvironmentVariableError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)
