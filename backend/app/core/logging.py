# %%
# Import the required modules.
import logging
import os
import yaml

from typing import Any, Dict

# %%
def setup_logging() -> None:
  """
  Set up the logging configuration.

	This function loads the logging configuration from a YAML file and configures the logging system
	using the loaded configuration.

	Parameters:
		None

	Returns:
		None
  """
	# Load the logging configuration from the YAML file.
  with open(os.path.join(os.path.dirname(__file__), "../../config/log_config.yaml"), "r") as f:
    log_config: Dict[str, Any] = yaml.safe_load(f.read())

  logging.config.dictConfig(log_config)  # Configure the logging system.
