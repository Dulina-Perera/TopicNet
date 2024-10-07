# %%
class AWSEnvironmentVariableNotSetError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class InvalidFileFormatError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class InvalidURIError(Exception):
	def __init__(self, message: str) -> None:
		super().__init__(message)

class NoSubmittedFileError(Exception):
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
