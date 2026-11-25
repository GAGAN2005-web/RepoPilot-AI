from app.services.ingestion_service import IngestionService
from app.services.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


async def main():
    owner = "GAGAN2005-web"
    repository = "SmartLogix-AI"
    branch = "main"

    # Step 1: Get repository chunks
    ingestion_service = IngestionService()

    chunks = await ingestion_service.get_repository_chunks(
        owner=owner,
        repository=repository,
        branch=branch,
    )

    print(f"Total chunks: {len(chunks)}")

    # Step 2: Create embeddings
    embedding_service = EmbeddingService()

    texts = [chunk["content"] for chunk in chunks]

    embeddings = embedding_service.create_embeddings(texts)

    print(f"Total embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")

    # Step 3: Store everything in Chroma
    vector_store = VectorStore()

    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        repository_id=1,
    )

    print("Repository indexed successfully!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())