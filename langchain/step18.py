from typing import Literal
from pydantic import BaseModel, Field
from models import get_model

class Receipt(BaseModel):
    """Data extracted from one receipt."""
    merchant: str = Field(description="Name of the shop or business")
    date: str = Field(description="Purchase date in YYYY-MM-DD format")
    amount: float = Field(description="Total amount paid, as a plain number")
    category: Literal["food", "transport", "shopping", "bills", "other"] = Field(
        description="Best matching spending category"
    )

model = get_model()
structured = model.with_structured_output(Receipt)

receipt = "chai point  02/11/26  2 x masala chai + samosa  total Rs 240/-  paid upi"
result = structured.invoke(f"Extract the data from this receipt:\n{receipt}")

print(type(result))
print(result)
print("amount + 10 =", result.amount + 10)