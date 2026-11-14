from langchain_core.messages import HumanMessage, ToolMessage
from models import get_model

MAX_STEPS = 5   # safety cap so the model can't loop forever

def execute(call, tools_by_name, needs_approval=()):
    """Run ONE tool request and always return a string for the model."""
    name, args = call["name"], call["args"]

    tool = tools_by_name.get(name)
    if tool is None:
        return f"Error: unknown tool '{name}'. Available tools: {', '.join(tools_by_name)}"

    if name in needs_approval:
        answer = input(f"  APPROVE {name}({args})? [y/N] ").strip().lower()
        if answer != "y":
            return "The user declined this action. Do not retry it."

    try:
        return str(tool.invoke(args))
    except Exception as e:
        return f"Error running {name}: {type(e).__name__}: {e}"

def run(question, tools, needs_approval=()):
    tools_by_name = {t.name: t for t in tools}
    model = get_model().bind_tools(tools)
    messages = [HumanMessage(content=question)]

    for step in range(1, MAX_STEPS + 1):
        ai = model.invoke(messages)
        messages.append(ai)

        if not ai.tool_calls:                 # no more tools wanted: final answer
            return ai.content

        for call in ai.tool_calls:
            result = execute(call, tools_by_name, needs_approval)
            print(f"  step {step}: {call['name']}({call['args']}) -> {result}")
            messages.append(ToolMessage(content=result, tool_call_id=call["id"]))

    return "Stopped: too many tool steps."