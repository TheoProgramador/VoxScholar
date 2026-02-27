import os
import requests

class GroqChat:
    def __init__(self, api_key: str | None = None, model: str = "openai/gpt-oss-120b"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("Defina GROQ_API_KEY no ambiente.")
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"

    def chat(self, messages: list[dict], temperature: float = 0.3, max_tokens: int = 400) -> str:
        r = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        return (data["choices"][0]["message"].get("content") or "").strip()