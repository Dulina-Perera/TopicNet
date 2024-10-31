# %%
# Import the required libraries, modules, classes and functions.
from fastapi import APIRouter, Depends, Request, Response
from logging import Logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from typing import Any, List, Optional

from ....core_ import (
  get_db_session,
  get_logger,
  read_files_owned_by_user_,
  read_nodes,
  read_user_id_by_session_id_
)

# %%
download_router_: APIRouter = APIRouter()

# %%
class FileResponse(BaseModel):
  id: int
  user_id: str
  name: str
  type: str
  path: str

  class Config:
    from_attributes: bool = True
    orm_mode: bool = True

class NodeResponse(BaseModel):
  id: int
  document_id: int
  parent_id: Optional[int]
  topic_and_content: str

  class Config:
    from_attributes: bool = True
    orm_mode: bool = True

# %%
@download_router_.get("/files")
async def download_file_metadata_(
	request_: Request,
	db_session_: async_scoped_session[AsyncSession] = Depends(get_db_session),
	logger_: Logger = Depends(get_logger)
) -> List[FileResponse]:
  # ################################################################################################
  # Extract the `session_id` from the request cookies.
  session_id_: str = request_.cookies.get("auth_session")

  # Read the `user_id` from the database using the `session_id`.
  user_id_: int = await read_user_id_by_session_id_(db_session_, session_id_)

  # ################################################################################################
  # Read the files owned by the user.
  files_: Any = await read_files_owned_by_user_(db_session_, user_id_)

  # Convert the files to the response model.
  response_: List[FileResponse] = [FileResponse.model_validate(file) for file in files_]

  logger_.info(f"Read {len(files_)} files from the database.")

  return response_

@download_router_.get("/nodes")
async def download_nodes_(
  document_id_: int,
	db_session_: async_scoped_session[AsyncSession] = Depends(get_db_session),
	logger_: Logger = Depends(get_logger)
) -> List[NodeResponse]:
  # ################################################################################################
  # Read the nodes for the given document.
  nodes_: Any = await read_nodes(db_session_, document_id_)

  # Convert the nodes to the response model.
  response_: List[NodeResponse] = [NodeResponse.model_validate(node) for node in nodes_]

  logger_.info(f"Read {len(nodes_)} nodes from the database.")

  return response_
