from google import genai

from app.core.configure import settings


class EmbeddingService:
    MODEL_NAME = "gemini-embedding-001"
    BATCH_SIZE = 100

    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=settings.gemini_api_key)

    def create_embedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        response = self.client.models.embed_content(
            model=self.MODEL_NAME,
            contents=text,
        )

        return response.embeddings[0].values

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = []

        for start in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[start:start + self.BATCH_SIZE]

            response = self.client.models.embed_content(
                model=self.MODEL_NAME,
                contents=batch,
            )

            embeddings.extend(
                embedding.values
                for embedding in response.embeddings
            )

        return embeddings