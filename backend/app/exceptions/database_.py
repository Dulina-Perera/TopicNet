# %%
class NoSuchDocumentError(Exception):
  def __init__(self, document_id: str) -> None:
    super().__init__(f"No such document: {document_id}")

class NoSuchNodeError(Exception):
	def __init__(self, node_id: str) -> None:
		super().__init__(f"No such node: {node_id}")

class NoSuchSentenceError(Exception):
	def __init__(self, sentence_id: str) -> None:
		super().__init__(f"No such sentence: {sentence_id}")
