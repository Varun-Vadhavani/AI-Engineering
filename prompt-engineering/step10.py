from itertools import permutations
from classify import score

EXAMPLES = [
    ("My files from last month are missing after I restored a backup.", "HIGH"),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.", "LOW"),
    ("Notifications arrive late on my tablet, though they work fine on my phone.", "MEDIUM"),
]

# Same three examples, every possible order (3 examples = 6 orders)
for order in permutations(EXAMPLES):
    labels = " -> ".join(label for _, label in order)
    correct, wrong = score(list(order))
    print(f"order {labels:22} score {correct}/10   wrong: {wrong}")