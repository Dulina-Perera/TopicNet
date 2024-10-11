# %%
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from typing import List, Tuple

# %%
def cvt_corpus_to_bow_fmt(corpus: List[str]) -> Tuple[List[List[Tuple[int, int]]], Dictionary]:
  """
	Convert a corpus of documents to bag-of-words format.

	Parameters:
	- corpus: List of documents

	Returns:
	- Tuple containing the bag-of-words representation of the corpus and the dictionary
  """
  # Associate each unique word in the corpus with a unique integer ID.
  dictionary: Dictionary = Dictionary(corpus)

  # Convert the corpus to bag-of-words format.
  bow_vectors: List[List[Tuple[int, int]]] = [dictionary.doc2bow(doc) for doc in corpus]

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
