from abc import ABC, abstractmethod
import logging

from numpy import ndarray
from torch import Tensor
from typing import Any, List


class BaseEmbedder(ABC):
	def __init__(self, model: Any = None) -> None:
		self.logger: logging.Logger = logging.getLogger(__name__)
		self.model = model


	@abstractmethod
	def embed(self, sentences: List[str]) -> ndarray | Tensor | List[Tensor]:
		pass
