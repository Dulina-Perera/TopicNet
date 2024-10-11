# %%
import numpy as np
import random
import re
import os

from gensim.corpora import Dictionary
from gensim.models import CoherenceModel, Nmf, TfidfModel
from typing import List, Tuple, Union

# from ....exceptions import InsufficientContextException

# %%
def cvt_corpus_to_bow_fmt(corpus: List[str]) -> Tuple[List[List[Tuple[int, int]]], Dictionary]:
  """
	Convert a corpus of documents to bag-of-words format.

	Parameters:
	- corpus: List of documents

	Returns:
	- Tuple containing the bag-of-words representation of the corpus and the dictionary
  """
  # Lowercase each document, split it by white space.
  _corpus: List[List[str]] = [doc.lower().split() for doc in corpus]

  # Associate each unique word in the corpus with a unique integer ID.
  dictionary: Dictionary = Dictionary(_corpus)

  # Convert the corpus to bag-of-words format.
  bow_vectors: List[List[Tuple[int, int]]] = [dictionary.doc2bow(doc) for doc in _corpus]

  return bow_vectors, dictionary


def transform_bow_vectors_to_tfidf_fmt(
  bow_vectors: List[List[Tuple[int, int]]],
  dictionary: Dictionary
) -> List[List[Tuple[int, float]]]:
	"""
	Transform bag-of-words vectors to TF-IDF format.

	Parameters:
	- bow_vectors: Bag-of-words representation of the corpus
	- dictionary: Dictionary object

	Returns:
	- TF-IDF representation of the corpus
	"""
	# Transform the bag-of-words vectors to TF-IDF format.
	tfidf_model: TfidfModel = TfidfModel(bow_vectors, dictionary=dictionary)
	tfidf_vectors: List[List[Tuple[int, float]]] = tfidf_model[bow_vectors]

	return tfidf_vectors


def parse_topic(topic_str: str) -> str:
  """
  Parse a topic string in the format '0.036*"disadvantages" + 0.030*"cons" + ...'
    and return a string with the words joined by hyphens.

    Parameters:
    - topic_str (str): The topic string to be parsed.

    Returns:
    - str: A string of words separated by hyphens.
  """
  # Use regular expression to find all words between the quotes.
  words = re.findall(r'\"(.*?)\"', topic_str)

  # Join the words with hyphens.
  return '-'.join(words)



def model_topics_with_nmf(
  corpus: List[str],
  min_topics: int = 2,
  max_topics: int = 6,
  normalize: bool = True,
  random_state: int = random.randint(0, 100)
) -> Tuple[Nmf, List[str]]:
  """
  Model topics using non-negative matrix factorization (NMF).

	Parameters:
	- corpus: List of documents
	- min_topics: Minimum number of topics
	- max_topics: Maximum number of topics
	- normalize: Whether to normalize the result
	- random_state: Random seed

	Returns:
	- NMF model
	- List of topic classifications for each document
  """
  # Lowercase each document, split it by white space.
  _corpus: List[List[str]] = [doc.lower().split() for doc in corpus]

  # Transform the corpus to the bag-of-words format.
  bow_vectors: List[List[Tuple[int, int]]]; dictionary: Dictionary
  bow_vectors, dictionary = cvt_corpus_to_bow_fmt(corpus)

  # Transform the bag-of-words vectors to TF-IDF format.
  tfidf_vectors: List[List[Tuple[int, float]]] = transform_bow_vectors_to_tfidf_fmt(bow_vectors, dictionary)

  if len(tfidf_vectors) < min_topics:
    # raise InsufficientContextException("Insufficient context to model topics.")
    raise ValueError("Insufficient context to model topics.")

  best_n_topics: Union[int, None] = None
  best_nmf_model: Union[Nmf, None] = None
  best_coherence_score: float = -np.inf

  # Iterate over the range of possible number of topics.
  for n_topics in range(min_topics, max_topics + 1):
    # Train an NMF model.
    nmf_model: Nmf = Nmf(
			corpus=tfidf_vectors,
			num_topics=n_topics,
			id2word={v: k for (k, v) in dictionary.token2id.items()},
			normalize=normalize,
			random_state=random_state
		)

    # Evaluate the model using the coherence score.
    coherence_model: CoherenceModel = CoherenceModel(
			model=nmf_model,
			texts=_corpus,
			dictionary=dictionary,
			coherence='c_v'
		)
    coherence_score: float = coherence_model.get_coherence()

    # Update the best model if the current model has a higher coherence score.
    if coherence_score > best_coherence_score:
      best_n_topics = n_topics
      best_nmf_model = nmf_model
      best_coherence_score = coherence_score

  # Get topics for each document.
  topic_classifications: List[str] = []
  for vec in bow_vectors:
    topic_distribution: List[Tuple[int, float]] = best_nmf_model.get_document_topics(
      vec,
      minimum_probability=0.0,
      normalize=True
    )

    # Get the most probable topic for the document.
    topic_id: int = max(topic_distribution, key=lambda x: x[1])[0]
    topic: str = best_nmf_model.print_topic(topic_id)
    topic_classifications.append(topic)

  return best_nmf_model, topic_classifications


# %%
if __name__ == '__main__':
  with open(os.path.join(os.path.dirname(__file__), "../../../../static/uploads/cognitive-analytics/cognitive-analytics.clean.txt"), "r") as f:
    sentences: List[str] = [line.strip() for line in f if line.strip()]

  topic_classifications: List[str]
  _, topic_classifications = model_topics_with_nmf(sentences)
  for topic in topic_classifications:
    print(parse_topic(topic))
  print(len(set(topic_classifications)))
