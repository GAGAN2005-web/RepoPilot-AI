from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

text = """
SmartLogix AI classifies customer logistics complaints
using a machine learning model.
"""

embedding = service.create_embedding(text)

print("Embedding created successfully!")
print(f"Model: {service.model_name}")
print(f"Dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")