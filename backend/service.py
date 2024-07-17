# %%
import warnings; warnings.filterwarnings('ignore')

import logging
import os
import plotly.express as px

from numpy import ndarray
from pathlib import Path
from plotly.graph_objs._figure import Figure
from sklearn.manifold._t_sne import TSNE
from typing import List

from backend._2_clean._method import extract_sentences_from_cleaned_text
from backend._3_embed._embedder import SentenceTransformersEmbedder, extract_embeddings

# %%
def main():
  logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p',
    level=logging.INFO,
    force=True,
    handlers=[
        logging.FileHandler('service.log', encoding='utf-8', errors='ignore'),
        logging.StreamHandler()
    ]
	)
  logger: logging.Logger = logging.getLogger(__name__)

  os.environ['TOKENIZERS_PARALLELISM'] = 'false'

  sentences: List[str] = extract_sentences_from_cleaned_text(Path.cwd() / 'test.txt', logger)

  embedder: SentenceTransformersEmbedder = SentenceTransformersEmbedder('all-mpnet-base-v2')
  embeddings: ndarray = extract_embeddings(embedder, sentences, logger)


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
  main()
