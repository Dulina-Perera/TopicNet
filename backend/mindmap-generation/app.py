# backend/mindmap-generation/main.py

# %%
import warnings; warnings.filterwarnings('ignore')
import os, sys; sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
import logging.config
import uvicorn
import yaml

from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Any, Dict

from api.v1.controllers import summarize_router

# %%
load_dotenv()

with open('config/log_config.yaml', 'r') as f:
	log_config: Dict[str, Any] = yaml.safe_load(f.read())

logging.config.dictConfig(log_config)

# %%
app: FastAPI = FastAPI(
	debug=True,
	title='TopicNet API',
	version='0.1.0',
)

app.include_router(summarize_router, prefix='/api/v1/summarize')

# %%
if __name__ == '__main__':
  uvicorn.run(
  	'app:app',
    host='127.0.0.1',
    port=5000,
    reload=True,
    log_level='info'
  )
