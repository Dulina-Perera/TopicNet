# %%
import os

from fastapi import APIRouter, Depends, File, Response, UploadFile
from logging import Logger
from typing import List, Tuple, Union

from ..services_ import (
  is_file_format_allowed,
  is_file_not_none,
  refine_summary_using_openai,
  summarize_using_spacy
)
from ....core_ import get_logger
from ....exceptions_ import InvalidFileFormatError, NoFileSubmittedError

# %%
summarize_router: APIRouter = APIRouter()

# %%
@summarize_router.post("")
async def summarize(
  file: Union[UploadFile, None] = File(default=None),
	logger: Logger = Depends(get_logger)
) -> Response:
  try:
    # Check if a file was submitted.
    if not is_file_not_none(file):
      raise NoFileSubmittedError()

    # Check if the file format is allowed.
    ALLOWED_FILE_FORMATS: Tuple[str, ...] = ("application/pdf",)
    if not is_file_format_allowed(file, ALLOWED_FILE_FORMATS):
      raise InvalidFileFormatError(ALLOWED_FILE_FORMATS)

    # TODO: Implement the sentence extraction and preprocessing logic here. ########################
    with open(os.path.join(os.path.dirname(__file__), "../../../../static/uploads/cognitive-analytics/cognitive-analytics.clean.txt"), "r") as f:
      sentences: List[str] = [line.strip() for line in f if line.strip()]
      text: str = " ".join(sentences)
    ################################################################################################

    # Summarize the text using SpaCy and TextRank and refine the summary using OpenAI"s GPT-4o-mini.
    summary: str = summarize_using_spacy(text)
    refined_summary: str = await refine_summary_using_openai(summary)

    return Response(
    	content=refined_summary,
    	status_code=200,
    	headers={"Content-Type": "application/json"}
  	)
  except Exception as e:
    logger.error(f"An error occurred while summarizing the document: {e}")
    return Response(
			content={"error": str(e)},
			status_code=500,
			headers={"Content-Type": "application/json"}
		)
