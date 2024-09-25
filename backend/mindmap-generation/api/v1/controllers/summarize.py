# backend/mindmap-generation/api/v1/controllers/summarize.py

# %%
from fastapi import Request, Response, APIRouter
from typing import Dict

from ..services import service_refine_summary_using_llm, service_summarize_using_spacy

# %%
summarize_router: APIRouter = APIRouter()

# %%
@summarize_router.post('/')
async def endpoint_summarize(request: Request) -> Response:
  # First check if body is None.
  body: bytes = await request.body()
  if not body:
    return Response(
      content='Expected request body',
      status_code=400,
      headers={'Content-Type': 'application/json'}
    )

  # Then check for the correct Content-Type.
  if request.headers.get('Content-Type') != 'text/plain':
    return Response(
      content='Expected Content-Type: text/plain',
      status_code=400,
      headers={'Content-Type': 'application/json'},
    )

  # If body is present and Content-Type is correct, decode the text.
  text: str = body.decode('utf-8')

  # Summarize the text using SpaCy and TextRank and refine the summary using OpenAI's GPT-4o-mini.
  refined_summary: str = service_refine_summary_using_llm(service_summarize_using_spacy(text))

  return Response(
    content=f'Summary: {refined_summary}',
    status_code=200,
    headers={'Content-Type': 'application/json'}
  )
