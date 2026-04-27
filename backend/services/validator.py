def validate_circuit_json(data):
    """
    Validates the structure and logic of the generated circuit JSON.
    """
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    
    if "qubits" not in data or "gates" not in data:
        return False, "Missing 'qubits' or 'gates' fields"
    
    qubits = data["qubits"]
    if not isinstance(qubits, int) or qubits <= 0:
        return False, "Invalid number of qubits"
    
    gates = data["gates"]
    if not isinstance(gates, list):
        return False, "'gates' must be a list"
    
    allowed_gates = ["H", "X", "Y", "Z", "S", "T", "CNOT", "RX", "RY", "RZ", "MEASURE"]
    
    for i, gate in enumerate(gates):
        g_type = gate.get("type", "").upper()
        if g_type not in allowed_gates:
            return False, f"Gate {i}: Unsupported gate type '{g_type}'"
        
        target = gate.get("target")
        if target is None or not isinstance(target, int) or target < 0 or target >= qubits:
            return False, f"Gate {i}: Invalid target qubit index"
            
        if g_type == "CNOT":
            control = gate.get("control")
            if control is None or not isinstance(control, int) or control < 0 or control >= qubits:
                return False, f"Gate {i}: Invalid control qubit index"
            if control == target:
                return False, f"Gate {i}: Control and target cannot be the same"

    return True, None

def correct_circuit_json(data):
    """
    Attempts to automatically fix common errors in the circuit JSON.
    Returns the corrected JSON.
    """
    if not isinstance(data, dict):
        return data

    corrected = data.copy()
    gates = corrected.get("gates", [])
    
    # 1. Map common gate name aliases
    alias_map = {
        "HADAMARD": "H",
        "CNOT": "CNOT",
        "CX": "CNOT",
        "CONTROLLED-NOT": "CNOT",
        "X-GATE": "X",
        "Y-GATE": "Y",
        "Z-GATE": "Z",
        "ROTATION-X": "RX",
        "ROTATION-Y": "RY",
        "ROTATION-Z": "RZ",
    }
    
    for gate in gates:
        g_type = str(gate.get("type", "")).upper()
        if g_type in alias_map:
            gate["type"] = alias_map[g_type]

    # 2. Ensure MEASURE gates exist if results are expected
    has_measure = any(g.get("type", "").upper() == "MEASURE" for g in gates)
    if not has_measure:
        num_qubits = corrected.get("qubits", 0)
        for i in range(num_qubits):
            gates.append({"type": "MEASURE", "target": i})
    
    # 3. Verify qubit count against used indices
    max_index = -1
    for gate in gates:
        target = gate.get("target", -1)
        control = gate.get("control", -1)
        max_index = max(max_index, target, control)
    
    if max_index >= corrected.get("qubits", 0):
        corrected["qubits"] = max_index + 1
        
    corrected["gates"] = gates
    return corrected
