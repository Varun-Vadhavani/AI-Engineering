import requests
from transformers import AutoTokenizer
from llm import API_KEY  # Assuming your Groq API key is stored here

# 1. Load the tokenizer for the specific model locally
# This downloads the vocabulary file (~4MB) once and caches it locally
tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-20b")

def count_groq_style_local(text: str) -> int:
    """Counts tokens locally using the model's tokenizer."""
    return len(tokenizer.encode(text))

def count_groq_api(text: str) -> int:
    """Counts tokens by asking the Groq API server directly."""
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-oss-20b",
            "messages": [{"role": "user", "content": text}],
            "max_tokens": 1,  # Stop immediately to save cost and time
        },
        timeout=30,
    )
    response.raise_for_status()
    # Groq returns standard OpenAI-format usage statistics
    return response.json()["usage"]["prompt_tokens"]

samples = {
    "English": "Our delivery service is available in more than fifty cities. Orders placed before noon are delivered the same day, and you can track your package in real time from the app.",
    "Hindi": "हमारी डिलीवरी सेवा पचास से अधिक शहरों में उपलब्ध है। दोपहर से पहले दिए गए ऑर्डर उसी दिन डिलीवर कर दिए जाते हैं, और आप ऐप से अपने पैकेज को रियल टाइम में ट्रैक कर सकते हैं।",
    "Code": "def total(items):\n    result = 0\n    for item in items:\n        if item['price'] > 0:\n            result += item['price'] * item['qty']\n    return result\n",
    "Numbers": ", ".join(str(n) for n in [48213, 90175, 33481, 70256, 12904, 85632, 40719, 66348, 29057, 51893, 77420, 18366]),
}

print(f"{'sample':<10}{'chars':>7}{'local_tok':>12}{'groq_api':>10}")
for name, text in samples.items():
    print(f"{name:<10}{len(text):>7}{count_groq_style_local(text):>12}{count_groq_api(text):>10}")
