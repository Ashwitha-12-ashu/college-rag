import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Example document chunks
# -----------------------------

chunks = [
    "Students must maintain a minimum attendance of 75%.",
    "The examination timetable will be announced later.",
    "Students with insufficient attendance may not be eligible to write examinations.",
    "The library is open from 9 AM to 6 PM.",
    "Students must carry their identity card during examinations."
]


# -----------------------------
# 3. Create embeddings
# -----------------------------

embeddings = model.encode(chunks)

print("Embedding shape:", embeddings.shape)


# -----------------------------
# 4. Convert embeddings to NumPy
# -----------------------------

embeddings = np.array(embeddings).astype("float32")


# -----------------------------
# 5. Create FAISS index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)


# -----------------------------
# 6. Add embeddings to FAISS
# -----------------------------

index.add(embeddings)

print("Number of vectors in FAISS:", index.ntotal)


# -----------------------------
# 7. User question
# -----------------------------

question = "What is the minimum attendance required?"


# -----------------------------
# 8. Convert question to embedding
# -----------------------------

query_embedding = model.encode([question])

query_embedding = np.array(query_embedding).astype("float32")


# -----------------------------
# 9. Search
# -----------------------------

k = 2

distances, indices = index.search(query_embedding, k)


# -----------------------------
# 10. Display results
# -----------------------------

print("\nQuestion:", question)

print("\nMost relevant chunks:")

for i in range(k):
    chunk_index = indices[0][i]

    print("\nResult", i + 1)
    print("Chunk:", chunks[chunk_index])
    print("Distance:", distances[0][i])