from sentence_transformers import SentenceTransformer

from app.core.configure import settings


class EmbeddingService:
    def __init__(self):
        self.model_name = settings.embedding_model
        self.model = SentenceTransformer(self.model_name)

    def create_embedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot create an embedding for empty text."
            )

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings.tolist()