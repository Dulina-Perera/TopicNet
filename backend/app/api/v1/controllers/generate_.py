# %%
# Import the required libraries, modules, functions and classes.
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from logging import Logger
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from typing import Any, List, Union

from ..services_.generate_ import NodeResponse, generate_base
from ....core_ import get_aws_s3_client, get_db_session, get_logger
from ....exceptions_ import InvalidFileFormatError, NoFileSubmittedError

# %%
# Router for the generate endpoint
generate_router: APIRouter = APIRouter()

# %%
@generate_router.post("/base")
async def generate(
  file: Union[UploadFile, None] = File(default=None),
	db_session: scoped_session[Session] = Depends(get_db_session),
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
