from bayesnet_model import build_model, infer_crowding

SCENARIOS = [
    # Example required-style scenarios
    ("Rainy evening + reduced service (Today)",  {"W": "Rainy", "T": "Evening", "D": "Weekday", "S": "Reduced",   "M": "Today"}),
    ("Rainy evening + reduced service (Future)", {"W": "Rainy", "T": "Evening", "D": "Weekday", "S": "Reduced",   "M": "Future"}),

    ("Clear morning weekday + normal (Today)",   {"W": "Clear", "T": "Morning", "D": "Weekday", "S": "Normal",    "M": "Today"}),
    ("Clear morning weekday + normal (Future)",  {"W": "Clear", "T": "Morning", "D": "Weekday", "S": "Normal",    "M": "Future"}),

    ("Weekend afternoon + normal (Today)",       {"W": "Clear", "T": "Afternoon", "D": "Weekend", "S": "Normal",  "M": "Today"}),

    ("Disrupted service near corridor (Today)",  {"W": "Clear", "T": "Evening", "D": "Weekday", "S": "Disrupted", "M": "Today"}),
    ("Disrupted service near corridor (Future)", {"W": "Clear", "T": "Evening", "D": "Weekday", "S": "Disrupted", "M": "Future"}),
]

def top_state(distribution):
    # distribution.values corresponds to state_names order in the CPD
    states = distribution.state_names["C"]
    probs = distribution.values
    i = probs.argmax()
    return states[i], probs[i]

if __name__ == "__main__":
    model = build_model()

    for name, evidence in SCENARIOS:
        dist = infer_crowding(model, evidence=evidence)
        state, p = top_state(dist)
        print(f"\n{name}")
        print(f"Evidence: {evidence}")
        print("P(C):", {s: float(v) for s, v in zip(dist.state_names['C'], dist.values)})
        print(f"Most likely: {state} ({p:.3f})")
