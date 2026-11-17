from classify import score

VARIED = [  # your best order from step 10
    ("Notifications arrive late on my tablet, though they work fine on my phone.", "MEDIUM"),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.", "LOW"),
    ("My files from last month are missing after I restored a backup.", "HIGH"),
]

REPETITIVE = [  # three different messages, but all the same label
    ("My files from last month are missing after I restored a backup.", "HIGH"),
    ("I was billed for a subscription I cancelled last week.", "HIGH"),
    ("I can't open my account and I have a deadline today.", "HIGH"),
]

POISONED = [  # same as varied, but the typo example has the WRONG label
    ("Notifications arrive late on my tablet, though they work fine on my phone.", "MEDIUM"),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.", "HIGH"),
    ("My files from last month are missing after I restored a backup.", "HIGH"),
]

for name, examples in [("varied", VARIED), ("repetitive", REPETITIVE), ("poisoned", POISONED)]:
    correct, wrong = score(examples)
    too_high = sum(1 for _, _, got in wrong if got == "HIGH")
    print(f"{name:11} score {correct}/10   wrong: {wrong}")
    print(f"{'':11} wrong answers that said HIGH: {too_high}")