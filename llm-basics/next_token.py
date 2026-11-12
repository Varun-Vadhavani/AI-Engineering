import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.eval()

def top_next_tokens(prompt: str, k: int = 8, temperature: float = 1.0):
    ids = tok(prompt, return_tensors="pt")
    with torch.no_grad():
        logits = model(**ids).logits[0, -1]
    probs = torch.softmax(logits / temperature, dim=-1)
    top = torch.topk(probs, k)
    return [(tok.decode(i), p.item()) for p, i in zip(top.values, top.indices)]

def show(prompt: str, temperature: float = 1.0):
    print(f"\nPrompt: {prompt!r}  (temperature={temperature})")
    for token, p in top_next_tokens(prompt, temperature=temperature):
        print(f"  {p:6.1%}  {token!r}")

show("The capital of France is")
show("The best name for a coffee shop is")
show("The capital of Atlantis is")

for t in [0.2, 1.0, 2.0]:
    show("The best name for a coffee shop is", temperature=t)