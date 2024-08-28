import hdbscan
import logging
import numpy as np

from abc import ABC, abstractmethod
from backend._5_cluster._utils import does_support_hdbscan
from numpy import ndarray
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
		if not does_support_hdbscan(model):
			self.logger.error('HDBScanClusterer only supports HDBSCAN models.')
			raise
		else:
			super().__init__(model)
			self.logger.info('Initialize HDBScanClusterer.')


	def fit(self, embeddings: np.ndarray) -> 'HDBScanClusterer':
		self.model.fit(embeddings)
		self.logger.info('Fit HDBScan model.')

		membership_vectors: ndarray = hdbscan.all_points_membership_vectors(self.model)
		membership_vectors = np.array([
    	vec / np.sum(vec) if np.sum(vec) > 0 else vec
     	for vec in membership_vectors
    ])

		cluster_cnt: int = membership_vectors.shape[1]
		self.labels_ = np.array([
			np.random.choice(cluster_cnt, p=vec)
			for vec in membership_vectors
		])
		self.logger.info('Assign labels to embeddings.')

		self.probabilities_ = np.array([
			vec[label] for vec, label in zip(membership_vectors, self.labels_)
		])

		return self
