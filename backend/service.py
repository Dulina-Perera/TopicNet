# %%
import warnings; warnings.filterwarnings('ignore')

import logging
import nltk
import os
import plotly.express as px

from collections import defaultdict
from hdbscan import HDBSCAN
from IPython.display import display
from nltk.tokenize.punkt import PunktSentenceTokenizer
from numpy import ndarray
from pandas import DataFrame
from pathlib import Path
from plotly.graph_objs._figure import Figure
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold._t_sne import TSNE
from typing import Dict, List, Union
from umap import UMAP

from _3_embed import BaseEmbedder, NoSentencesToEncodeError, SentenceTransformersEmbedder
from _5_cluster import HDBScanClusterer

# %%
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

# %%
def extract_sentences_from_cleaned_text(path: Union[str, Path]) -> List[str]:
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
    logger.error(f'Fail to decode the file at path \'{path}\'. Ensure it is a valid UTF-8 text file.')
    return []
  except Exception as e:
    logger.error(f'An unexpected error: {e}.')
    return []


def extract_embeddings(
  model: BaseEmbedder,
  sentences: List[str]
) -> ndarray:
  try:
    if not sentences:
      raise NoSentencesToEncodeError()
    else:
      embeddings: ndarray = model.embed(sentences)
      return embeddings
  except NoSentencesToEncodeError as e:
    logger.warning(e)
    return []
  except Exception as e:
    logger.error(f'Unexpected error: {e}.')
    return []


def main():
  os.environ['TOKENIZERS_PARALLELISM'] = 'false'

  sentences: List[str] = extract_sentences_from_cleaned_text(Path.cwd() / 'test.txt')

  embedder: SentenceTransformersEmbedder = SentenceTransformersEmbedder('all-mpnet-base-v2')
  embeddings: ndarray = extract_embeddings(embedder, sentences)

  reducer: UMAP = UMAP(
    n_neighbors=15,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    low_memory=True
  )
  embeddings = reducer.fit_transform(embeddings)
  logger.info(f'Reduce embeddings to {embeddings.shape[1]} dimensions.')

  hdbscan_model: HDBSCAN = HDBSCAN(
    min_cluster_size=2,
		metric='euclidean',
  	cluster_selection_method="eom",
		prediction_data=True
	)
  clusterer: HDBScanClusterer = HDBScanClusterer(hdbscan_model)
  clusterer.fit(embeddings)
  clusters: ndarray = clusterer.labels_

  # Visualize embeddings.
  visualize_embeddings(embeddings, clusters)

  df: DataFrame = DataFrame({
		'Sentence': sentences,
		'Embedding': embeddings.tolist(),
		'Cluster': clusters.tolist()
	})

  # Initialize CountVectorizer and TfidfTransformer.
  vectorizer: CountVectorizer = CountVectorizer(stop_words='english')
  transformer: TfidfTransformer = TfidfTransformer()

  # Group sentences by cluster.
  grouped_sentences = defaultdict(list)
  for sentence, cluster in zip(sentences, clusters):
    grouped_sentences[cluster].append(sentence)

  # Create topics for each cluster.
  topics: Dict = {}
  for cluster, sentences in grouped_sentences.items():
    X = vectorizer.fit_transform(sentences)
    tfidf_matrix = transformer.fit_transform(X)
    feature_names = vectorizer.get_feature_names_out()

    # Get the top 10 words for each cluster.
    sorted_indices = tfidf_matrix.toarray().sum(axis=0).argsort()[::-1]
    top_terms = [feature_names[i] for i in sorted_indices[:10]]
    topics[cluster] = '-'.join(top_terms)

  # Add topics to the dataframe.
  df['Topic'] = df['Cluster'].map(topics)

  df.to_csv('test.csv', index=False)



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
