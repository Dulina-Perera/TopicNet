# %%
# Import the required libraries, modules, classes, and functions.
import os

from aioboto3 import Session
from fastapi import Depends
from typing import Annotated, Any, AsyncGenerator

from .config_ import is_env_var_set
from ..exceptions_ import EnvVarNotSetError

# %%
async def get_aws_s3_client() -> AsyncGenerator:
  """
  Get an AWS S3 client within an async context manager.

  :return: The AWS S3 client.
  :rtype: AsyncGenerator
  """
  # Verify required environment variables.
  for env_var in ("AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
    if not is_env_var_set(env_var):
      raise EnvVarNotSetError(env_var)

  # Initialize the session and create an S3 client in async context.
  session = Session()
  async with session.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  ) as s3_client:
    yield s3_client

# %%
# AWS S3 client dependency
s3_client_dep: Annotated = Annotated[Any, Depends(get_aws_s3_client)]
