# backend/app/services/embed.py

import logging
import plotly.express as px
import torch

from numpy import ndarray
from plotly.graph_objs import Figure
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
from typing import List
from umap import UMAP

class NoSentencesToEncodeError(Exception):
	def __init__(self, message: str = 'No sentences to encode') -> None:
		super().__init__(message)

class NoEmbeddingsToReduceError(Exception):
	def __init__(self, message: str = 'No embeddings to reduce') -> None:
		super().__init__(message)


def extract_embeddings(sentences: List[str]) -> ndarray:
  logger: logging.Logger = logging.getLogger(__name__)

  try:
    if not sentences:
      raise NoSentencesToEncodeError()
    else:
      embedder: SentenceTransformer = SentenceTransformer(
        'all-mpnet-base-v2',
        device='cuda' if torch.cuda.is_available() else 'cpu'
      )
      logger.info(f'Initialize SentenceTransformer embedder: {embedder}.')

      embeddings: ndarray = embedder.encode(
				sentences,
				show_progress_bar=True
			)
      logger.info('Embed sentences.')

      return embeddings
  except NoSentencesToEncodeError as e:
    logger.warning(e)
    return []
  except Exception as e:
    logger.error(f'Unexpected error: {e}.')
    return []


def reduce_embeddings(embeddings: ndarray) -> ndarray:
	logger: logging.Logger = logging.getLogger(__name__)

	try:
		if not embeddings.any():
			raise NoEmbeddingsToReduceError()
		else:
			reducer: UMAP = UMAP(
				n_neighbors=16,
				n_components=8,
				min_dist=0.0,
				metric='cosine',
				low_memory=True
			)
			logger.info('Initialize UMAP reducer.')

			reduced_embeddings: ndarray = reducer.fit_transform(embeddings)
			logger.info(f'Reduce embeddings to {reduced_embeddings.shape[1]} dimensions.')

			return reduced_embeddings
	except NoEmbeddingsToReduceError as e:
		logger.warning(e)
		return []
	except Exception as e:
		logger.error(f'Unexpected error: {e}.')
		return []


def visualize_embeddings(embeddings: ndarray, clusters: List[int]):
  tsne: TSNE = TSNE(n_components=2, random_state=42)
  tsne_embeddings: ndarray = tsne.fit_transform(embeddings)

  fig: Figure = px.scatter(
    x=tsne_embeddings[:, 0],
    y=tsne_embeddings[:, 1],
    color=clusters.astype(str),
    labels={'color': 'Cluster'},
    title='t-SNE Visualization of Embeddings'
  )
  fig.show()
