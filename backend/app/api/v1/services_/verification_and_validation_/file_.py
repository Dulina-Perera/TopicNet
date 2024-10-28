# %%
from fastapi import UploadFile
from typing import Optional, Tuple

# %%
def is_file_not_none(file: Optional[UploadFile]) -> bool:
  """
	Check if a file was submitted.

	:param file: The file to check
	:type file: Optional[UploadFile]

	:return: True if the file is not None, False otherwise
	:rtype: bool
 	"""
  if file is None:
    return False

  return True


def is_file_format_allowed(
  file: UploadFile,
	allowed_file_formats: Tuple[str, ...]
) -> bool:
  """
	Check if the file format is allowed.

	:param file: The file to check
	:type file: UploadFile
	:param allowed_file_formats: The allowed file formats
	:type allowed_file_formats: Tuple[str, ...]

	:return: True if the file format is allowed, False otherwise
	:rtype: bool
	"""
  if file.content_type not in allowed_file_formats:
    return False

  return True
