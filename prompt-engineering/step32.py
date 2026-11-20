from collections import defaultdict
from langchain_ollama import ChatOllama
from tests import TESTS
from scoring import run_once
from prompts_v import PROMPT_V1, PROMPT_V2

RUNS = 3

# A realistic setting: temperature above 0, like many real apps
warm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192, temperature=0.7)

IDS = [t["id"] for t in TESTS]

def evaluate(name, prompt):
    totals, passes = [], defaultdict(int)
    for _ in range(RUNS):
        res = run_once(prompt, model=warm)
        totals.append(sum(ok for ok, _ in res.values()))
        for i, (ok, _) in res.items():
            passes[i] += ok
    always = [i for i in IDS if passes[i] == RUNS]
    never = [i for i in IDS if passes[i] == 0]
    flaky = {i: f"{passes[i]}/{RUNS}" for i in IDS if 0 < passes[i] < RUNS}
    print(f"{name}: totals per run {totals} | mean {sum(totals)/RUNS:.1f}/10 | range {min(totals)}-{max(totals)}")
    print(f"   always pass ({len(always)}): {always}")
    print(f"   never pass  ({len(never)}): {never}")
    print(f"   flaky       ({len(flaky)}): {flaky}\n")

evaluate("V1", PROMPT_V1)
evaluate("V2", PROMPT_V2)