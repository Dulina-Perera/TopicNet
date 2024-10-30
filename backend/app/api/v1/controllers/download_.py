# %%
# Import the required libraries, modules, classes and functions.
from fastapi import APIRouter, Depends, Response
from logging import Logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from typing import Any, List, Optional

from ....core_ import get_db_session, get_logger, read_nodes

# %%
download_router_: APIRouter = APIRouter()

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
@download_router_.get("/nodes")
async def download_nodes_(
  document_id_: int,
	db_session_: async_scoped_session[AsyncSession] = Depends(get_db_session),
	logger_: Logger = Depends(get_logger)
):
  # ################################################################################################
  # Read the nodes for the given document.
  nodes_: Any = await read_nodes(db_session_, document_id_)

  # Convert the nodes to the response model.
  response_: List[NodeResponse] = [NodeResponse.model_validate(node) for node in nodes_]

  logger_.info(f"Read {len(nodes_)} nodes from the database.")

  return response_
