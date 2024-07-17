import nltk

from logging import Logger
from nltk.tokenize.punkt import PunktSentenceTokenizer
from pathlib import Path
from typing import List, Union


def extract_sentences_from_cleaned_text(
  path: Union[str, Path],
  logger: Logger
) -> List[str]:
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
