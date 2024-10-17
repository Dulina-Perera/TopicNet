# %%
import os
import pytextrank
import spacy

from openai import AsyncOpenAI
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from typing import Optional

from ....core_ import is_valid_openai_model
from ....exceptions_ import InvalidOpenAIModelError

# %%
def summarize_using_spacy(text: str) -> str:
  """
	Summarize the given text using SpaCy and TextRank.

	:param text: The text to summarize
	:type text: str

	:returns: The summarized text
	:rtype: str
  """
	# Load spaCy model and add the pytextrank pipe.
  nlp: English = spacy.load("en_core_web_md")
  nlp.add_pipe("textrank")

  # Process the document with SpaCy.
  doc: Doc = nlp(text)

  # Rank the sentences instead of phrases.
  summary: str = ""
  for sent in doc._.textrank.summary(limit_phrases=5, limit_sentences=5):
    summary += str(sent) + " "

  return summary


async def refine_summary_using_openai(summary: str, model: Optional[str] = "gpt-4o-mini") -> str:
  """
	Refine the given summary using OpenAI models.

	:param summary: The summary to refine
	:type summary: str

	:param model: The OpenAI model to use, defaults to "gpt-4o"
	:type model: str, optional

	:returns: The refined summary
	:rtype: str
 	"""
  if not await is_valid_openai_model(model):
    raise InvalidOpenAIModelError(model)

  # Initialize the OpenAI client.
  client: AsyncOpenAI = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  # Define the prompt.
  system_prompt: str = (
		f"You are a helpful assistant."
		f"You will be provided with an extractive summary of a document."
		f"Please generate a detailed and refined topic, and then enhance the summary to make it more concise and coherent."
		f"The output should be a markdown-formatted summary in the following format: \"<your summary>\"."
	)
  user_prompt: str = summary

  # Generate the refined content.
  response: str = await client.chat.completions.create(
		model=model,
		messages=[
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": user_prompt}
		],
		max_tokens=1000,
		temperature=0.3
	)

  # Return the refined content.
  return response.choices[0].message.content
