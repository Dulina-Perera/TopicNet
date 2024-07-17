import logging
import torch

from abc import ABC, abstractmethod
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from typing import Any, List, Union

from _3_embed._error import NoSentencesToEncodeError


class BaseEmbedder(ABC):
	def __init__(self, model: Any = None) -> None:
		self.logger: logging.Logger = logging.getLogger(__name__)
		self.model: Any = model


	@abstractmethod
	def embed(self, sentences: List[str]) -> ndarray:
		pass


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


		def embed(self, sentences: List[str]) -> ndarray:
			embeddings: ndarray = self.model.encode(
      		sentences,
					show_progress_bar=True
        )
			self.logger.info('Embed sentences.')

			return embeddings
