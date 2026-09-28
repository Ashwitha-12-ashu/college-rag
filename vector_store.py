import faiss


def create_vector_store(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_vector_store(index, query_embedding, k=3):

    distances, indices = index.search(
        query_embedding,
        k
    )

    return distances, indices