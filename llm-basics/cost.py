from count import samples, count_groq_api

INPUT_PRICE_PER_M = 0.075
OUTPUT_PRICE_PER_M = 0.30

REQUESTS = 10_000
ASSUMED_OUTPUT_TOKENS = 100   # assume a short reply to each request

def cost_usd(input_tokens: int, output_tokens: int, n: int) -> float:
    input_cost = input_tokens * n * INPUT_PRICE_PER_M / 1_000_000
    output_cost = output_tokens * n * OUTPUT_PRICE_PER_M / 1_000_000
    return input_cost + output_cost

print(f"{'sample':<10}{'in tokens':>10}{'input only':>14}{'with output':>14}")

for name, text in samples.items():
    t = count_groq_api(text)
    print(f"{name:<10}{t:>10}"
          f"{cost_usd(t, 0, REQUESTS):>13.2f}$"
          f"{cost_usd(t, ASSUMED_OUTPUT_TOKENS, REQUESTS):>13.2f}$")