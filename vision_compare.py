import base64
import sys
import time
import requests
from llm import API_KEY

sys.stdout.reconfigure(errors="replace")

URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "qwen/qwen3.8-27b"
REQUEST_INTERVAL_SECONDS = 20
MAX_ATTEMPTS = 5
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def call(
    content: list[dict[str, object]], max_tokens: int = 300
) -> tuple[str, int, int]:
    for attempt in range(MAX_ATTEMPTS):
        r = requests.post(
            URL,
            headers=HEADERS,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": content}],
                "max_completion_tokens": max_tokens,
            },
            timeout=60,
        )
        if r.status_code != 429 or attempt == MAX_ATTEMPTS - 1:
            break
        retry_after = r.headers.get("Retry-After")
        try:
            delay = (
                float(retry_after)
                if retry_after is not None
                else REQUEST_INTERVAL_SECONDS
            )
        except ValueError:
            delay = REQUEST_INTERVAL_SECONDS
        delay = min(max(delay, REQUEST_INTERVAL_SECONDS), 60)
        print(f"Rate limited; retrying in {delay:g}s...", flush=True)
        time.sleep(delay)

    r.raise_for_status()
    data = r.json()
    choice = data["choices"][0]
    answer = choice["message"].get("content")
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError(
            f"Model returned no answer (finish_reason={choice.get('finish_reason', 'unknown')!r})."
        )
    usage = data["usage"]
    return answer.strip(), usage["prompt_tokens"], usage["completion_tokens"]

with open("chart.png", "rb") as f:
    image_b64 = base64.standard_b64encode(f.read()).decode()

IMAGE_PART = {
    "type": "image_url",
    "image_url": {"url": f"data:image/png;base64,{image_b64}"},
}

# What "extracted text" from the chart looks like
TEXT_PART = {
    "type": "text",
    "text": "Chart: Monthly Sales (units)\nJan: 120\nFeb: 135\nMar: 128\nApr: 160\nMay: 182\nJun: 175",
}

questions = [
    "Which month had the highest sales? Answer in one short sentence.",
    "What were the sales in April? Reply with only the number.",
    "What were the total sales across all six months? Reply with only the number.",
]

total_calls = len(questions) * 2
completed_calls = 0

for q in questions:
    print(f"\nQ: {q}")
    for label, part in [("IMAGE", IMAGE_PART), ("TEXT ", TEXT_PART)]:
        answer, tin, tout = call([part, {"type": "text", "text": q}])
        print(f"  {label} | in={tin:>5} out={tout:>3} | {answer.strip()}")
        completed_calls += 1
        if completed_calls < total_calls:
            time.sleep(REQUEST_INTERVAL_SECONDS)