# %%
# Import the required libraries, modules, functions and classes.
import asyncio
import os

from fastapi import APIRouter, Depends, File, Request, Response, UploadFile
from logging import Logger
from pydantic import BaseModel
from secrets import token_urlsafe
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from typing import Any, Dict, List, Optional, Tuple

from ..services_ import (
  create_topic_dict,
  is_file_format_allowed,
  is_file_not_none,
  model_topics_with_nmf,
  parse_topic,
  refine_summary_using_openai,
  refine_topic_and_content_using_openai,
  summarize_using_spacy,
  upload_file_to_s3
)
from ....core_ import (
  bind_sentence_to_node,
  create_base_nodes,
  create_document_,
  does_document_exist_,
  does_node_exist,
  get_aws_s3_client,
  get_db_session,
  get_logger,
  get_nodes_by_ids,
  has_child_nodes,
  read_nodes,
  read_sentences_belonging_to_node,
  read_user_id_by_session_id_,
  save_node_layer,
  save_sentences
)
from ....exceptions_ import (
  DocumentDoesNotExistError,
  InvalidFileFormatError,
  NodeDoesNotExistError,
  NodeAlreadyHasChildrenError,
  NodeDoesNotHaveEnoughSentencesToExtendError,
  NoFileSubmittedError
)

# %%
# Router for the generate endpoint
generate_router_: APIRouter = APIRouter()

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
@generate_router_.post("/base")
async def generate_base_(
  request_: Request,
  file_: Optional[UploadFile] = File(default=None),
	db_session_: async_scoped_session[AsyncSession] = Depends(get_db_session),
	s3_client_: Any = Depends(get_aws_s3_client),
	logger_: Logger = Depends(get_logger)
) -> List[NodeResponse]:
  # ################################################################################################
  # Extract the `session_id` from the request cookies.
  session_id_: str = request_.cookies.get("auth_session")

  # Read the `user_id` from the database using the `session_id`.
  user_id_: int = await read_user_id_by_session_id_(db_session_, session_id_)

  # ################################################################################################
  # Check if a file was submitted.
  if not is_file_not_none(file_):
    raise NoFileSubmittedError()

  # Check if the file format is allowed.
  ALLOWED_FILE_FORMATS_: Tuple[str, ...] = ("application/pdf",)
  if not is_file_format_allowed(file_, ALLOWED_FILE_FORMATS_):
    raise InvalidFileFormatError(ALLOWED_FILE_FORMATS_)

  logger_.info(f"Received {file_.filename} with content type {file_.content_type} and size {file_.size} bytes.")

  # ################################################################################################
  # Extract the file name and file's content type.
  file_name_: str = file_.filename
  content_type_: str = file_.content_type

  # Save the file to S3 and retrieve the S3 URI.
  path_: str = await upload_file_to_s3(file_, token_urlsafe(16), s3_client_)

  logger_.info(f"Uploaded the file to S3 with URI {path_}.")

 	# Insert the document metadata into the database.
  document_: Any = await create_document_(db_session_, user_id_, file_name_, content_type_, path_)

  logger_.info(f"Inserted the document metadata into the database with ID {document_.id}.")

  # ################################################################################################
  # TODO: Implement the sentence extraction and preprocessing logic here. ########################
  with open(os.path.join(os.path.dirname(__file__), "../../../../static/uploads/cognitive-analytics/cognitive-analytics.clean.txt"), "r") as f:
    sentences_: List[str] = [line.strip() for line in f if line.strip()]

  logger_.info(f"Extracted {len(sentences_)} sentences from the file.")

  # Save the sentences to the database.
  sentence_ids_: List[int] = await save_sentences(db_session_, sentences_, document_.id)

  logger_.info(f"Saved {len(sentence_ids_)} sentences to the database.")

  # ################################################################################################
  # Summarize the content in a parallel manner.
  summarize_task_: asyncio.Task = asyncio.create_task(refine_summary_using_openai(summarize_using_spacy(" ".join(sentences_))))

  # ################################################################################################
  # Perform topic modeling using NMF.
  topics_: List[str]
  _, topics_ = model_topics_with_nmf(sentences_)
  topics_ = [parse_topic(topic) for topic in topics_]

  topic_dict_: Dict[str, str] = create_topic_dict(topics_, sentences_)

  # Refine the topics and content using OpenAI.
  refined_content_: List[str] = []
  for (topic_, content_) in topic_dict_.items():
    _ = await refine_topic_and_content_using_openai(topic_, content_)
    refined_content_.append(_)

  logger_.info(f"Performed topic modeling with NMF and refined the topics and content using OpenAI.")

  # Wait for the summarization task to complete.
  summary_: str = await summarize_task_

  refined_content_.insert(0, summary_)

  # Save the refined content to the database.
  node_ids_: List[int] = await create_base_nodes(db_session_, refined_content_, document_.id)

  logger_.info(f"Saved {len(node_ids_)} base nodes to the database.")

  # ################################################################################################
  # Bind sentences to the respective nodes.
  topic_to_node_mapping_: Dict[str, int] = {topic: node_id for (node_id, topic) in enumerate(topic_dict_.keys(), start=1)}
  topics_as_node_ids_: List[int] = [topic_to_node_mapping_[topic] for topic in topics_]

  for (sentence_id_, node_id_) in zip(sentence_ids_, topics_as_node_ids_):
    _ = await bind_sentence_to_node(db_session_, sentence_id_, document_.id, node_id_)

  logger_.info(f"Bound {len(sentence_ids_)} sentences to the respective nodes.")

  # ################################################################################################
  # Read the nodes from the database.
  nodes_: List[Any] = await read_nodes(db_session_, document_.id)

  # Convert the nodes to the response model.
  response_: List[NodeResponse] = [NodeResponse.model_validate(node) for node in nodes_]

  logger_.info(f"Read {len(nodes_)} nodes from the database.")

  return response_

