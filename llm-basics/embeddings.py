import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")

table = model.wte.weight
print("Embedding matrix shape:", tuple(table.shape))

def vec(word: str) -> torch.Tensor:
    ids = tok.encode(" " + word)
    assert len(ids) == 1
    return table[ids[0]].detach()

v = vec("king")
print("Length of one vector:", len(v))
print("First 8 numbers of 'king':", v[:8].tolist())

def sim(a: str, b: str) -> float:
    return F.cosine_similarity(vec(a), vec(b), dim=0).item()

pairs = [
    ("king", "queen"),
    ("cat", "dog"),
    ("car", "truck"),
    ("king", "banana"),
    ("cat", "democracy"),
    ("car", "banana"),
]

for a, b in pairs:
    print(f"{a:>8} vs {b:<10} similarity = {sim(a, b):.3f}")