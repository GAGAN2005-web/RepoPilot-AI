from app.services.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.context_builder import build_context


def main():
    query = "Where is the machine learning model loaded?"

    embedding_service = EmbeddingService()

    query_embedding = embedding_service.create_embedding(query)

    vector_store = VectorStore()

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
        repository_id=1,
    )

    context = build_context(results)

    print("\nGenerated Context:")
    print("=" * 80)
    print(context)


if __name__ == "__main__":
    main()