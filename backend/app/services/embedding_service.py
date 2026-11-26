from google import genai

from app.core.configure import settings


class EmbeddingService:
    MODEL_NAME = "gemini-embedding-001"

    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def create_embedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot create an embedding for empty text."
            )

        response = self.client.models.embed_content(
            model=self.MODEL_NAME,
            contents=text,
        )

        return response.embeddings[0].values

    def create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        response = self.client.models.embed_content(
            model=self.MODEL_NAME,
            contents=texts,
        )

        return [
            embedding.values
            for embedding in response.embeddings
        ]