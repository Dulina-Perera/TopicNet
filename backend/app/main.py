# backend/app/main.py

import logging
import os
import sys
import uvicorn

from app.api.v1.endpoints import mindmap
from fastapi import FastAPI
from typing import Any, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

log_config: Dict[str, Any] = {
	'format': '%(asctime)s [%(levelname)s] %(message)s',
	'datefmt': '%Y-%m-%d %I:%M:%S %p',
	'level': logging.INFO,
	'force': True,
	'handlers': [
		logging.FileHandler('api.log', encoding='utf-8', errors='ignore'),
		logging.StreamHandler()
	]
}

logging.basicConfig(**log_config)

app: FastAPI = FastAPI(title='TopicNet API', version='0.1.0')

app.include_router(mindmap.router, prefix='/topicnet/mindmap/v1')

if __name__ == '__main__':
  os.environ['TOKENIZERS_PARALLELISM'] = 'false'

  uvicorn.run(
    'app.main:app',
    host='127.0.0.1',
    port=5000,
    reload=True,
    log_config=log_config
  )
