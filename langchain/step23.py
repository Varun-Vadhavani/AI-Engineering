from models import get_model
from tools import TOOLS

model = get_model().bind_tools(TOOLS)

for question in [
    "What's the weather in Ahmedabad?",
    "How much is 5000 INR in USD?",
    "Tell me a short joke.",
]:
    response = model.invoke(question)
    print("Q:", question)
    print("  content:   ", repr(response.content))
    print("  tool_calls:", response.tool_calls)
    print()