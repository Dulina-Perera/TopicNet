import logging

from numpy import ndarray
from typing import List

from backend._3_embed._embedder import BaseEmbedder
from backend._3_embed._error import NoSentencesToEncodeError


def extract_embeddings(
  model: BaseEmbedder,
  sentences: List[str],
  logger: logging.Logger
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
