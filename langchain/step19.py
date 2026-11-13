from pydantic import ValidationError
from schemas import Receipt

# 1) Invalid: should be rejected
try:
    Receipt(merchant="Shop", date="2026-13-45", amount=-5, category="food")
except ValidationError as e:
    print("REJECTED:")
    print(e)

# 2) Wrong category word: should be rejected
try:
    Receipt(merchant="Shop", date="2026-11-02", amount=240, category="groceries")
except ValidationError as e:
    print("\nREJECTED:", e.errors()[0]["msg"])

# 3) Valid but WRONG: the real receipt said 240 on 2026-11-02
r = Receipt(merchant="Chai Point", date="2025-01-01", amount=9999, category="food")
print("\nACCEPTED (but wrong!):", r)