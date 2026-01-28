from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def build_model():
    # 1) Define structure (DAG)
    model = DiscreteBayesianNetwork([
        ("W", "P"),  # Weather -> Demand Proxy
        ("T", "P"),  # Time of day -> Demand Proxy
        ("D", "P"),  # Day type -> Demand Proxy
        ("M", "P"),  # Network mode -> Demand Proxy

        ("P", "C"),  # Demand Proxy -> Crowding Risk
        ("S", "C"),  # Service status -> Crowding Risk
        ("M", "C"),  # Network mode -> Crowding Risk
    ])

    # 2) Define CPDs
    # State order matters. Keep it consistent everywhere.

    # Weather (W): Clear / Rainy / Thunderstorms
    cpd_w = TabularCPD(
        variable="W", variable_card=3,
        values=[[0.60], [0.30], [0.10]],
        state_names={"W": ["Clear", "Rainy", "Thunderstorms"]}
    )

    # Time of Day (T): Morning / Afternoon / Evening
    cpd_t = TabularCPD(
        variable="T", variable_card=3,
        values=[[0.35], [0.30], [0.35]],
        state_names={"T": ["Morning", "Afternoon", "Evening"]}
    )

    # Day Type (D): Weekday / Weekend
    cpd_d = TabularCPD(
        variable="D", variable_card=2,
        values=[[0.72], [0.28]],
        state_names={"D": ["Weekday", "Weekend"]}
    )

    # Network Mode (M): Today / Future
    cpd_m = TabularCPD(
        variable="M", variable_card=2,
        values=[[0.50], [0.50]],
        state_names={"M": ["Today", "Future"]}
    )

    # Service Status (S): Normal / Reduced / Disrupted
    cpd_s = TabularCPD(
        variable="S", variable_card=3,
        values=[[0.80], [0.15], [0.05]],
        state_names={"S": ["Normal", "Reduced", "Disrupted"]}
    )

    # Demand Proxy (P): Low / Medium / High
    # P depends on W, T, D, M (3*3*2*2 = 36 columns).
    #
    # To get you started quickly, we’ll implement a simple rule-based generator:
    # - base demand: Medium
    # - Evening + Weekday => push higher
    # - Weekend Afternoon => medium-high
    # - Bad weather (Rainy/Thunderstorms) => slightly higher demand in stations (proxy)
    # - Future mode => slightly spreads load (assume slightly lower high demand in some cases)
    #
    # This is "assumed but justified": you will later refine with sources or datasets.

    w_states = ["Clear", "Rainy", "Thunderstorms"]
    t_states = ["Morning", "Afternoon", "Evening"]
    d_states = ["Weekday", "Weekend"]
    m_states = ["Today", "Future"]

    def demand_probs(w, t, d, m):
        # Start with baseline
        low, med, high = 0.25, 0.50, 0.25

        # Time/Day effect
        if t == "Evening" and d == "Weekday":
            low, med, high = 0.15, 0.45, 0.40
        elif t == "Morning" and d == "Weekday":
            low, med, high = 0.20, 0.50, 0.30
        elif t == "Afternoon" and d == "Weekend":
            low, med, high = 0.20, 0.45, 0.35

        # Weather effect (proxy: more crowding potential during bad weather)
        if w == "Rainy":
            low -= 0.05
            high += 0.05
        elif w == "Thunderstorms":
            low -= 0.08
            high += 0.08

        # Future mode effect (assume slightly better distribution/capacity)
        if m == "Future":
            high -= 0.03
            med += 0.03

        # Clamp and re-normalize
        low = max(low, 0.01)
        med = max(med, 0.01)
        high = max(high, 0.01)
        s = low + med + high
        return [low / s, med / s, high / s]

    # Build 36 columns in the exact pgmpy evidence order
    columns = []
    for w in w_states:
        for t in t_states:
            for d in d_states:
                for m in m_states:
                    columns.append(demand_probs(w, t, d, m))

    # TabularCPD wants rows = states of P, columns = all evidence combinations.
    # columns is list of [low, med, high] for each column; transpose it:
    p_low = [col[0] for col in columns]
    p_med = [col[1] for col in columns]
    p_high = [col[2] for col in columns]

    cpd_p = TabularCPD(
        variable="P", variable_card=3,
        values=[p_low, p_med, p_high],
        evidence=["W", "T", "D", "M"],
        evidence_card=[3, 3, 2, 2],
        state_names={
            "P": ["Low", "Medium", "High"],
            "W": w_states,
            "T": t_states,
            "D": d_states,
            "M": m_states,
        }
    )

    # Crowding Risk (C): Low / Medium / High depends on P, S, M (3*3*2 = 18 columns).
    p_states = ["Low", "Medium", "High"]
    s_states = ["Normal", "Reduced", "Disrupted"]

    def crowding_probs(p, s, m):
        # Baseline: if demand is low and service normal => low crowding likely
        if p == "Low":
            low, med, high = 0.70, 0.25, 0.05
        elif p == "Medium":
            low, med, high = 0.35, 0.50, 0.15
        else:  # High demand
            low, med, high = 0.15, 0.45, 0.40

        # Service disruption pushes crowding up
        if s == "Reduced":
            low -= 0.10
            high += 0.10
        elif s == "Disrupted":
            low -= 0.20
            high += 0.20

        # Future mode: assume improved resilience/capacity around the corridor
        if m == "Future":
            high -= 0.05
            med += 0.03
            low += 0.02

        # Clamp and normalize
        low = max(low, 0.01)
        med = max(med, 0.01)
        high = max(high, 0.01)
        total = low + med + high
        return [low / total, med / total, high / total]

    c_cols = []
    for p in p_states:
        for s in s_states:
            for m in m_states:
                c_cols.append(crowding_probs(p, s, m))

    c_low = [col[0] for col in c_cols]
    c_med = [col[1] for col in c_cols]
    c_high = [col[2] for col in c_cols]

    cpd_c = TabularCPD(
        variable="C", variable_card=3,
        values=[c_low, c_med, c_high],
        evidence=["P", "S", "M"],
        evidence_card=[3, 3, 2],
        state_names={
            "C": ["Low", "Medium", "High"],
            "P": p_states,
            "S": s_states,
            "M": m_states
        }
    )

    model.add_cpds(cpd_w, cpd_t, cpd_d, cpd_m, cpd_s, cpd_p, cpd_c)

    # 3) Validate model
    if not model.check_model():
        raise ValueError("Model is invalid. Check CPDs and structure.")

    return model


def infer_crowding(model, evidence: dict):
    infer = VariableElimination(model)
    result = infer.query(variables=["C"], evidence=evidence, show_progress=False)
    return result["C"]


if __name__ == "__main__":
    model = build_model()
    dist = infer_crowding(model, evidence={"W": "Rainy", "T": "Evening", "D": "Weekday", "S": "Reduced", "M": "Today"})
    print(dist)
