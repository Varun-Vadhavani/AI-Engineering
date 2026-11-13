from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class Receipt(BaseModel):
    """Data extracted from one receipt."""
    merchant: str = Field(min_length=1, description="Name of the shop or business")
    date: str = Field(description="Date the purchase was made or paid, as YYYY-MM-DD")
    amount: float = Field(gt=0, description="Final total actually paid, as a plain number")
    category: Literal["food", "transport", "shopping", "bills", "other"] = Field(
        description="food = restaurants, cafes and groceries; transport = cabs, fuel, travel; "
                    "shopping = goods; bills = utilities, phone, rent; other = anything else"
    )

    @field_validator("date")
    @classmethod
    def date_must_be_real_and_not_future(cls, v):
        try:
            d = datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("date must be a real calendar date in YYYY-MM-DD format")
        if d > date.today():
            raise ValueError("date is in the future")
        return v