# backend/app.py

# %%
import warnings; warnings.filterwarnings('ignore')
import os, sys; sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
import logging.config
import yaml

from dotenv import load_dotenv
from robyn import Robyn
from typing import Any, Dict

# %%
load_dotenv()

with open('log_config.yaml', 'r') as f:
	log_config: Dict[str, Any] = yaml.safe_load(f.read())

logging.config.dictConfig(log_config)

# %%
app: Robyn = Robyn(__file__)


@app.get('/')
async def index():
  return 'Hello World!'


# %%
if __name__ == '__main__':
  app.start(host='127.0.0.1', port=8080)
