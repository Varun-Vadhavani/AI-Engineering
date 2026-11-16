import json
import os
import sys
import time
from langchain_core.prompts import ChatPromptTemplate
from models import get_model
from errors import is_temporary

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 3
CHUNK = 10          # save after every 10 items
MAX_ROUNDS = 3      # cap on retry rounds
OUT = "summaries.jsonl"

texts = json.load(open("texts.json", encoding="utf-8"))[:N]
chain = ChatPromptTemplate.from_template(
    "Summarize this in one short sentence:\n\n{text}"
) | get_model()

def load_state():
    """Latest saved row per item index. Later lines override earlier ones."""
    state = {}
    if os.path.exists(OUT):
        for line in open(OUT, encoding="utf-8"):
            row = json.loads(line)
            state[row["i"]] = row
    return state

def save(rows):
    with open(OUT, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())     # force it onto the disk right now

for round_no in range(1, MAX_ROUNDS + 1):
    state = load_state()
    todo = [i for i in range(len(texts))
            if state.get(i, {}).get("status") not in ("ok", "failed_permanent")]
    if not todo:
        break
    print(f"Round {round_no}: {len(todo)} items to do")

    for s in range(0, len(todo), CHUNK):
        ids = todo[s:s + CHUNK]
        results = chain.batch([{"text": texts[i]} for i in ids],
                              config={"max_concurrency": CAP},
                              return_exceptions=True)
        rows = []
        for i, r in zip(ids, results):          # batch keeps the input order
            if isinstance(r, Exception):
                status = "failed_temporary" if is_temporary(r) else "failed_permanent"
                rows.append({"i": i, "status": status,
                             "error": f"{type(r).__name__}: {str(r)[:150]}"})
            else:
                rows.append({"i": i, "status": "ok", "summary": r.content})
        save(rows)                               # progress is on disk after every chunk
        print(f"  saved {len(ids)} items ({sum(x['status'] == 'ok' for x in rows)} ok)")

    if round_no < MAX_ROUNDS:
        time.sleep(5 * round_no)                 # wait longer before each retry round