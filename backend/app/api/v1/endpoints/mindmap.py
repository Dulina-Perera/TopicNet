# backend/app/api/v1/endpoints/mindmap.py

import os

from app.models import Node
from app.services import cluster_embeddings, extract_embeddings, extract_text_from_pdf, extract_sentences_from_cleaned_text, generate_topics, reduce_embeddings, summarize_text, visualize_embeddings
from fastapi import APIRouter, File, HTTPException, UploadFile
from numpy import ndarray
from pandas import DataFrame
from secrets import token_hex
from typing import Dict, List

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

    meta_title: str = extract_text_from_pdf(file_path)

    sentences: List[str] = extract_sentences_from_cleaned_text(f'{dir_path}/{file_name}.clean.txt')

    embeddings: ndarray = extract_embeddings(sentences)
    embeddings = reduce_embeddings(embeddings)

    labels: ndarray; probabilities: ndarray
    labels, probabilities = cluster_embeddings(embeddings)

    visualize_embeddings(embeddings, labels)

    df: DataFrame = DataFrame({
			'Sentence': sentences,
			'Embedding': embeddings.tolist(),
			'Cluster': labels.tolist(),
			'Probability': probabilities.tolist()
		})

    df = generate_topics(df)

    df.to_csv(f'{dir_path}/{file_name}.csv', index=False)

    root_topic: str; root_content: str
    with open(f'{dir_path}/{file_name}.clean.txt', 'r') as f:
      cleaned_text: str = f.read()
      root_topic, root_content = summarize_text(cleaned_text, meta_title)
    print(f"Root topic: {root_topic}")
    print(f"Root content: {root_content}")

    return {
			'status': 'success',
			'message': 'File uploaded successfully.'
		}
