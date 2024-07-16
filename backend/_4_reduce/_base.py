import logging

from abc import ABC, abstractmethod
from numpy import ndarray
from typing import Any

class BaseDimensionalityReducer(ABC):
	def __init__(self, model: Any) -> None:
		self.logger: logging.Logger = logging.getLogger(__name__)
		self.model = model


	@abstractmethod
	def fit(self, X: ndarray) -> 'BaseDimensionalityReducer':
		return self


	@abstractmethod
	def transform(self, X: ndarray) -> ndarray:
		return X
