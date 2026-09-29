from loader import load_pdf
from chunker import create_chunks
from embeddings import (
    create_embeddings,
    create_query_embedding
)
from vector_store import (
    create_vector_store,
    search_vector_store
)
from gemini_api import generate_answer


def build_rag_system(pdf_path):
    """
    Load PDF, create chunks, embeddings and FAISS index.
    """

    # 1. Load PDF
    text = load_pdf(pdf_path)

    print("Extracted characters:", len(text))

    if not text.strip():
        raise ValueError(
            "No text could be extracted from this PDF. "
            "The PDF may be scanned/image-based."
        )

    # 2. Create chunks
    chunks = create_chunks(text)

    print("Number of chunks:", len(chunks))

    if not chunks:
        raise ValueError(
            "No chunks were created from the PDF."
        )

    # 3. Create embeddings
    embeddings = create_embeddings(chunks)

    print("Embedding shape:", embeddings.shape)

    # 4. Create FAISS index
    index = create_vector_store(embeddings)

    return chunks, index


def ask_question(question, chunks, index, k=3):
    """
    Ask a question using the existing RAG system.
    """

    # 1. Convert question into an embedding
    query_embedding = create_query_embedding(question)

    # 2. Search FAISS
    distances, indices = search_vector_store(
        index,
        query_embedding,
        k
    )

    # 3. Retrieve relevant chunks
    retrieved_chunks = []

    for i in range(k):

        chunk_index = indices[0][i]

        if chunk_index != -1:
            retrieved_chunks.append(
                chunks[chunk_index]
            )

    # 4. Combine retrieved chunks
    context = "\n\n".join(
        retrieved_chunks
    )

    # 5. Create prompt for Gemini
    prompt = f"""
You are a college document assistant.

Answer the user's question using ONLY the information
provided in the context below.

Do not use outside knowledge.

If the answer is not available in the context,
say:

"The answer is not available in the document."

Keep the answer clear and easy to understand.

Context:

{context}

Question:

{question}

Answer:
"""

    # 6. Send prompt to Gemini
    answer = generate_answer(prompt)

    return answer, retrieved_chunks