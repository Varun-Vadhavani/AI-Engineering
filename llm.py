import os
import base64

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("FREE_API_KEY")


def ask(prompt: str, max_tokens: int = 2048) -> str:
    if not API_KEY:
        raise RuntimeError("FREE_API_KEY is not set. Add it to your .env file.")

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


def ask_image(path: str, prompt: str, max_tokens: int = 100):
    if not API_KEY:
        raise RuntimeError("FREE_API_KEY is not set. Add it to your .env file.")

    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode()

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen/qwen3.8-27b",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{data}"},
                        },
                    ],
                }
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    d = response.json()
    content = d["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    return content.strip(), d.get("usage", {}).get("prompt_tokens", 0)
