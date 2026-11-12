import json

message = {"role": "user", "content": "Hello"}
messages = [message]

messages.append({"role": "assistant", "content": "Hi! How can I help?"})

topic = "RAG"
prompt = f"Explain {topic} in one sentence."

def build_prompt(topic: str, audience: str = "beginner") -> str:
    return f"Explain {topic} to a {audience}."

contents = [m["content"] for m in messages]

as_text = json.dumps(messages, indent=2)
back_to_dict = json.loads(as_text)

try:
    value = {"a": 1}["b"]
except KeyError as e:
    print(f"Missing key: {e}")

print(build_prompt(topic))
print(contents)
print(as_text)