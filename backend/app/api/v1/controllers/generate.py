# %%
# Import the required modules.
import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from logging import Logger
from secrets import token_urlsafe
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from typing import Any, Dict, List, Union, Tuple

from ..services_ import (
  create_topic_dict,
  is_file_format_allowed,
  is_file_not_none,
  model_topics_with_nmf,
  parse_topic,
  refine_topic_n_content,
  refine_topic_and_content_using_openai,
  save_s3_uri,
  save_sentences_to_db,
  upload_file_to_s3
)
from ....core_ import get_db_session, get_logger, get_aws_s3_client
from ....exceptions_ import InvalidFileFormatError, NoFileSubmittedError

# %%
# Router for the generate endpoint
generate_router: APIRouter = APIRouter()

# %%
@generate_router.post("/base")
async def generate_base(
  file: Union[UploadFile, None] = File(default=None),
	db_session: scoped_session[Session] = Depends(get_db_session),
  s3_client: Any = Depends(get_aws_s3_client),
  logger: Logger = Depends(get_logger)
) -> Dict:
  try:
    # Check if a file was submitted.
    if not is_file_not_none(file):
      raise NoFileSubmittedError("No file was submitted.")

    # Check if the file format is allowed.
    ALLOWED_FILE_FORMATS: Tuple[str, ...] = ("application/pdf",)
    if not is_file_format_allowed(file, ALLOWED_FILE_FORMATS):
      raise InvalidFileFormatError(
        f"Invalid file format. Only {', '.join(ALLOWED_FILE_FORMATS)} files are supported."
      )

    # Upload the file to S3 and store the file's S3 URI in the database.
    s3_uri: str = upload_file_to_s3(file, token_urlsafe(16), s3_client)
    document_id: int = save_s3_uri(s3_uri, db_session, s3_client)

    # TODO: Implement the sentence extraction and preprocessing logic here. ########################
    with open(os.path.join(os.path.dirname(__file__), "../../../../static/uploads/cognitive-analytics/cognitive-analytics.clean.txt"), "r") as f:
      sentences: List[str] = [line.strip() for line in f if line.strip()]
    ################################################################################################

    # Save the sentences to the database.
    sentence_ids: List[int] = save_sentences_to_db(
      db_session,
      sentences,
      document_id,
      max_retries=3*len(sentences)
    )
    logger.info(f"Saved {len(sentence_ids)} sentences to the database.")

    # Model the topics using NMF.
    topics: List[str]
    _, topics = model_topics_with_nmf(sentences)
    topics = [parse_topic(topic) for topic in topics]

    # Create a dictionary mapping topics to the sentences that belong to them.
    topic_dict: Dict[str, str] = create_topic_dict(topics, sentences)

    # Refine the topics and content using OpenAI.
    refined_content: List[str] = []
    for (topic, content) in topic_dict.items():
      _ = await refine_topic_and_content_using_openai(topic, content)
      refined_content.append(_)

    # Return the document ID and the S3 URI.
    return {
			# "document_id": document_id,
			# "s3_uri": s3_uri,
			"content": refined_content
		}
  except NoFileSubmittedError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except InvalidFileFormatError as e:
    raise HTTPException(status_code=415, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
