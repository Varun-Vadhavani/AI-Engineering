from models import get_model
from schemas import Receipt

class ExtractionError(Exception):
    pass

# include_raw=True: instead of crashing on bad output, we get a dict back with
# "parsed" (the Receipt or None) and "parsing_error" (what went wrong, or None)
structured = get_model().with_structured_output(Receipt, include_raw=True)

def extract_receipt(text, max_retries=2):
    base = f"Extract the data from this receipt:\n{text}"
    prompt = base
    last_error = None

    for attempt in range(1, max_retries + 2):          # first try + retries
        result = structured.invoke(prompt)

        if result["parsed"] is not None:               # CHECK passed
            print(f"  attempt {attempt}: valid")
            return result["parsed"]

        last_error = str(result["parsing_error"])[:500]
        print(f"  attempt {attempt}: INVALID -> {last_error.splitlines()[0]}")

        # DECIDE: repair. Tell the model exactly what was wrong.
        prompt = (f"{base}\n\nYour previous answer was rejected: {last_error}\n"
                  "Return corrected data that fixes this problem.")

    # DECIDE: give up with a clear error
    raise ExtractionError(
        f"No valid data after {max_retries + 1} attempts. Last error: {last_error}"
    )

TESTS = {
    "normal":      "chai point  02/11/26  2 x masala chai + samosa  total Rs 240/-  paid upi",
    "future date": "chai point  02/11/2027  2 x masala chai  total Rs 240/-",
    "no data":     "Thank you for shopping with us! Have a great day.",
}

for name, text in TESTS.items():
    print(f"\n[{name}]")
    try:
        print("  RESULT:", extract_receipt(text))
    except ExtractionError as e:
        print("  REJECTED:", e)