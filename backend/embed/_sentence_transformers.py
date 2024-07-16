import torch

from backend.embed._base import BaseEmbedder
from backend.embed._no_sentences_to_encode_error import NoSentencesToEncodeError
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from torch import Tensor
from typing import List, Union


class SentenceTransformersEmbedder(BaseEmbedder):
		def __init__(self, model: Union[str, None] = None) -> None:
			super().__init__()

			try:
				if isinstance(model, SentenceTransformer):
					self.model = model
				elif isinstance(model, str):
					self.model = SentenceTransformer(
       			model_name_or_path=model,
						device='cuda' if torch.cuda.is_available() else 'cpu'
        	)
				else:
					raise
			except Exception as e:
				self.logger.warning(f'Invalid SentenceTransformer model definition: {model}.')

				# Fallback to the default model.
				self.model = SentenceTransformer(
					'all-mpnet-base-v2',
					device='cuda' if torch.cuda.is_available() else 'cpu'
				)
			finally:
				self.logger.info(f'Initialize SentenceTransformer model: {self.model}.')


		def embed(self, sentences: List[str]) -> ndarray | Tensor | List[Tensor]:
			try:
				if not sentences:
					raise NoSentencesToEncodeError()

				embeddings: ndarray | Tensor | List[Tensor] = self.model.encode(
      		sentences,
					show_progress_bar=True
        )
				self.logger.info('Embed sentences.')

				return embeddings
			except NoSentencesToEncodeError as e:
				self.logger.warning(e)
				return []
			except Exception as e:
				self.logger.error(f'Unexpected error: {e}.')
				return []
