from app.rag.vector_store import VectorStore
from app.services.embedding_service import EmbeddingService


embedding_service = EmbeddingService()
vector_store = VectorStore()

text = """
The SmartLogix application loads a trained machine learning
model using joblib and uses it to classify customer complaints.
"""

embedding = embedding_service.create_embedding(text)

chunk = {
    "path": "app.py",
    "extension": ".py",
    "language": "python",
    "chunk_index": 999,
    "content": text,
}

vector_store.add_chunks(
    chunks=[chunk],
    embeddings=[embedding],
)

print("Chunk added to Chroma successfully!")

results = vector_store.search(
    query_embedding=embedding,
    top_k=1,
)

print("Search completed!")
print(results)