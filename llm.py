import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["FREE_API_KEY"]

def ask(prompt: str, max_tokens: int = 2048) -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-oss-20b",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 1.0,
        },
        timeout=30,
    )
    response.raise_for_status()
    choice = response.json()["choices"][0]
    content = choice["message"].get("content")
    if not isinstance(content, str) or not content.strip():
        finish_reason = choice.get("finish_reason", "unknown")
        raise RuntimeError(
            f"Model returned no answer (finish_reason={finish_reason!r})."
        )
    return content.strip()