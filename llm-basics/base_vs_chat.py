from transformers import AutoTokenizer, AutoModelForCausalLM
from llm import ask

tok = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

prompt = "Explain what an Python is in one sentence."

ids = tok(prompt, return_tensors="pt")

out = model.generate(
    **ids, max_new_tokens=40, do_sample=False, pad_token_id=tok.eos_token_id
)

print("BASE MODEL (GPT-2):")
print(tok.decode(out[0]), "\n")