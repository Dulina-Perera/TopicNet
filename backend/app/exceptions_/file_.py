# %%
from typing import Tuple

# %%
class InvalidFileFormatError(Exception):
  def __init__(self, allowed_file_formats: Tuple[str, ...]) -> None:
    self.allowed_file_formats: Tuple[str, ...] = allowed_file_formats
    super().__init__(f"Invalid file format. Only {', '.join(self.allowed_file_formats)} files are supported.")

class NoFileSubmittedError(Exception):
  def __init__(self) -> None:
    super().__init__("No file was submitted.")
