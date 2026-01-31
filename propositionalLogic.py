import sys
sys.path.append('/mnt/user-data/uploads')

from logic import *


TODAY = Symbol("TODAY")
FUTURE = Symbol("FUTURE")
SUSP_TM_EX = Symbol("SUSP_TM_EX")
TELE_ACTIVE = Symbol("TELE_ACTIVE")
CRL_ACTIVE = Symbol("CRL_ACTIVE")
WORKS_CHANGI = Symbol("WORKS_CHANGI")
CLOSED_CA = Symbol("CLOSED_CA")
CLOSED_T5 = Symbol("CLOSED_T5")
USE_SB_T5 = Symbol("USE_SB_T5")
USE_T5_TM = Symbol("USE_T5_TM")
USE_EX_CA = Symbol("USE_EX_CA")
USE_TM_EX = Symbol("USE_TM_EX")


rules = {
    "R1": Implication(TODAY, Not(FUTURE)),
    "R2": Implication(TELE_ACTIVE, FUTURE),
    "R3": Implication(CRL_ACTIVE, FUTURE),
    "R4": Implication(WORKS_CHANGI, CLOSED_CA),
    "R5": Implication(SUSP_TM_EX, Not(USE_TM_EX)),
    "R6": Implication(CLOSED_T5, Not(USE_SB_T5)),
    "R7": Implication(TODAY, Not(USE_SB_T5)),
    "R8": Implication(TODAY, Not(USE_T5_TM)),
    "R9a": Implication(USE_SB_T5, TELE_ACTIVE),
    "R9b": Implication(USE_T5_TM, TELE_ACTIVE),
    "R10": Implication(CLOSED_CA, Not(USE_EX_CA))
}

knowledge = And(*rules.values())


scenarios = [
    {
        "num": 1,
        "description": "Using future route in today mode",
        "mode": "Today",
        "route": "Sungei Bedok to T5",
        "advisories": "None",
        "facts": And(TODAY, USE_SB_T5)
    },
    {
        "num": 2,
        "description": "Valid today mode route",
        "mode": "Today",
        "route": "Tanah Merah to Expo to Changi Airport",
        "advisories": "None",
        "facts": And(TODAY, USE_TM_EX, USE_EX_CA)
    },
    {
        "num": 3,
        "description": "Using route to closed station",
        "mode": "Today",
        "route": "Expo to Changi Airport",
        "advisories": "CLOSED_CA",
        "facts": And(TODAY, USE_EX_CA, CLOSED_CA)
    },
    {
        "num": 4,
        "description": "Valid future mode route",
        "mode": "Future",
        "route": "Sungei Bedok to T5",
        "advisories": "None",
        "facts": And(FUTURE, USE_SB_T5, TELE_ACTIVE)
    },
    {
        "num": 5,
        "description": "Route to station with works",
        "mode": "Future",
        "route": "Expo to Changi Airport",
        "advisories": "WORKS_CHANGI",
        "facts": And(FUTURE, USE_EX_CA, WORKS_CHANGI)
    },
    {
        "num": 6,
        "description": "Using suspended route",
        "mode": "Future",
        "route": "Tanah Merah to Expo",
        "advisories": "SUSP_TM_EX",
        "facts": And(FUTURE, USE_TM_EX, SUSP_TM_EX)
    }
]


def is_satisfiable(kb):
    symbols = kb.symbols()
    return try_find_model(kb, symbols, {})


def try_find_model(kb, symbols, model):
    if not symbols:
        try:
            return kb.evaluate(model)
        except:
            return False
    
    remaining = symbols.copy()
    p = remaining.pop()
    
    model_true = model.copy()
    model_true[p] = True
    if try_find_model(kb, remaining, model_true):
        return True
    
    model_false = model.copy()
    model_false[p] = False
    return try_find_model(kb, remaining, model_false)


def find_violated_rules(scenario_facts):
    violated = []
    
    for rule_name, rule in rules.items():
        test_kb = And(rule, scenario_facts)
        if not is_satisfiable(test_kb):
            violated.append(rule_name)
    
    symbols_dict = {}
    for symbol in scenario_facts.symbols():
        symbols_dict[symbol] = True
    
    if "WORKS_CHANGI" in symbols_dict and "USE_EX_CA" in symbols_dict:
        if "R4" not in violated:
            test_r4_chain = And(rules["R4"], rules["R10"], scenario_facts)
            if not is_satisfiable(test_r4_chain):
                violated.extend(["R4", "R10"])
    
    return sorted(list(set(violated)))


