# %%
import uvicorn

from fastapi.applications import FastAPI
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException

# %%
app: FastAPI = FastAPI()


@app.post('/topicnet/mindmap/generate')
async def generate_mindmap_from_pdf(file: UploadFile = None):
    # Verify that the file is a PDF.
    if file is None or file.content_type != 'application/pdf':
        return HTTPException(status_code=415, detail='Expected a `.pdf` file.')
    else:
        # TODO: Call the appropriate functions to generate a mindmap from the PDF.
    
    
        # TODO: Return the generated mindmap.
        return {'message': 'Mindmap generated successfully.'}

# %%
if __name__ == '__main__':
    uvicorn.run(app, port=5000, log_level='info')
