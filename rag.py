def build_rag_system(pdf_path):
    """
    Load PDF, create chunks, embeddings and FAISS index.
    """

    # 1. Load PDF
    text = load_pdf(pdf_path)

    print("Extracted characters:", len(text))

    # Check if PDF contains extractable text
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