def get_rule_description(rule_name):
    descriptions = {
        "R1": "TODAY → ¬FUTURE (Cannot be in both modes simultaneously)",
        "R2": "TELE_ACTIVE → FUTURE (TELe only available in future mode)",
        "R3": "CRL_ACTIVE → FUTURE (CRL only active in future mode)",
        "R4": "WORKS_CHANGI → CLOSED_CA (Works at Changi closes the airport)",
        "R5": "SUSP_TM_EX → ¬USE_TM_EX (Suspended route cannot be used)",
        "R6": "CLOSED_T5 → ¬USE_SB_T5 (Closed T5 blocks SB-T5 route)",
        "R7": "TODAY → ¬USE_SB_T5 (SB-T5 not available in today mode)",
        "R8": "TODAY → ¬USE_T5_TM (TM-T5 not available in today mode)",
        "R9a": "USE_SB_T5 → TELE_ACTIVE (SB-T5 requires TELe to be active)",
        "R9b": "USE_T5_TM → TELE_ACTIVE (TM-T5 requires TELe to be active)",
        "R10": "CLOSED_CA → ¬USE_EX_CA (Closed airport blocks EX-CA route)"
    }
    return descriptions.get(rule_name, "Unknown rule")


def analyze_scenario(scenario_facts):
    combined_kb = And(knowledge, scenario_facts)
    is_sat = is_satisfiable(combined_kb)
    
    if not is_sat:
        result = "CONTRADICTION"
        violated_rules = find_violated_rules(scenario_facts)
    else:
        result = "VALID"
        violated_rules = []
    
    return result, violated_rules


def view_rules():
    print("\n" + "="*100)
    print("PROPOSITIONAL LOGIC RULES")
    print("="*100)
    
    rule_details = [
        ("R1", "TODAY → ¬FUTURE", "Cannot be in both TODAY and FUTURE modes simultaneously"),
        ("R2", "TELE_ACTIVE → FUTURE", "TELe is only available in FUTURE mode"),
        ("R3", "CRL_ACTIVE → FUTURE", "CRL is only active in FUTURE mode"),
        ("R4", "WORKS_CHANGI → CLOSED_CA", "Works at Changi closes the airport station"),
        ("R5", "SUSP_TM_EX → ¬USE_TM_EX", "Suspended Tanah Merah to Expo route cannot be used"),
        ("R6", "CLOSED_T5 → ¬USE_SB_T5", "Closed Terminal 5 blocks Sungei Bedok to T5 route"),
        ("R7", "TODAY → ¬USE_SB_T5", "Sungei Bedok to T5 route not available in TODAY mode"),
        ("R8", "TODAY → ¬USE_T5_TM", "Tanah Merah to T5 route not available in TODAY mode"),
        ("R9", "(USE_SB_T5 → TELE_ACTIVE) ∧ (USE_T5_TM → TELE_ACTIVE)", 
         "Both SB-T5 and TM-T5 routes require TELe to be active"),
        ("R10", "CLOSED_CA → ¬USE_EX_CA", "Closed Changi Airport blocks Expo to Changi route")
    ]
    
    for rule_id, formula, description in rule_details:
        print(f"\n{rule_id}: {formula}")
        print(f"     → {description}")
    
    print("\n" + "="*100)


def view_scenarios():
    print("\n" + "="*100)
    print("ALL SCENARIOS")
    print("="*100)
    
    for scenario in scenarios:
        print(f"\nScenario {scenario['num']}: {scenario['description']}")
        print(f"  • Mode: {scenario['mode']}")
        print(f"  • Route: {scenario['route']}")
        print(f"  • Advisories: {scenario['advisories']}")
    
    print("\n" + "="*100)


def run_scenario_validation():
    print("\n" + "="*100)
    print("SCENARIO VALIDATION RESULTS")
    print("="*100)
    
    results = []
    for scenario in scenarios:
        result, violated_rules = analyze_scenario(scenario["facts"])
        scenario_result = scenario.copy()
        scenario_result["result"] = result
        scenario_result["violated_rules"] = violated_rules
        results.append(scenario_result)
    
    # Display results
    for scenario in results:
        status = "✅ VALID" if scenario["result"] == "VALID" else "❌ CONTRADICTION"
        print(f"\nScenario {scenario['num']}: {status}")
        print(f"  Mode: {scenario['mode']} | Route: {scenario['route']} | Advisories: {scenario['advisories']}")
        
        if scenario["violated_rules"]:
            print(f"  Rules Violated:")
            for rule_name in scenario["violated_rules"]:
                print(f"    • {rule_name}: {get_rule_description(rule_name)}")
    
    print("\n" + "="*100)


def display_menu():
    print("\n" + "="*100)
    print("MRT LOGIC INFERENCE SYSTEM - MAIN MENU")
    print("="*100)
    print("\nPlease select an option:")
    print("  1. View All Rules")
    print("  2. View All Scenarios")
    print("  3. Run Scenario Validation")
    print("  4. Exit")
    print("\n" + "="*100)


def main():
    print("="*100)
    print(" "*30 + "MRT LOGIC INFERENCE SYSTEM")
    print(" "*25 + "Propositional Logic Analysis Tool")
    print("="*100)
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                view_rules()
            elif choice == "2":
                view_scenarios()
            elif choice == "3":
                run_scenario_validation()
            elif choice == "4":
                print("\n" + "="*100)
                print("Thank you for using the MRT Logic Inference System!")
                print("="*100 + "\n")
                break
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 4.")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*100)
            print("Program interrupted. Exiting...")
            print("="*100 + "\n")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again.")
    

if __name__ == "__main__":
    main()