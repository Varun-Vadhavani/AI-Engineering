import base64
import io
import requests
from PIL import Image
from llm import API_KEY

URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "qwen/qwen3.8-27b"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def count_with_image(img: Image.Image, question: str) -> int:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode("ascii")
    body = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{data}"},
                },
            ],
        }],
        "max_completion_tokens": 1,
    }
    response = requests.post(URL, headers=HEADERS, json=body, timeout=30)
    response.raise_for_status()
    return response.json()["usage"]["prompt_tokens"]


question = "Describe this chart."

with Image.open("chart.png") as original:
    print(f"{'size':>12}{'pixels':>10}{'prompt tokens':>15}")
    for width in [1200, 600, 300, 150]:
        height = int(original.height * width / original.width)
        img = original.resize((width, height))
        tokens = count_with_image(img, question)
        print(f"{width}x{height:<6}{width * height:>10}{tokens:>15}")