from llm import ask_full

TASKS = {
    "EXTRACTION": (
        "Invoice INV-2026-0417, dated 12 October 2026, issued to Meridian Traders Pvt Ltd. "
        "Total due: 48,250 INR.\n\n"
        "Extract the invoice number and total as JSON with keys invoice_no and total. "
        "Output only the JSON."
    ),
    "CREATIVE": "Suggest a name and a one-line tagline for a new coffee shop. Reply in one line.",
}

for task, prompt in TASKS.items():
    for temp in [0.0, 1.0]:
        outputs = [ask_full(prompt, max_tokens=80, temperature=temp)[0] for _ in range(5)]
        print(f"\n{task} | temperature={temp} | unique outputs: {len(set(outputs))}/5")
        for o in outputs:
            print(f"   {o}")