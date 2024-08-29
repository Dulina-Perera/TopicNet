# backend/app/api/v1/endpoints/mindmap.py

import os

from app.models import Node
from app.services import extract_text_from_pdf
from fastapi import APIRouter, File, HTTPException, UploadFile
from secrets import token_hex
from typing import Dict

router: APIRouter = APIRouter()

MAPPINGS: Dict[str, str] = {
	'Cognitive Analytics.pdf': '005f605e8b76deeea52dbf1e7d477a57'
}

@router.post('/generate')
async def generate_mindmap_from_pdf(file: UploadFile = File(...)):
  if file is None or file.content_type != 'application/pdf':
    return HTTPException(status_code=415, detail='Expected a `.pdf` file.')
  else:
    file_ext: str = file.filename.split('.')[-1]
    file_name: str = MAPPINGS.get(file.filename, token_hex(16))
    dir_path: str = f'./temp/{file_name}'
    file_path: str = f'{dir_path}/{file_name}.{file_ext}'

    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, 'wb') as f:
      content: bytes = await file.read()
      f.write(content)

    extract_text_from_pdf(file_path)

    return {
			'status': 'success',
			'message': 'File uploaded successfully.'
		}
