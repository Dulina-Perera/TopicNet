# backend/mindmap-generation/api/v1/services/summarize.py

# %%
import os
import re
import spacy

from re import Match
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from typing import Any, Union

# %%
def summarize_using_spacy(text: str) -> str:
	# Load spaCy model and add the pytextrank pipe.
	nlp: English = spacy.load('en_core_web_lg')
	nlp.add_pipe('textrank')

	# Process the document using spaCy.
	doc: Doc = nlp(text)

	# Rank the sentences instead of phrases.
	summary: str = ''
	for sent in doc._.textrank.summary(limit_phrases=5, limit_sentences=5):
		summary += str(sent) + ' '

	return summary


def refine_summary_using_llm(summary: str) -> str:
  prompt: str = (
    f"The following is an extractive summary of a document: {summary}\n\n"
    f"Please refine the summary to make it more concise and coherent.\n\n"
    f"Format your response as follows: \"Refined summary: <your summary>\"."
  )

  client: OpenAI = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

  response: ChatCompletion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
    ],
    max_tokens=500,
    temperature=0.7
  )
  refined_summary: str = response.choices[0].message.content

  match: Union[Match[str], None] = re.search(
    r'Refined summary:\s*(.*)',
    refined_summary,
    re.DOTALL
  )
  if match:
    refined_summary = match.group(1).strip()
    return refined_summary
  else:
    raise ValueError("Response is not in the expected 'Refined summary: <your summary>' format.")
