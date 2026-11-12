import json
import time
import requests
from llm import API_KEY

def timed_call(prompt: str, max_tokens: int = 400):
    start = time.perf_counter()
    first_token_at = None
    input_tokens = output_tokens = 0

    with requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "content-type": "application/json",
        },
        json={
            "model": "openai/gpt-oss-20b",
            "max_tokens": max_tokens,
            "stream": True,
            # Stream options allow us to request usage stats within the stream chunks
            "stream_options": {"include_usage": True}, 
            "messages": [{"role": "user", "content": prompt}],
        },
        stream=True,
        timeout=60,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            
            # Groq/OpenAI ends the stream with standard text data: [DONE]
            if line.strip() == b"data: [DONE]":
                break
                
            if not line.startswith(b"data: "):
                continue
                
            # Load the JSON chunk data payload
            chunk_data = json.loads(line[len(b"data: "):])

            # 1. Track the first valid content token to capture TTFT
            choices = chunk_data.get("choices", [])
            if choices and len(choices) > 0:
                delta = choices[0].get("delta", {})
                if "content" in delta and first_token_at is None:
                    first_token_at = time.perf_counter()

            # 2. Extract final performance token counts out of the usage block
            if "usage" in chunk_data and chunk_data["usage"] is not None:
                input_tokens = chunk_data["usage"]["prompt_tokens"]
                output_tokens = chunk_data["usage"]["completion_tokens"]

    end = time.perf_counter()
    
    # Fallback to prevent crash if a model returns no tokens or fails instantly
    if first_token_at is None:
        first_token_at = end
        
    ttft = first_token_at - start
    gen_time = end - first_token_at
    speed = output_tokens / gen_time if gen_time > 0 else 0
    return input_tokens, output_tokens, ttft, end - start, speed

long_text = "The quick brown fox jumps over the lazy dog. " * 400   # big input

tests = {
    "short question, short answer": "What is 2+2? Reply with just the number.",
    "short question, long answer": "Write a detailed 300-word explanation of how the internet works.",
    "long question, short answer": f"{long_text}\n\nHow many times does the word 'fox' appear above? Reply with just a number.",
}

print(f"{'test':<30}{'in':>7}{'out':>6}{'TTFT':>8}{'total':>8}{'tok/s':>8}")
for name, prompt in tests.items():
    i, o, ttft, total, speed = timed_call(prompt)
    print(f"{name:<30}{i:>7}{o:>6}{ttft:>7.2f}s{total:>7.2f}s{speed:>8.1f}")
