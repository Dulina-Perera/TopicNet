# %%
from bertopic._bertopic import BERTopic
from bertopic.representation._keybert import KeyBERTInspired
from bertopic.vectorizers._ctfidf import ClassTfidfTransformer
from hdbscan.hdbscan_ import HDBSCAN
from sentence_transformers.SentenceTransformer import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap.umap_ import UMAP

# %%
# Step 1 - Extract embeddings
embedding_model: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")
# embedding_model: SentenceTransformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Step 2 - Reduce dimensionality
umap_model: UMAP = UMAP(
  n_neighbors=15,
  n_components=5,
  metric="cosine",
  min_dist=0.0
)

# Step 3 - Cluster reduced embeddings
hdbscan_model: HDBSCAN = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

# Step 4 - Tokenize topics
vectorizer_model: CountVectorizer = CountVectorizer(stop_words="english")

# Step 5 - Create topic representation
ctfidf_model: ClassTfidfTransformer = ClassTfidfTransformer()

# Step 6 - (Optional) Fine-tune topic representations with 
# a `bertopic.representation` model
representation_model: KeyBERTInspired = KeyBERTInspired()

# All steps together
topic_model: BERTopic = BERTopic(
  embedding_model=embedding_model,          # Step 1 - Extract embeddings
  umap_model=umap_model,                    # Step 2 - Reduce dimensionality
  hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
  vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
  ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
  representation_model=representation_model # Step 6 - (Optional) Fine-tune topic represenations
)
