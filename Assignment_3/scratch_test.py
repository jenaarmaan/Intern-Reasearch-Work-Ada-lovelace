
import sys
import os
import json

# Add Assignment 3 to path
sys.path.append(os.path.abspath("Assignment 3"))

from backend.services.ai_engine import generate_circuit_json
from backend.services.validator import validate_circuit_json, correct_circuit_json
from backend.services.quantum_engine import build_and_simulate_circuit

def run_test(name, prompt):
    print(f"\n=== Testing: {name} ===")
    print(f"Prompt: {prompt}")
    
    # 1. AI Generation
    circuit_json = generate_circuit_json(prompt)
    print(f"AI Output: {json.dumps(circuit_json, indent=2)}")
    
    if "error" in circuit_json:
        print(f"[FAIL] AI Generation Failed: {circuit_json['error']}")
        return False
        
    # 2. Correction & Validation
    circuit_json = correct_circuit_json(circuit_json)
    is_valid, v_error = validate_circuit_json(circuit_json)
    
    if not is_valid:
        print(f"[FAIL] Validation Failed: {v_error}")
        return False
    else:
        print("[PASS] Validation Passed")
        
    # 3. Simulation
    result = build_and_simulate_circuit(circuit_json)
    if result["success"]:
        print("[PASS] Simulation Success")
        print(f"Metrics: {result['metrics']}")
        print("Counts:")
        print(result["counts"])
        # print("Diagram:")
        # print(result["diagram"])
        return True
    else:
        print(f"[FAIL] Simulation Failed: {result['error']}")
        return False

if __name__ == "__main__":
    test_cases = [
        ("Bell State", "Create a Bell state"),
        ("Hadamard", "Apply Hadamard to qubit 0"),
        ("GHZ State", "Create a 3-qubit GHZ state (H on 0, CNOT 0->1, CNOT 1->2)"),
        ("Rotation", "Apply RX with pi/4 on qubit 0")
    ]
    
    results = []
    for name, prompt in test_cases:
        success = run_test(name, prompt)
        results.append((name, success))
        import time
        time.sleep(5)
    
    print("\n\n=== FINAL RESULTS ===")
    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{name}: {status}")
