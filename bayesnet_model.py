from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def build_model():
    # 1) Define structure (DAG)
    # IMPORTANT: Since cpd_p uses evidence ["T","D","S"], the DAG MUST include T->P, D->P, S->P.
    model = DiscreteBayesianNetwork([
        ("W", "S"),   # Weather -> Service Status
        ("T", "P"),   # Time of Day -> Demand Proxy
        ("D", "P"),   # Day Type -> Demand Proxy
        ("S", "P"),   # Service Status -> Demand Proxy

        ("P", "C"),   # Demand Proxy -> Crowding Risk
        ("S", "C"),   # Service Status -> Crowding Risk
        ("M", "C"),   # Network Mode -> Crowding Risk
    ])

    # 2) Define CPDs
    # State order matters. Keep it consistent everywhere.

    # Weather (W): Clear / Rainy / Thunderstorms
    cpd_w = TabularCPD(
        variable="W", variable_card=3,
        values=[[0.50], [0.42], [0.08]],
        state_names={"W": ["Clear", "Rainy", "Thunderstorms"]}
    )

    # Time of Day (T): Morning / Afternoon / Evening
    cpd_t = TabularCPD(
        variable="T", variable_card=3,
        values=[[0.25], [0.35], [0.40]],
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
        values=[[0.85], [0.15]],
        state_names={"M": ["Today", "Future"]}
    )

    # Service Status (S): Normal / Reduced / Disrupted
    # P(S | W)
    cpd_s = TabularCPD(
        variable="S", variable_card=3,
        values=[
            # Evidence order: W = Clear, Rainy, Thunderstorms
            [0.97, 0.92, 0.78],  # Normal
            [0.02, 0.06, 0.15],  # Reduced
            [0.01, 0.02, 0.07],  # Disrupted
        ],
        evidence=["W"],
        evidence_card=[3],
        state_names={
            "S": ["Normal", "Reduced", "Disrupted"],
            "W": ["Clear", "Rainy", "Thunderstorms"],
        }
    )

    # Demand Proxy (P): Low / Medium / High
    # P depends on T, D, S (3*2*3 = 18 columns).
    t_states = ["Morning", "Afternoon", "Evening"]
    d_states = ["Weekday", "Weekend"]
    s_states = ["Normal", "Reduced", "Disrupted"]

    # Evidence order: ["T","D","S"] with cards [3,2,3] => 18 columns
    # Column order:
    # for T in [Morning,Afternoon,Evening]:
    #   for D in [Weekday,Weekend]:
    #     for S in [Normal,Reduced,Disrupted]:
    p_low = [
        0.134, 0.101, 0.077,   # Morning, Weekday, (Normal/Reduced/Disrupted)
        0.156, 0.117, 0.089,   # Morning, Weekend, (Normal/Reduced/Disrupted)
        0.458, 0.386, 0.312,   # Afternoon, Weekday
        0.525, 0.453, 0.375,   # Afternoon, Weekend
        0.216, 0.174, 0.137,   # Evening, Weekday
        0.258, 0.209, 0.165,   # Evening, Weekend
    ]

    p_med = [
        0.272, 0.241, 0.213,
        0.222, 0.196, 0.173,
        0.305, 0.303, 0.288,
        0.270, 0.266, 0.250,
        0.417, 0.396, 0.357,
        0.360, 0.340, 0.305,
    ]

    p_high = [
        0.594, 0.658, 0.710,
        0.622, 0.687, 0.738,
        0.237, 0.311, 0.400,
        0.205, 0.281, 0.375,
        0.368, 0.430, 0.506,
        0.382, 0.452, 0.530,
    ]

    cpd_p = TabularCPD(
        variable="P", variable_card=3,
        values=[p_low, p_med, p_high],
        evidence=["T", "D", "S"],
        evidence_card=[3, 2, 3],
        state_names={
            "P": ["Low", "Medium", "High"],
            "T": t_states,
            "D": d_states,
            "S": s_states,
        }
    )

    # Crowding Risk (C): Low / Medium / High depends on P, S, M (3*3*2 = 18 columns).
    p_states = ["Low", "Medium", "High"]
    s_states = ["Normal", "Reduced", "Disrupted"]
    m_states = ["Today", "Future"]

    # Evidence order: ["P","S","M"] with cards [3,3,2] => 18 columns
    # Column order:
    # for P in [Low,Medium,High]:
    #   for S in [Normal,Reduced,Disrupted]:
    #     for M in [Today,Future]:

    c_low = [
        # P=Low
        0.85, 0.92,   # S=Normal, M=Today/Future
        0.35, 0.15,   # S=Reduced
        0.15, 0.01,   # S=Disrupted
        # P=Medium
        0.30, 0.55,
        0.05, 0.15,
        0.02, 0.01,
        # P=High
        0.05, 0.20,
        0.00, 0.02,
        0.00, 0.01,
    ]

    c_med = [
        # P=Low
        0.14, 0.08,
        0.50, 0.60,
        0.35, 0.27,
        # P=Medium
        0.60, 0.40,
        0.25, 0.60,
        0.08, 0.27,
        # P=High
        0.35, 0.60,
        0.10, 0.48,
        0.02, 0.27,
    ]

    c_high = [
        # P=Low
        0.01, 0.00,
        0.15, 0.25,
        0.50, 0.72,
        # P=Medium
        0.10, 0.05,
        0.70, 0.25,
        0.90, 0.72,
        # P=High
        0.60, 0.20,
        0.90, 0.50,
        0.98, 0.72,
    ]

    cpd_c = TabularCPD(
        variable="C", variable_card=3,
        values=[c_low, c_med, c_high],
        evidence=["P", "S", "M"],
        evidence_card=[3, 3, 2],
        state_names={
            "C": ["Low", "Medium", "High"],
            "P": p_states,
            "S": s_states,
            "M": m_states,
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
    # pgmpy returns a DiscreteFactor for a single-variable query
    return result


if __name__ == "__main__":
    model = build_model()
    print(model.check_model())
    print(model.get_cpds("S"))
    print(model.get_cpds("P"))
    print(model.get_cpds("C"))

    # Example 1: infer S from W (since S not provided)
    dist = infer_crowding(model, evidence={"W": "Rainy", "T": "Evening", "D": "Weekday", "M": "Today"})
    print(dist)

    # Example 2: force service advisory
    dist2 = infer_crowding(model, evidence={"T": "Evening", "D": "Weekday", "S": "Reduced", "M": "Today"})
    print(dist2)
