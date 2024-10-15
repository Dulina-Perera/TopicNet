# %%
import os

from boto3 import client
from fastapi import Depends
from typing import Annotated, Any

from .config_ import are_env_vars_set
from ..exceptions import UndefinedAWSEnvironmentVariableError

# %%
def get_s3_client() -> Any:
	"""
	Get an S3 client with the specified configuration.

	This function gets an S3 client with the specified configuration.

	Parameters:
		None

	Returns:
		Any: The S3 client
	"""
	if not are_env_vars_set("AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
		raise UndefinedAWSEnvironmentVariableError("AWS environment variables are not set.")

	# Initialize an S3 client with credentials and region.
	return client(
		service_name="s3",
		region_name=os.getenv("AWS_REGION"),
		aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
		aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
	)

# %%
# S3 client dependency
s3_client_dep = Annotated[client, Depends(get_s3_client)]
