import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MAX_VALID_ATT = 1000  # фильтр допустимости


with open("results.json") as f:
    data = json.load(f)

nsga2 = data["nsga2"]
dbmosa = data["dbmosa"]

nsga2 = [
    p for p in nsga2 if p[0] < MAX_VALID_ATT
]

dbmosa = [
    p for p in dbmosa if p[0] < MAX_VALID_ATT
]

# === Парето-фронты ===
plt.figure()
plt.scatter(
    [a for a, t in nsga2],
    [t for a, t in nsga2],
    label="NSGA-II",
    marker="o",
)
plt.scatter(
    [a for a, t in dbmosa],
    [t for a, t in dbmosa],
    label="DBMOSA",
    marker="x",
)

plt.xlabel("ATT")
plt.ylabel("TRT")
plt.title("Pareto Front Comparison (Mandl)")
plt.legend()
plt.grid(True)
plt.savefig("pareto_front.png", dpi=200, bbox_inches="tight")
plt.close()
