import logging

from numpy import ndarray
from torch import Tensor
from typing import Any, List


class BaseEmbedder:
	def __init__(self, model: Any = None) -> None:
		self.logger: logging.Logger = logging.getLogger(__name__)
		self.model = model


	def embed(self, sentences: List[str]) -> ndarray | Tensor | List[Tensor]:
		pass
