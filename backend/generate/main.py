# %%
import nltk
import numpy as np
import os
import plotly.express as px

from hdbscan.hdbscan_ import HDBSCAN
from nltk.tokenize.punkt import PunktSentenceTokenizer
from pandas.core.frame import DataFrame
from pathlib import Path
from plotly.graph_objs._figure import Figure
from sentence_transformers.SentenceTransformer import SentenceTransformer
from sklearn.manifold._t_sne import TSNE
from typing import List, Union

# %%
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# %%
def extract_sentences_from_txt(path: Union[str, Path] = "./test.txt") -> List[str]:
  with open(path, mode="r", encoding="utf-8") as file:
    text: str = file.read()
    text = text.replace("\n", " ")

  tokenizer: PunktSentenceTokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
  sentences: List[str] = tokenizer.tokenize(text)
  
  return sentences


def embed_sentences(sentences: List[str]) -> List[List[float]]:
	model: SentenceTransformer = SentenceTransformer("all-mpnet-base-v2")
	embeddings: List[List[float]] = model.encode(sentences)
	
	return embeddings


def cluster_embeddings(embeddings: List[List[float]]) -> List[int]:
	clusterer: HDBSCAN = HDBSCAN(min_cluster_size=2, min_samples=1, metric="euclidean")
	clusters: List[int] = clusterer.fit_predict(embeddings)
 
	return clusters


def visualize_embeddings(embeddings: np.ndarray, clusters: List[int]):
  tsne: TSNE = TSNE(n_components=2, random_state=42)
  tsne_embeddings: np.ndarray = tsne.fit_transform(embeddings)
  
  fig: Figure = px.scatter(
    x=tsne_embeddings[:, 0],
    y=tsne_embeddings[:, 1],
    color=clusters.astype(str),
    labels={'color': 'Cluster'},
    title="t-SNE Visualization of Embeddings"
  )
  fig.show()

# %%
if __name__ == "__main__":
	sentences: List[str] = extract_sentences_from_txt()
	embeddings: List[List[float]] = embed_sentences(sentences)
	clusters: List[int] = cluster_embeddings(embeddings)
 
	df: DataFrame = DataFrame({
		"sentence": sentences,
		"embedding": [embedding.tolist() for embedding in embeddings],
		"cluster": clusters
	})

	df.to_csv("sentences_clusters.csv", index=False)
 
	visualize_embeddings(np.array(embeddings), clusters)
