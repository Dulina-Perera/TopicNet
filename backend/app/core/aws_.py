# %%
# Import the required libraries, modules, classes, and functions.
import os

from boto3 import client
from fastapi import Depends
from typing import Annotated, Any

from .config_ import are_env_vars_set
from ..exceptions import EnvVarsNotSetError

# %%
def get_aws_s3_client() -> Any:
	"""
	Get an AWS S3 client.

	:param None

	:return: The AWS S3 client
	:rtype: Any
	"""
	# Check if the required environment variables are set.
	if not are_env_vars_set("AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
		raise EnvVarsNotSetError()

	# Initialize an S3 client with credentials and region.
	return client(
		service_name="s3",
		region_name=os.getenv("AWS_REGION"),
		aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
		aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
	)

# %%
# AWS S3 client dependency
s3_client_dep: Annotated = Annotated[client, Depends(get_aws_s3_client)]
