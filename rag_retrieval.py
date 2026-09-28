from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# ==========================================
# 1. LOAD PDF
# ==========================================

pdf_path = "data/Unit3_SE (1).pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:

    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"


print("PDF loaded successfully.")
print("Total characters:", len(text))


# ==========================================
# 2. CREATE CHUNKS
# ==========================================

chunk_size = 500

chunks = []

for i in range(0, len(text), chunk_size):

    chunk = text[i:i + chunk_size]

    chunks.append(chunk)


print("Total chunks:", len(chunks))


# ==========================================
# 3. LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ==========================================
# 4. CREATE EMBEDDINGS
# ==========================================

print("\nCreating embeddings...")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

print("Embedding shape:", embeddings.shape)


# ==========================================
# 5. CREATE FAISS INDEX
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS index created.")
print("Vectors stored:", index.ntotal)


# ==========================================
# 6. ASK USER QUESTION
# ==========================================

question = input("\nAsk a question about the PDF: ")


# ==========================================
# 7. EMBED USER QUESTION
# ==========================================

query_embedding = model.encode([question])

query_embedding = np.array(query_embedding).astype("float32")


# ==========================================
# 8. SEARCH FAISS
# ==========================================

k = 3

distances, indices = index.search(
    query_embedding,
    k
)


# ==========================================
# 9. GET RETRIEVED CHUNKS
# ==========================================

retrieved_chunks = []

for i in range(k):

    chunk_index = indices[0][i]

    retrieved_chunks.append(chunks[chunk_index])


# ==========================================
# 10. DISPLAY RETRIEVED CHUNKS
# ==========================================

print("\n========================================")
print("MOST RELEVANT CHUNKS")
print("========================================")

for i in range(k):

    chunk_index = indices[0][i]

    print("\n------------------------------")
    print("RESULT", i + 1)
    print("------------------------------")

    print("Distance:", distances[0][i])

    print("\nChunk:")
    print(chunks[chunk_index])


# ==========================================
# 11. COMBINE CHUNKS INTO CONTEXT
# ==========================================

context = "\n\n".join(retrieved_chunks)


# ==========================================
# 12. BUILD RAG PROMPT
# ==========================================

prompt = f"""
You are a college document assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not available in the context,
say that the information is not available in the document.

Context:

{context}

Question:

{question}

Answer:
"""


# ==========================================
# 13. DISPLAY FINAL PROMPT
# ==========================================

print("\n========================================")
print("RAG PROMPT")
print("========================================")

print(prompt)