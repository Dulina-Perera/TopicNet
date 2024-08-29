# backend/app/main.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from fastapi import FastAPI
from app.api.v1.endpoints import mindmap

app: FastAPI = FastAPI(title='TopicNet API', version='0.1.0')

app.include_router(mindmap.router, prefix='/topicnet/mindmap/v1')

if __name__ == '__main__':
  uvicorn.run(
    'app.main:app',
    host='127.0.0.1',
    port=5000,
    reload=True,
    log_level='info'
  )

