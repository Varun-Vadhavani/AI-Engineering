from langchain_core.messages import HumanMessage, ToolMessage
from models import get_model
from tools import TOOLS

tools_by_name = {t.name: t for t in TOOLS}
model = get_model().bind_tools(TOOLS)

def run(question):
    messages = [HumanMessage(content=question)]

    # Move 1: the model answers or asks for tools
    ai = model.invoke(messages)
    messages.append(ai)                      # keep the model's request in the history

    if not ai.tool_calls:                    # no tool needed: this IS the final answer
        return ai.content, messages

    # Move 2 + 3: run each tool and send each result back with the matching id
    for call in ai.tool_calls:
        print(f"  running {call['name']}({call['args']})  id={call['id']}")
        result = tools_by_name[call["name"]].invoke(call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    # Move 4: the model reads the results and writes the final answer
    final = model.invoke(messages)
    messages.append(final)
    return final.content, messages

for q in [
    "What's the weather in Mumbai?",
    "What's the weather in Mumbai, and how much is 100 USD in INR?",
    "Tell me a short joke.",
]:
    print("\nQ:", q)
    answer, messages = run(q)
    print("A:", answer)
    print("  message types:", [type(m).__name__ for m in messages])