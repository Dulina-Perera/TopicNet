# %%
# Import the required libraries, modules, classes, and functions.
import logging

from fastapi import Depends
from logging import Logger
from typing import Annotated

# %%
def get_logger(name: str = "app") -> Logger:
  """
  Get a logger with the specified name.

	:param name: The name of the logger
	:type name: str

	:return: The logger
	:rtype: Logger
  """
  return logging.getLogger(name)

# %%
# Logger dependency
logger_dep: Annotated = Annotated[logging.Logger, Depends(get_logger)]
