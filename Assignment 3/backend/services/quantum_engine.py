from qiskit import QuantumCircuit, transpile
import json

# Try to import high-performance Aer, fallback to basic Python simulator if blocked
try:
    from qiskit_aer import AerSimulator
    HAS_AER = True
except (ImportError, Exception):
    from qiskit.providers.basic_provider import BasicSimulator
    HAS_AER = False

def build_and_simulate_circuit(circuit_data):
    """
    Takes structured JSON circuit data and returns simulation results.
    Uses high-performance Aer if available, otherwise falls back to pure Python simulator.
    """
    try:
        num_qubits = circuit_data.get("qubits", 1)
        qc = QuantumCircuit(num_qubits, num_qubits)
        
        gates = circuit_data.get("gates", [])
        
        for gate in gates:
            gate_type = gate.get("type").upper()
            target = gate.get("target")
            control = gate.get("control")
            params = gate.get("params", [])
            
            if gate_type == "H":
                qc.h(target)
            elif gate_type == "X":
                qc.x(target)
            elif gate_type == "Y":
                qc.y(target)
            elif gate_type == "Z":
                qc.z(target)
            elif gate_type == "S":
                qc.s(target)
            elif gate_type == "T":
                qc.t(target)
            elif gate_type == "CNOT":
                if control is not None:
                    qc.cx(control, target)
            elif gate_type == "RX":
                if params:
                    qc.rx(params[0], target)
            elif gate_type == "RY":
                if params:
                    qc.ry(params[0], target)
            elif gate_type == "RZ":
                if params:
                    qc.rz(params[0], target)
            elif gate_type == "MEASURE":
                qc.measure(target, target)

        # Choose Simulator
        if HAS_AER:
            simulator = AerSimulator()
            method = "Aer (C++)"
        else:
            simulator = BasicSimulator()
            method = "Basic (Python Fallback)"

        compiled_circuit = transpile(qc, simulator)
        job = simulator.run(compiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        # Performance Metrics
        gate_counts = qc.count_ops()
        metrics = {
            "depth": qc.depth(),
            "gate_count": sum(gate_counts.values()),
            "qubits": num_qubits,
            "width": qc.width(),
            "gate_distribution": dict(gate_counts),
            "sim_method": method
        }
        
        return {
            "success": True,
            "counts": counts,
            "metrics": metrics,
            "qasm": qc.qasm() if hasattr(qc, 'qasm') else "N/A",
            "diagram": qc.draw('text').__str__()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
