from classify import score

POISONED_2 = [
    ("Notifications arrive late on my tablet, though they work fine on my phone.", "MEDIUM"),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.", "LOW"),
    ("My files from last month are missing after I restored a backup.", "LOW"),
]

correct, wrong = score(POISONED_2)
print(f"poisoned (data loss labeled LOW)  score {correct}/10   wrong: {wrong}")
print("for comparison, varied was 9/10 with wrong: [(7, 'LOW', 'HIGH')]")