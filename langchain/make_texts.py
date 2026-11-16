import json

topics = [
    ("a bakery", "opened a second branch near the railway station"),
    ("a school", "introduced a robotics club for grade 8 students"),
    ("a bus service", "changed its night timetable on three routes"),
    ("a hospital", "started a free eye check-up camp every Sunday"),
    ("a local library", "added 2,000 new books and a quiet reading room"),
    ("a cricket club", "won the district final after a close last-over finish"),
    ("a startup", "launched an app that helps farmers track crop prices"),
    ("a city council", "approved a plan to plant 5,000 trees along main roads"),
    ("a cinema", "began showing classic films on Friday afternoons"),
    ("a coaching centre", "moved its weekend classes online for exam season"),
]
details = [
    "Many residents said they welcomed the change.",
    "Some people raised concerns about the cost.",
    "The announcement was made on Monday morning.",
    "Officials said more updates would follow next month.",
    "Local news channels covered the story briefly.",
    "Staff members said preparation took several weeks.",
    "Early feedback has been mostly positive.",
    "A few neighbours complained about noise during setup.",
    "The project was funded by small donations.",
    "Reporters noted that the effect may take months to measure.",
    "Attendance at the first event was higher than expected.",
    "Critics said the plan does not go far enough.",
    "Supporters called it a long-overdue improvement.",
    "The team said they will review results after three months.",
    "Several nearby businesses plan similar steps.",
    "The change takes effect at the start of next week.",
    "People can find details on a notice board at the entrance.",
    "The decision followed a survey of local families.",
    "Volunteers helped spread the word over the weekend.",
    "An independent group will check how it goes.",
]

texts = []
for i in range(200):
    who, what = topics[i % len(topics)]
    detail = details[(i * 7) % len(details)]
    texts.append(f"{who.capitalize()} {what}. {detail}")

with open("texts.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, indent=2)

print(len(texts), "texts saved. Example:", texts[0])