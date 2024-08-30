# backend/app/main.py

# %%
import warnings; warnings.filterwarnings('ignore')
import os, sys; sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import logging.config
import uvicorn

from fastapi import FastAPI
from dotenv import load_dotenv
from typing import Any, Dict
from app.api.v1.endpoints import mindmap

# %%
load_dotenv()

log_config: Dict[str, Any] = {
  'version': 1,
  'formatters': {
    'default': {
      'format': '%(asctime)s [%(levelname)s] %(message)s',
      'datefmt': '%Y-%m-%d %I:%M:%S %p'
    },
  },
  'handlers': {
    'file': {
      'class': 'logging.FileHandler',
      'filename': 'api.log',
      'formatter': 'default',
      'encoding': 'utf-8',
    },
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'default',
    },
  },
  'root': {
    'level': 'INFO',
    'handlers': ['file', 'console']
  },
}

logging.config.dictConfig(log_config)

# %%
app: FastAPI = FastAPI(title='TopicNet API', version='0.1.0')

app.include_router(mindmap.router, prefix='/topicnet/mindmap/v1')

# %%
if __name__ == '__main__':
  os.environ['TOKENIZERS_PARALLELISM'] = 'false'

  uvicorn.run(
  	'app.main:app',
    host='127.0.0.1',
    port=5000,
    reload=True,
    log_level='info'
  )
