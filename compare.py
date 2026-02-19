import json

MAX_VALID_ATT = 1000  # фильтр допустимости


with open("experiments/results.json") as f:
    data = json.load(f)

nsga2 = data["nsga2"]
dbmosa = data["dbmosa"]

nsga2 = [
    p for p in nsga2 if p[0] < MAX_VALID_ATT
]

dbmosa = [
    p for p in dbmosa if p[0] < MAX_VALID_ATT
]

def summarize(points):
    atts = [a for a, _ in points]
    trts = [t for _, t in points]

    return {
        "ATT_best": min(atts),
        "ATT_mean": sum(atts) / len(atts),
        "ATT_worst": max(atts),
        "TRT_best": min(trts),
        "TRT_mean": sum(trts) / len(trts),
        "TRT_worst": max(trts),
    }

print("NSGA-II:", summarize(nsga2))
print("DBMOSA:", summarize(dbmosa))
