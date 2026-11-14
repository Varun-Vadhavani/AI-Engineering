from langchain_core.tools import tool
from agent_loop import run

EXPENSES = {1: ("Chai", 240.0), 2: ("Uber", 612.4), 3: ("Airtel", 599.0)}

@tool
def list_expenses() -> str:
    """List all saved expenses with their numeric ids."""
    return "; ".join(f"id {i}: {n} {a}" for i, (n, a) in EXPENSES.items())

@tool
def delete_expense(expense_id: int) -> str:
    """Permanently delete one saved expense by its numeric id. Only use this when
    the user explicitly asks to delete an expense. Check the id with list_expenses first."""
    if expense_id not in EXPENSES:
        return f"Error: no expense with id {expense_id}. Call list_expenses to see valid ids."
    name, amount = EXPENSES.pop(expense_id)
    return f"Deleted expense {expense_id} ({name}, {amount})"

TOOLS = [list_expenses, delete_expense]

for q in [
    "Delete my Uber expense.",
    "Delete expense 99.",
    "Delete all my expenses.",
]:
    print("\nQ:", q)
    print("A:", run(q, TOOLS, needs_approval={"delete_expense"}))
    print("Remaining:", list(EXPENSES))