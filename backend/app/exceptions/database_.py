# %%
class DocumentDoesNotExistError(Exception):
  def __init__(self, document_id: str) -> None:
    super().__init__(f"Document {document_id} does not exist")

class NodeDoesNotExistError(Exception):
	def __init__(self, node_id: str) -> None:
		super().__init__(f"Node {node_id} does not exist")

class SentenceDoesNotExistError(Exception):
	def __init__(self, sentence_id: str) -> None:
		super().__init__(f"Sentence {sentence_id} does not exist")
