# %%
# Import the required libraries, modules, functions and classes.
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from logging import Logger
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from typing import Any, List, Union

from ..services_.generate_ import NodeResponse, extend_node, generate_base
from ....core_ import get_aws_s3_client, get_db_session, get_logger
from ....exceptions_ import InvalidFileFormatError, NoFileSubmittedError

# %%
# Router for the generate endpoint
generate_router: APIRouter = APIRouter()

# %%
@generate_router.post("/base")
async def generate(
  file: Union[UploadFile, None] = File(default=None),
	db_session: async_scoped_session[AsyncSession] = Depends(get_db_session),
	s3_client: Any = Depends(get_aws_s3_client),
	logger: Logger = Depends(get_logger)
) -> List[NodeResponse]:
  try:
    nodes: List[NodeResponse] = await generate_base(db_session, s3_client, logger, file)

    return nodes
  except NoFileSubmittedError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except InvalidFileFormatError as e:
    raise HTTPException(status_code=415, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@generate_router.post("/extend")
async def extend(
  document_id: int,
  node_id: int,
  db_session: async_scoped_session[AsyncSession] = Depends(get_db_session),
  logger: Logger = Depends(get_logger)
) -> List[NodeResponse]:
  try:
    nodes: List[NodeResponse] = await extend_node(document_id, node_id, db_session, logger)

    return nodes
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
