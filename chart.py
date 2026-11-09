import matplotlib
matplotlib.use("Agg")          # render to a file, no window needed
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120, 135, 128, 160, 182, 175]

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
ax.bar(months, sales, color="#4c78a8")
ax.set_title("Monthly Sales (units)")
ax.set_ylabel("Units sold")
fig.savefig("chart.png")
print("saved chart.png (1200x750 pixels)")