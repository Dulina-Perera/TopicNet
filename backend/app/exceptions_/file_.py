# %%
class InvalidFileFormatError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class NoFileSubmittedError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)
