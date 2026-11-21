import json
from pydantic import BaseModel, Field
# from langchain_ollama import ChatOllama
from tests import TESTS
from scoring import run_once
from prompts_v import PROMPT_V1
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

improver = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.7)
# improver = ChatOllama(model="qwen2.5-coder:7b", temperature=0.7, num_ctx=8192)

class Versions(BaseModel):
    versions: list[str] = Field(description="Three complete, improved system prompts")

# 1) Find where the current prompt fails
results = run_once(PROMPT_V1)
failures = [(t, results[t["id"]][1]) for t in TESTS if not results[t["id"]][0]]
print(f"V1 fails {len(failures)} of {len(TESTS)} cases: {[t['id'] for t, _ in failures]}\n")

failure_text = "\n\n".join(
    f"Question: {t['q']}\nA good answer: {t['expected']}\nThe assistant said: {reply.replace(chr(10), ' | ')}"
    for t, reply in failures
)

# 2) Ask the improver for three different versions
META = f"""You improve system prompts for an AI assistant.

The assistant is the support bot for QuickNotes, a note-taking app. In the user message it receives the
app's docs and a customer question.

<current_prompt>
{PROMPT_V1}
</current_prompt>

<cases_it_gets_wrong>
{failure_text}
</cases_it_gets_wrong>

Write 3 improved versions of the system prompt.
- Fix these failures with GENERAL rules. Do not mention these exact questions.
- Keep what already works: answers come only from the docs, at most 2 sentences,
  and every reply is two lines, "Answer:" and "Source:".
- Keep each version short and clear, with fewer than 8 rules.
- Make the three versions take different approaches: for example ordered decision steps,
  a short rule list, and rules plus one example.
Each version must be a complete system prompt that can be used as it is."""

out = improver.with_structured_output(Versions).invoke(META)

# 3) Save and print them so you can read them
with open("candidates.json", "w") as f:
    json.dump(out.versions, f, indent=2)

for i, v in enumerate(out.versions, start=1):
    print(f"===== CANDIDATE {i} ({len(v.split())} words) =====\n{v}\n")