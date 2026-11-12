from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("gpt2")
total = sum(p.numel() for p in model.parameters())
print(f"GPT-2 parameters: {total:,}")

emb = model.transformer.wte.weight.numel()
print(f"Of which the token embedding table: {emb:,} ({emb / total:.0%})")

# Memory needed just to hold the weights
for name, bytes_per_param in [("fp32", 4), ("fp16", 2), ("4-bit", 0.5)]:
    for size_b in [8, 70]:
        gb = size_b * 1e9 * bytes_per_param / 1e9
        print(f"{size_b}B model in {name}: ~{gb:.0f} GB")