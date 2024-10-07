# %%
class AWSEnvironmentVariableNotSetError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class InvalidFileFormatError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class NoSubmittedFileError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class NoSuchBucketError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class S3UploadError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)
