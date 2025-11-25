import logging
import requests
from app.config import settings

class LLMClient:
    def ask(self, question: str) -> str:
        if settings.LLM_PROVIDER == "ollama":
            return self.ask_ollama(question)
        else:
            return "Provider not implemented yet."

    def ask_ollama(self, question: str):
        url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": question,
            "temperature": settings.LLM_TEMPERATURE,
            "stream": False,
        }
        response = requests.post(url, json=payload)
        # logging.info(f"LLM Response Status: {response.status_code}, Content: {response.text}")
        return response.json().get("response", "")

llm_client = LLMClient()
