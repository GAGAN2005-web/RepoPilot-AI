from app.services.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


def main():
    query = "Where is the machine learning model loaded?"

    # Create embedding for the user's question
    embedding_service = EmbeddingService()

    query_embedding = embedding_service.create_embedding(query)

    # Search only inside repository ID 1
    vector_store = VectorStore()

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
        repository_id=1,
    )

    print("\nQuery:")
    print(query)

    print("\nRetrieved chunks:")
    print("=" * 80)

    for i in range(len(results["documents"][0])):
        print(f"\nResult {i + 1}")
        print("-" * 80)

        metadata = results["metadatas"][0][i]

        print(f"Repository ID: {metadata['repository_id']}")
        print(f"Path: {metadata['path']}")
        print(f"Language: {metadata['language']}")
        print(f"Chunk Index: {metadata['chunk_index']}")
        print(f"Distance: {results['distances'][0][i]}")

        print("\nContent:")
        print(results["documents"][0][i])


if __name__ == "__main__":
    main()