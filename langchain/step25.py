from langchain_core.tools import tool
from agent_loop import execute, run
from tools import TOOLS

@tool
def flaky_lookup(item: str) -> str:
    """Look up an item in the inventory database."""
    raise RuntimeError("database offline")

ALL_TOOLS = TOOLS + [flaky_lookup]
by_name = {t.name: t for t in ALL_TOOLS}

print("--- failure tests (no model involved) ---")
print(execute({"name": "delete_everything", "args": {}, "id": "1"}, by_name))
print(execute({"name": "get_weather", "args": {"town": "Mumbai"}, "id": "2"}, by_name))
print(execute({"name": "convert_currency", "args": {"amount": "lots", "from_currency": "USD", "to_currency": "INR"}, "id": "3"}, by_name))
print(execute({"name": "flaky_lookup", "args": {"item": "laptop"}, "id": "4"}, by_name))

print("\n--- model tests ---")
for q in [
    "Weather in Mumbai and in London?",
    "Convert 50 USD to EUR, then convert that EUR amount to INR.",
    "Look up the item 'laptop' in the inventory database.",
]:
    print("\nQ:", q)
    print("A:", run(q, ALL_TOOLS))