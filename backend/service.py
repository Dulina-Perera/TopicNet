# %%
import warnings; warnings.filterwarnings('ignore')

import logging
import nltk
import os
import plotly.express as px
import torch

from hdbscan.hdbscan_ import HDBSCAN
from math import floor
from nltk.tokenize.punkt import PunktSentenceTokenizer
from numpy import ndarray
from pandas.core.frame import DataFrame
from pathlib import Path
from plotly.graph_objs._figure import Figure
from sentence_transformers.SentenceTransformer import SentenceTransformer
from sklearn.manifold._t_sne import TSNE
from sklearn.preprocessing import normalize
from torch import Tensor
from typing import List, Union

# %%
# Setup logging configuration.
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s [%(levelname)s] %(message)s',
  handlers=[logging.FileHandler('generate.log'), logging.StreamHandler()]
)
logger: logging.Logger = logging.getLogger(__name__)

os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# %%
def extract_sentences_from_txt(path: Union[str, Path] = './test.txt') -> List[str]:
  try:
    # Ensure the file exists.
    if not Path(path).exists() or not Path(path).is_file():
      raise FileNotFoundError(f'File \'{path}\' does not exist or is not a file.')

    # Open the file and read the content.
    logger.info(f'Read file at path: {path}')
    with open(path, mode='r', encoding='utf-8') as file:
      content: str = file.read()

    # Replace newlines with spaces.
    content = content.replace('\n', ' ')

    # Load the Punkt tokenizer and tokenize the content into sentences.
    tokenizer: PunktSentenceTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    logger.info('Load Punkt tokenizer')
    sentences: List[str] = tokenizer.tokenize(content)
    logger.info(f'Extract {len(sentences)} sentences')

    return sentences
  except FileNotFoundError as e:
    logger.error(e)
    return []
  except UnicodeDecodeError as e:
    logger.error(f'Failed to decode the file at path \'{path}\'. Ensure it is a valid UTF-8 text file.')
    return []
  except Exception as e:
    logger.error(f'An unexpected error occurred: {e}')
    return []


def embed_sentences(sentences: List[str]) -> ndarray | Tensor | List[Tensor]:
  try:
    # Check if the sentences list is empty.
    if not sentences:
      raise ValueError('The sentences list is empty.')

    # Load the SentenceTransformer model.
    model_name: str = 'all-mpnet-base-v2'
    model: SentenceTransformer = SentenceTransformer(
      model_name,
      device='cuda' if torch.cuda.is_available() else 'cpu'
    )

    # Generate embeddings for the sentences.
    embeddings: ndarray | Tensor | List[Tensor] = model.encode(sentences, show_progress_bar=True)
    logger.info(f'Generate embeddings')

    return embeddings
  except ValueError as e:
    logger.error(e)
    return []
  except Exception as e:
    logger.error(f'An unexpected error occurred: {e}')
    return []


def cluster_embeddings(embeddings: List[List[float]]) -> List[int]:
  normalized_embeddings: ndarray = normalize(embeddings)

  clusterer: HDBSCAN = HDBSCAN(min_cluster_size=floor(len(embeddings) / 10), min_samples=1, metric='euclidean')
  clusters: List[int] = clusterer.fit_predict(normalized_embeddings)

  return clusters


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

# %%
if __name__ == '__main__':
  sentences: List[str] = extract_sentences_from_txt()
  embeddings: List[List[float]] = embed_sentences(sentences)
  clusters: List[int] = cluster_embeddings(embeddings)
  for (sentence, cluster) in zip(sentences, clusters):
    print(f'{cluster}: {sentence}', end='\n\n')

  # df: DataFrame = DataFrame({
	# 	'sentence': sentences,
	# 	'embedding': [embedding.tolist() for embedding in embeddings],
	# 	'cluster': clusters
	# })

  # df.to_csv('sentences_clusters.csv', index=False)

  # visualize_embeddings(array(embeddings), clusters)
