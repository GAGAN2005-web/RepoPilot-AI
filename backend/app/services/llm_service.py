import httpx


class LLMService:
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "qwen2.5-coder:3b"

    async def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        payload = {
            "model": self.MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.OLLAMA_URL,
                    json=payload,
                )

            response.raise_for_status()

            data = response.json()

            return data["response"]

        except httpx.TimeoutException:
            raise RuntimeError("Ollama request timed out.")

        except httpx.HTTPError as exc:
            raise RuntimeError(
                f"Failed to communicate with Ollama: {exc}"
            )