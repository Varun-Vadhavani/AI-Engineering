import re
import time
from pydantic import ValidationError
from models import get_model
from schemas import Receipt

# (receipt text, expected merchant, date, amount, category)
CASES = [
    ("chai point  02/11/26  2 x masala chai + samosa  total Rs 240/-  paid upi",
     "chai point", "2026-11-02", 240.0, "food"),
    ("SWIGGY ORDER #88213 | 12 Nov 2026 | Biryani 1x 349.00 | Delivery 25 | GST 15.50 | Grand Total ₹389.50",
     "swiggy", "2026-11-12", 389.50, "food"),
    ("Uber trip 5th Nov 2026 Airport to Navrangpura fare 612.40 INR",
     "uber", "2026-11-05", 612.40, "transport"),
    ("Reliance Digital\n2026-10-28\nUSB cable 299\nMouse 799\nSubtotal 1098\nGST 18% 197.64\nTOTAL 1295.64",
     "reliance digital", "2026-10-28", 1295.64, "shopping"),
    ("Torrent Power electricity bill Oct 2026, due 15/11/2026, amount payable Rs. 1,842.00, paid on 03-11-2026",
     "torrent power", "2026-11-03", 1842.0, "bills"),
    ("d-mart 30/10/26 groceries: rice 520 oil 310 milk 66 .... total 896 (cash)",
     "dmart", "2026-10-30", 896.0, "food"),
    ("Ola cab 9/11/26 rs 187 ride to station",
     "ola", "2026-11-09", 187.0, "transport"),
    ("Cafe Coffee Day  Nov 7  2026  cappuccino 180 + brownie 150 = 330 total incl tax",
     "cafe coffee day", "2026-11-07", 330.0, "food"),
    ("Airtel postpaid bill 01-11-2026 amount 599 paid via card",
     "airtel", "2026-11-01", 599.0, "bills"),
    ("Amazon.in order 21 Oct 2026 earphones ₹1,499 (discount -200) you paid 1299",
     "amazon", "2026-10-21", 1299.0, "shopping"),
]

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

structured = get_model().with_structured_output(Receipt)

valid_correct = valid_wrong = invalid = 0

for i, (text, exp_m, exp_d, exp_a, exp_c) in enumerate(CASES, 1):
    try:
        r = structured.invoke(f"Extract the data from this receipt:\n{text}")
    except Exception as e:
        invalid += 1
        print(f"Q{i}: INVALID  ({type(e).__name__})")
        time.sleep(1)
        continue

    problems = []
    if norm(exp_m) not in norm(r.merchant): problems.append(f"merchant={r.merchant!r}")
    if r.date != exp_d:                     problems.append(f"date={r.date} (expected {exp_d})")
    if abs(r.amount - exp_a) > 0.01:        problems.append(f"amount={r.amount} (expected {exp_a})")
    if r.category != exp_c:                 problems.append(f"category={r.category} (expected {exp_c})")

    if problems:
        valid_wrong += 1
        print(f"Q{i}: VALID BUT WRONG -> " + "; ".join(problems))
    else:
        valid_correct += 1
        print(f"Q{i}: valid and correct")
    time.sleep(1)   # be gentle with free-tier rate limits

print(f"\nvalid and correct: {valid_correct}/10")
print(f"valid but wrong:   {valid_wrong}/10")
print(f"invalid/failed:    {invalid}/10")