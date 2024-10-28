# %%
class DatabaseInitializationError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(message)

class DocumentDoesNotExistError(Exception):
  def __init__(self, document_id: str) -> None:
    super().__init__(f"Document {document_id} does not exist.")

class NodeAlreadyHasChildrenError(Exception):
	def __init__(self, node_id: str, document_id: str) -> None:
		super().__init__(f"Node {node_id} already has children for document {document_id}.")

class NodeDoesNotExistError(Exception):
	def __init__(self, node_id: str, document_id: str) -> None:
		super().__init__(f"Node {node_id} does not exist for document {document_id}.")

class NodeDoesNotHaveEnoughSentencesToExtendError(Exception):
	def __init__(self, node_id: str, document_id: str) -> None:
		super().__init__(f"Node {node_id} does not have enough sentences to extend for document {document_id}.")

class SentenceDoesNotExistError(Exception):
	def __init__(self, sentence_id: str, document_id: str) -> None:
		super().__init__(f"Sentence {sentence_id} does not exist in document {document_id}.")
