# %%
# Import the required libraries, modules, classes, and functions.
import os

from openai import AsyncOpenAI
from openai.pagination import SyncPage
from openai.types import Model
from typing import List

from .config import are_env_vars_set
from ..exceptions import EnvVarNotSetError

# %%
async def is_valid_openai_model(model: str) -> bool:
  """
	Check if the specified OpenAI model is valid.

	:param model: The OpenAI model to check
	:type model: str

	:returns: True if the model is valid, False otherwise
	:rtype: bool
	"""
  # Check if the `OPENAI_API_KEY` environment variable is set.
  if not are_env_vars_set("OPENAI_API_KEY"):
    raise EnvVarNotSetError("The OPENAI_API_KEY environment variable is not set.")

  # Initialize the OpenAI client.
  client: AsyncOpenAI = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  # Get the list of available models.
  response: SyncPage[Model] = await client.models.list()
  models: List[str] = [model.id for model in response.data]

  # Check if the specified model is valid.
  return model in models
