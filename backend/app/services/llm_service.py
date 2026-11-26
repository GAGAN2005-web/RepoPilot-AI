from google import genai

from app.core.configure import settings


class LLMService:
    MODEL_NAME = "gemini-3.5-flash-lite"

    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.client.models.generate_content(
                model=self.MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as exc:
            raise RuntimeError(
                f"Failed to communicate with Gemini: {exc}"
            )