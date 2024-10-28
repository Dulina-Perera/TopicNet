# %%
# Import the required libraries, modules, classes, and functions.
import logging
import os
import yaml

from dotenv import load_dotenv
from typing import Any, Dict, Tuple, Union

# %%
# The directory containing the configuration files
CONFIG_DIR: str = os.path.join(os.path.dirname(__file__), "../../config")

# %%
def is_env_var_set(env_var: str) -> bool:
	"""
	Check if the specified environment variable is set.

	:param env_var: The environment variable to check
	:type env_var: str

	:return: True if the environment variable is set, False otherwise
	:rtype: bool
	"""
	return os.getenv(env_var) is not None


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


def setup_logging() -> None:
  """
  Set up the logging system using the configuration from the YAML file located in the config directory.

	:param None

	:return: None
  """
  with open(os.path.join(CONFIG_DIR, "log_config.yaml"), "r") as file:
    log_config: Dict[str, Any] = yaml.safe_load(file.read())

  logging.config.dictConfig(log_config)
