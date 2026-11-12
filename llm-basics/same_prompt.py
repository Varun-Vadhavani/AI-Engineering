import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["FREE_API_KEY"]

def ask(prompt: str, max_tokens: int = 100) -> str:
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
    return response.json()["choices"][0]["message"]["content"].strip()

prompt = "Suggest one name for a coffee shop. Reply with just the name."

for i in range(5):
    print(f"Run {i + 1}: {ask(prompt)}")