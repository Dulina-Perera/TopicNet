import logging
import numpy as np
from abc import ABC, abstractmethod
from typing import Any


class BaseClusterer(ABC):
	def __init__(self, model: Any = None) -> None:
		self.logger: logging.Logger = logging.getLogger(__name__)
		self.model: Any = model
		self.labels_: np.ndarray = None
		self.probabilities_: np.ndarray = None


	@abstractmethod
	def fit(self, embeddings: np.ndarray) -> 'BaseClusterer':
		self.labels_ = np.full(embeddings.shape[0], None, dtype=object)
		self.probabilities_ = np.full(embeddings.shape[0], None, dtype=object)

		return self


class HDBScanClusterer(BaseClusterer):
	def __init__(self, model: Any) -> None:
		super().__init__(model)


	def fit(self, embeddings: np.ndarray) -> 'HDBScanClusterer':
		self.model.fit(embeddings)
		self.logger.info('Fit HDBScan model.')

		self.labels_ = self.model.labels_
		self.probabilities_ = self.model.probabilities_

		return self

