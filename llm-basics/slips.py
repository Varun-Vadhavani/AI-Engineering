import random
from PIL import Image, ImageDraw
from llm import ask_image

# Test A: counting (23 red circles, true answer = 23)
rng = random.Random(7)
img = Image.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(img)
placed = []
while len(placed) < 23:
    x, y = rng.randint(40, 760), rng.randint(40, 560)
    if all((x - px) ** 2 + (y - py) ** 2 > 55 ** 2 for px, py in placed):
        placed.append((x, y))
for x, y in placed:
    draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill="#d9534f")
img.save("dots.png")

print("TEST A: counting (truth = 23)")
for trial in range(3):
    answer, _ = ask_image("dots.png", "How many red circles are in this image? Reply with just the number.")
    print(f"  trial {trial + 1}: {answer}")

# ---- Test B: small dense text (truth known) ----
rng = random.Random(3)
lines = [f"Ref {1000 + i}: batch value {rng.randint(1000, 9999)}" for i in range(40)]
truth = lines[27].split()[-1]

text_img = Image.new("RGB", (400, 40 * 14 + 20), "white")
d = ImageDraw.Draw(text_img)
for i, line in enumerate(lines):
    d.text((10, 10 + i * 14), line, fill="black")
text_img.save("dense_full.png")
w, h = text_img.size
text_img.resize((int(w * 0.35), int(h * 0.35))).save("dense_small.png")

print(f"\nTEST B: dense text, batch value for Ref 1027 (truth = {truth})")
for name in ["dense_full.png", "dense_small.png"]:
    answer, tokens = ask_image(name, "What is the batch value for Ref 1027? Reply with just the number.")
    print(f"  {name:<16} in={tokens:>4} | {answer}")

# ---- Test C: asking about something that is not there ----
print("\nTEST C: a detail that does not exist in dots.png")
for q in [
    "What text is written on the sign in the top-left corner?",
    "What brand is the car in the background?",
]:
    answer, _ = ask_image("dots.png", q, max_tokens=120)
    print(f"  Q: {q}\n  A: {answer}\n")