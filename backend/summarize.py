# %%
# Step 1: Summarization (as before)
from transformers import pipeline, SummarizationPipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from collections import defaultdict
import openai  # or your LLM of choice

# %%
# Initialize summarization pipeline
summarizer = pipeline('summarization')

# %%
with open('test.txt', 'r') as file:
  text = file.read()

# %%
# Function to split text into chunks of a specified maximum length
def chunk_text(text: str, max_chunk_size: int = 1000) -> list:
  words = text.split()
  chunks = []

  current_chunk = []
  current_length = 0

  for word in words:
    if current_length + len(word) + 1 <= max_chunk_size:
      current_chunk.append(word)
      current_length += len(word) + 1
    else:
      chunks.append(' '.join(current_chunk))
      current_chunk = [word]
      current_length = len(word) + 1

  if current_chunk:
    chunks.append(' '.join(current_chunk))

  return chunks

# Split the text into smaller chunks
chunks = chunk_text(text, max_chunk_size=1000)

# Summarize each chunk
summaries = [summarizer(chunk, max_length=200, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]

# Combine all summaries into a single summary
intermediate_summary = ' '.join(summaries)
final_summary = summarizer(intermediate_summary, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

print("Final Summary:")
print(final_summary)

# %%
# Step 2: Topic Extraction
vectorizer = CountVectorizer(stop_words='english')
transformer = TfidfTransformer()

X = vectorizer.fit_transform([final_summary])
tfidf_matrix = transformer.fit_transform(X)
feature_names = vectorizer.get_feature_names_out()

# Get the top 5 words as topics
sorted_indices = tfidf_matrix.toarray().sum(axis=0).argsort()[::-1]
top_terms = [feature_names[i] for i in sorted_indices[:5]]
topic = '-'.join(top_terms)
print("Extracted Topic:", topic)

# %%
# Step 3: Prepare the prompt for LLM
prompt = (
  f"The following is a summary of an article:\n\n{final_summary}\n\n"
  f"The main topics are: {topic}\n\n"
  f"Please generate a more detailed and refined topic, and then write an enhanced content summary based on this information."
)

# Step 4: Generate Enhanced Topic and Content using OpenAI's GPT
# You'll need an OpenAI API key for this
openai.api_key = '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'

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",  # or use another model variant
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ],
  max_tokens=500,  # Adjust as needed
  temperature=0.7
)

# Extract the generated text
generated_text = response['choices'][0]['message']['content'].strip()

print("Enhanced Topic and Content:")
print(generated_text)
