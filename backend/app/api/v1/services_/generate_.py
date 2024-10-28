# %%
# Import the required libraries, modules, classes, and functions.
import asyncio
import os

from fastapi import File, UploadFile
from logging import Logger
from pydantic import BaseModel
from secrets import token_urlsafe
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from typing import Any, Dict, List, Optional, Tuple

from .file_storage_ import upload_file_to_s3
from .summarization import refine_summary_using_openai, summarize_using_spacy
from .topic_and_content_refinement_ import refine_topic_and_content_using_openai
from .topic_modeling import create_topic_dict, model_topics_with_nmf, parse_topic
from .verification_and_validation_ import is_file_format_allowed, is_file_not_none
from ....core_ import (
  bind_sentence_to_node,
  read_nodes,
  save_base_nodes,
  save_s3_uri,
  save_sentences
)
from ....exceptions_ import InvalidFileFormatError, NoFileSubmittedError

# %%
class NodeResponse(BaseModel):
  id: int
  document_id: int
  parent_id: Optional[int]
  topic_and_content: str

  class Config:
    from_attributes: bool = True
    orm_mode: bool = True

# %%
async def generate_base(
  db_session: async_scoped_session[AsyncSession],
  s3_client: Any,
  logger: Logger,
  file: Optional[UploadFile] = File(default=None)
) -> List[NodeResponse]:
  # ################################################################################################
  # Check if a file was submitted.
  if not is_file_not_none(file):
    raise NoFileSubmittedError()

  # Check if the file format is allowed.
  ALLOWED_FILE_FORMATS: Tuple[str, ...] = ("application/pdf",)
  if not is_file_format_allowed(file, ALLOWED_FILE_FORMATS):
    raise InvalidFileFormatError(ALLOWED_FILE_FORMATS)

  logger.info(f"Received {file.filename} with content type {file.content_type} and size {file.size} bytes.")

	# ################################################################################################
  # Upload the file to S3 and store the file's S3 URI in the database.
  s3_uri: str = await upload_file_to_s3(file, token_urlsafe(16), s3_client)
  document_id: int = await save_s3_uri(db_session, s3_uri)

  logger.info(f"Uploaded the file to S3 with URI {s3_uri}.")

  # ################################################################################################
  # TODO: Implement the sentence extraction and preprocessing logic here. ########################
  with open(os.path.join(os.path.dirname(__file__), "../../../../static/uploads/cognitive-analytics/cognitive-analytics.clean.txt"), "r") as f:
    sentences: List[str] = [line.strip() for line in f if line.strip()]

  logger.info(f"Extracted {len(sentences)} sentences from the file.")

  # Save the sentences to the database.
  sentence_ids: List[int] = await save_sentences(db_session, sentences, document_id)

  logger.info(f"Saved {len(sentence_ids)} sentences to the database.")

  # ################################################################################################
  # Summarize the content in a parallel manner.
  summarize_task: asyncio.Task = asyncio.create_task(refine_summary_using_openai(summarize_using_spacy(" ".join(sentences))))

  # ################################################################################################
  # Perform topic modeling using NMF.
  topics: List[str]
  _, topics = model_topics_with_nmf(sentences)
  topics = [parse_topic(topic) for topic in topics]

  topic_dict: Dict[str, str] = create_topic_dict(topics, sentences)

  # Refine the topics and content using OpenAI.
  refined_content: List[str] = []
  for (topic, content) in topic_dict.items():
    _ = await refine_topic_and_content_using_openai(topic, content)
    refined_content.append(_)

  logger.info(f"Performed topic modeling with NMF and refined the topics and content using OpenAI.")

  # ################################################################################################
  # Wait for the summarization task to complete.
  summary: str = await summarize_task

  refined_content.insert(0, summary)

  # Save the refined content to the database.
  node_ids: List[int] = await save_base_nodes(db_session, refined_content, document_id)

  logger.info(f"Saved {len(node_ids)} base nodes to the database.")

  # ################################################################################################
  # Bind sentences to the respective nodes.
  topic_to_node_mapping: Dict[str, int] = {topic: node_id for (node_id, topic) in enumerate(topic_dict.keys(), start=1)}
  topics_as_node_ids: List[int] = [topic_to_node_mapping[topic] for topic in topics]

  for (sentence_id, node_id) in zip(sentence_ids, topics_as_node_ids):
    _ = await bind_sentence_to_node(db_session, sentence_id, document_id, node_id)

  logger.info(f"Bound {len(sentence_ids)} sentences to the respective nodes.")

  # ################################################################################################
  # Read the nodes from the database.
  nodes: List[Any] = await read_nodes(db_session, document_id)

  # Convert the nodes to the response model.
  nodes_response: List[NodeResponse] = [NodeResponse.model_validate(node) for node in nodes]

  logger.info(f"Read {len(nodes)} nodes from the database.")
  return nodes_response


