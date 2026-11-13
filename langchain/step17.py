import json
from models import get_model

model = get_model()

receipt = "chai point  02/11/26  2 x masala chai + samosa  total Rs 240/-  paid upi"

prompt = f"""Extract merchant, date, amount and category from this receipt.
Reply with JSON only.

Receipt: {receipt}"""

ok = 0
for attempt in range(5):
    text = model.invoke(prompt).content
    print(f"--- attempt {attempt + 1} raw output:\n{text}\n")
    try:
        data = json.loads(text)
        ok += 1
        print("parsed OK:", data)
    except json.JSONDecodeError as e:
        print("PARSE FAILED:", e)

print(f"\n{ok}/5 parsed")