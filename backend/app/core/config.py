# %%
# Import the required modules.
import os
import yaml

from dotenv import load_dotenv
from typing import Dict, Union

# %%
def are_env_vars_set(*env_vars: str) -> bool:
  """
  Check if the specified environment variables are set.

	This function checks if the specified environment variables are set.

	Parameters:
		*env_vars (str): The environment variables to check.

	Returns:
		bool: True if all the environment variables are set, False otherwise
  """
  return all([os.getenv(env_var) for env_var in env_vars])


def load_env_vars() -> None:
	"""
	Load the environment variables from .env files.

	This function loads the environment variables from .env files located in the config directory at the root of the project.

	Parameters:
		None

	Returns:
		None
	"""
	env_dir: str = os.path.join(os.path.dirname(__file__), "../../config")  # The directory containing the .env files

  # Load environment variables from the .env files.
	for file in os.listdir(env_dir):
		if file.endswith(".env"):
			load_dotenv(os.path.join(env_dir, file))


def load_db_config() -> Dict[str, Union[int, str]]:
	"""
	Load the database configuration from the YAML file.

	This function loads the database configuration from the db_config.yaml file located in the config directory at the root of the project.

	Parameters:
		None

	Returns:
		dict: The database configuration
	"""
	with open(os.path.join(os.path.dirname(__file__), "../../config/db_config.yaml"), "r") as f:
		db_config: Dict[str, Union[int, str]] = yaml.safe_load(f.read())

	return db_config
