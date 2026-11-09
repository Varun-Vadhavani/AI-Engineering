import random
import time
from requests.exceptions import HTTPError
from llm import ask

LABS = ["Atlas", "Borealis", "Cinder", "Delphi", "Ember", "Fjord", "Gale", "Helix"]
WORDS = ["ALFA", "BRAVO", "DELTA", "ECHO", "FOXTROT", "GOLF"]
NEEDLE = "Note X: the access code for the Orion lab is 7391-KILO."
QUESTION = "What is the access code for the Orion lab? Reply with just the code."

def build_prompt(position: float, n_lines: int, seed: int) -> str:
    rng = random.Random(seed)
    lines = [
        f"Note {i}: the access code for the {rng.choice(LABS)} lab is "
        f"{rng.randint(1000, 9999)}-{rng.choice(WORDS)}."
        for i in range(n_lines)
    ]
    lines.insert(int(n_lines * position), NEEDLE)
    return "\n".join(lines) + f"\n\n{QUESTION}"

def ask_with_retry(prompt: str) -> str:
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            return ask(prompt, max_tokens=256)
        except HTTPError as error:
            response = error.response
            if response is None or response.status_code != 429:
                raise
            if attempt == max_attempts - 1:
                raise RuntimeError(
                    f"Groq rate limit persisted after {max_attempts} attempts: "
                    f"{response.text}"
                ) from error
            retry_after = response.headers.get("Retry-After")
            try:
                delay = (
                    float(retry_after)
                    if retry_after is not None
                    else min(15 * (2**attempt), 60)
                )
            except ValueError:
                delay = min(15 * (2**attempt), 60)
            print(f"Rate limited; retrying in {delay:g}s...", flush=True)
            time.sleep(min(delay, 60))

N_LINES = 300
TRIALS = 3
REQUEST_INTERVAL_SECONDS = 20
POSITIONS = [0.0, 0.25, 0.5, 0.75, 1.0]
total_requests = len(POSITIONS) * TRIALS
completed_requests = 0

for position in POSITIONS:
    hits = 0
    for seed in range(TRIALS):
        answer = ask_with_retry(build_prompt(position, N_LINES, seed))
        hits += "7391-KILO" in answer
        completed_requests += 1
        if completed_requests < total_requests:
            time.sleep(REQUEST_INTERVAL_SECONDS)
    print(f"needle at {position:>4.0%} of the text: {hits}/{TRIALS} correct")