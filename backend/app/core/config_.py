# %%
# Import the required libraries, modules, classes, and functions.
import os
import yaml

from dotenv import load_dotenv
from typing import Dict, Tuple, Union

# %%
CONFIG_DIR: str = os.path.join(os.path.dirname(__file__), "../../config")  # The directory containing the configuration files

# %%
def are_env_vars_set(*env_vars: Tuple[str]) -> bool:
  """
  Check if the specified environment variables are set.

	:param env_vars: The environment variables to check
	:type env_vars: Tuple[str]

	:return: True if all the environment variables are set, False otherwise
	:rtype: bool
  """
  return all([os.getenv(env_var) for env_var in env_vars])


def load_env_vars() -> None:
	"""
	Load the environment variables from .env files located in the config directory.

	:param None

	:return: None
	"""
	for file in os.listdir(CONFIG_DIR):
		if file.endswith(".env"):
			load_dotenv(os.path.join(CONFIG_DIR, file))


def load_db_config() -> Dict[str, Union[int, str]]:
	"""
	Load the database configuration from the YAML file located in the config directory.

	:param None

	:return: The database configuration
	:rtype: Dict[str, Union[int, str]]
	"""
	with open(os.path.join(CONFIG_DIR, "db_config.yaml"), "r") as file:
		db_config: Dict[str, Union[int, str]] = yaml.safe_load(file.read())

	return db_config