@generate_router_.post("/extend")
async def extend_node_(
	document_id: int,
	node_id: int,
	db_session_: async_scoped_session[AsyncSession] = Depends(get_db_session),
	logger_: Logger = Depends(get_logger)
) -> List[NodeResponse]:
  """
	Extend the specified node in the specified document by generating child nodes.

	:param document_id: The ID of the document
	:type document_id: int

	:param node_id: The ID of the node
	:type node_id: int

	:param db_session: The database session
	:type db_session: AsyncSession

	:param logger: The logger
	:type logger: Logger

	:return: The child nodes
	:rtype: List[NodeResponse]
 	"""
  # ################################################################################################
  # Check if the document exists in the database.
  if not await does_document_exist_(db_session_, document_id):
    raise DocumentDoesNotExistError(document_id)
  logger_.info(f"Document {document_id} exists.")

  # Check if the node exists in the database.
  if not await does_node_exist(db_session_, node_id, document_id):
    raise NodeDoesNotExistError(node_id, document_id)
  logger_.info(f"Node {node_id} exists for document {document_id}.")

  # Check if the node already has children.
  if await has_child_nodes(db_session_, node_id, document_id):
    raise NodeAlreadyHasChildrenError(node_id, document_id)
  logger_.info(f"Node {node_id} does not have children for document {document_id}.")

  # ################################################################################################
  # Get the sentences associated with the specified node.
  tmp: List[Any] = await read_sentences_belonging_to_node(db_session_, node_id, document_id)
  sentences: List[str] = [_.content for _ in tmp]
  sentence_ids: List[int] = [_.id for _ in tmp]

  logger_.info(f"Retrieved {len(sentences)} sentences associated with node {node_id} for document {document_id}.")

  if len(sentences) < 2:
    raise NodeDoesNotHaveEnoughSentencesToExtendError(node_id, document_id)

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

  logger_.info(f"Performed topic modeling with NMF and refined the topics and content using OpenAI.")

  # Save the refined content to the database.
  node_ids: List[int] = await save_node_layer(db_session_, refined_content, node_id, document_id)

  logger_.info(f"Saved {len(node_ids)} child nodes to the database.")

  # ################################################################################################
  # Rebond the sentences to the respective nodes.
  topic_to_node_mapping: Dict[str, int] = {topic: node_id for (node_id, topic) in enumerate(topic_dict.keys(), start=node_ids[0])}
  topics_as_node_ids: List[int] = [topic_to_node_mapping[topic] for topic in topics]

  for (sentence_id, _node_id) in zip(sentence_ids, topics_as_node_ids):
    _ = await bind_sentence_to_node(db_session_, sentence_id, document_id, _node_id)

  # ################################################################################################
  # Read the nodes from the database.
  nodes: List[Any] = await get_nodes_by_ids(db_session_, node_ids, document_id)

  # Convert the nodes to the response model.
  nodes_response: List[NodeResponse] = [NodeResponse.model_validate(node) for node in nodes]
  logger_.info(f"Read {len(nodes)} nodes from the database.")

  return nodes_response
