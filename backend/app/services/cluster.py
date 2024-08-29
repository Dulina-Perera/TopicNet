# backend/app/services/cluster.py

import hdbscan
import logging
import math
import numpy as np

from hdbscan import HDBSCAN
from numpy import ndarray
from typing import Tuple

class NoEmbeddingsToClusterError(Exception):
	def __init__(self, message: str = 'No embeddings to cluster') -> None:
		super().__init__(message)


def cluster_embeddings(embeddings: ndarray) -> Tuple[ndarray, ndarray]:
	logger: logging.Logger = logging.getLogger(__name__)

	try:
		if not embeddings.any():
			raise NoEmbeddingsToClusterError()
		else:
			clusterer: HDBSCAN = HDBSCAN(
				min_cluster_size=math.ceil(len(embeddings) / 4),
				metric='euclidean',
				cluster_selection_method='eom',
				prediction_data=True
			)
			clusterer.fit(embeddings)
			logger.info('Fit HDBSCAN model.')

			membership_vectors: ndarray = hdbscan.all_points_membership_vectors(clusterer)
			cluster_cnt: int = membership_vectors.shape[1]

			membership_vectors = np.array([
				vec / np.sum(vec) if np.sum(vec) > 0 else vec
				for vec in membership_vectors
			])

			labels: ndarray = np.array([
				np.random.choice(cluster_cnt, p=vec)
				for vec in membership_vectors
			])
			logger.info('Assign labels to embeddings.')

			probabilities: ndarray = np.array([
				vec[label] for vec, label in zip(membership_vectors, labels)
			])

			return labels, probabilities
	except NoEmbeddingsToClusterError as e:
		logger.warning(e)
		return []
	except Exception as e:
		logger.error(f'Unexpected error: {e}.')
		return []
