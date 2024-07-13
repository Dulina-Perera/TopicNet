# %%
import numpy as np
import pandas as pd
import spacy

from bertopic._bertopic import BERTopic
from IPython.display import display
from sentence_transformers.SentenceTransformer import SentenceTransformer
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from typing import Dict, List

# %%
# Load SpaCy model.
nlp: English = spacy.load("en_core_web_lg")

# Read the text file.
with open("text.txt", mode="r", encoding="utf-8") as file:
  text: str = file.read()

# Process the text with SpaCy.
doc: Doc = nlp(text)

# Extract sentences and their embeddings.
data: List[Dict] = []
for sent in doc.sents:
  data.append({
    "sentence": sent.text,
    "embedding": sent.vector.tolist()  # Convert the embedding to a list for better storage compatibility.
  })

# Create a DataFrame.
df: pd.DataFrame = pd.DataFrame(data)
display(df.head())

# Save DataFrame to a Parquet file.
df.to_parquet("sentences_embeddings.parquet", engine="pyarrow")
