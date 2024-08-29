# backend/app/services/generate.py

from collections import defaultdict
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from typing import Dict, List


def generate_topics(df: DataFrame) -> DataFrame:
  sentences: List[str] = df['Sentence'].tolist()
  embeddings: List[List[float]] = df['Embedding'].tolist()
  clusters: List[int] = df['Cluster'].tolist()

  grouped_sentences = defaultdict(list)
  for sentence, cluster in zip(sentences, clusters):
    grouped_sentences[cluster].append(sentence)

  vectorizer: CountVectorizer = CountVectorizer(stop_words='english')
  transformer: TfidfTransformer = TfidfTransformer()

  topics: Dict = {}
  for cluster, sentences in grouped_sentences.items():
    X = vectorizer.fit_transform(sentences)
    tfidf_matrix = transformer.fit_transform(X)
    feature_names = vectorizer.get_feature_names_out()

    sorted_indices = tfidf_matrix.toarray().sum(axis=0).argsort()[::-1]
    top_terms = [feature_names[i] for i in sorted_indices[:10]]
    topics[cluster] = '-'.join(top_terms)

  df['Topic'] = df['Cluster'].map(topics)

  return df
