from tools import TOOLS

for t in TOOLS:
    print("NAME:       ", t.name)
    print("DESCRIPTION:", t.description)
    print("INPUTS:     ", t.args)
    print()

print(TOOLS[0].invoke({"city": "Ahmedabad"}))