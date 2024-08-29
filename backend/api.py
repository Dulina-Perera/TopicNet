#

import uvicorn

from fastapi.applications import FastAPI

app: FastAPI = FastAPI(title='TopicNet API', version='0.1.0')


@app.post('/topicnet/mindmap/generate')
async def generate_mindmap_from_pdf(file: UploadFile = File(...)):
  if file is None or file.content_type != 'application/pdf':
    return HTTPException(status_code=415, detail='Expected a `.pdf` file.')
  else:
    file_ext: str = file.filename.split('.')[-1]
    file_name: str = token_hex(16)
    file_path: str = f'./temp/{file_name}.{file_ext}'

    with open(file_path, 'wb') as f:
      content: bytes = await file.read()
      f.write(content)

    # TODO: Call the appropriate functions to generate a mindmap from the PDF.

    return {
			'status': 'success',
			'message': 'File uploaded successfully.'
		}

if __name__ == '__main__':
  uvicorn.run(
    'api:app',
    host='127.0.0.1',
    port=5000,
    reload=True,
    log_level='info'
  )
