# %%
# Import the required libraries, modules, functions and classes.
# from fastapi import APIRouter, Depends, HTTPException
# from pydantic import BaseModel
# from typing import Any

# from ....core_ import does_document_exist, does_node_exist, get_db_session, get_logger, update_node_content
# from ....exceptions_ import DocumentDoesNotExistError, NodeDoesNotExistError

# %%
# Router for the update endpoint
from fastapi import APIRouter
update_router: APIRouter = APIRouter()

# Request model for updating node content
# class UpdateNodeContentRequest(BaseModel):
#   content: str

# %%
# @update_router.post("/node")
# async def update(
#   document_id: int,
# 	node_id: int,
# 	update_request: UpdateNodeContentRequest,
#   db_session = Depends(get_db_session),
# 	logger = Depends(get_logger)
# ) -> Any:
#   """
#   Update the content of a node within a specific document.

#   :param document_id: The ID of the document containing the node
#   :type document_id: int

#   :param node_id: The ID of the node to update
#   :type node_id: int

#   :param update_request: The updated content for the node
#   :type update_request: UpdateNodeContentRequest

#   :return: Success message or error response
#   :rtype: Any
#   """
#   try:
#     # ################################################################################################
#   	# Check if the document exists in the database.
#     if not await does_document_exist(db_session, document_id):
#       raise DocumentDoesNotExistError(document_id)
#     logger.info(f"Document {document_id} exists.")

#     # Check if the node exists in the database.
#     if not await does_node_exist(db_session, node_id, document_id):
#       raise NodeDoesNotExistError(node_id, document_id)
#     logger.info(f"Node {node_id} exists for document {document_id}.")

# 		# ################################################################################################
#   	# Update the content of the node in the database.
#     await update_node_content(db_session, update_request.content, node_id, document_id)
#     logger.info(f"Node {node_id} content updated.")

#     # ################################################################################################
#   	# Return a success message.
#     return {"message": f"Node {node_id} updated successfully."}
#   except DocumentDoesNotExistError as e:
#     logger.error(e)
#     raise HTTPException(status_code=404, detail=str(e))
#   except NodeDoesNotExistError as e:
#     logger.error(e)
#     raise HTTPException(status_code=404, detail=str(e))
#   except Exception as e:
#     logger.error(e)
#     raise HTTPException(status_code=500, detail="Internal server error.")
