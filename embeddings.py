from sentence_transformers import SentenceTransformer
import numpy as np


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================
# CREATE EMBEDDINGS FOR DOCUMENT CHUNKS
# ==========================================

def create_embeddings(chunks):

    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings).astype("float32")

    return embeddings


# ==========================================
# CREATE EMBEDDING FOR USER QUESTION
# ==========================================

def create_query_embedding(question):

    query_embedding = model.encode([question])

    query_embedding = np.array(query_embedding).astype("float32")

    return query_embedding