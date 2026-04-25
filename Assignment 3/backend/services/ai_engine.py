import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

SYSTEM_PROMPT = """
You are a Quantum Circuit Architect. Your task is to translate natural language descriptions of quantum experiments into a structured JSON format that can be parsed into a Qiskit circuit.

### Output JSON Schema:
{
  "qubits": int,
  "gates": [
    {
      "type": "string",  // Supported: H, X, Y, Z, CNOT, S, T, RX, RY, RZ, MEASURE
      "target": int,
      "control": int,    // Required only for CNOT
      "params": [float]  // Required only for rotation gates (RX, RY, RZ) in radians
    }
  ]
}

### Rules:
1. Return ONLY the JSON object. No markdown, no explanations.
2. Qubit indices must start at 0.
3. For a Bell State, use H on qubit 0 and CNOT with control 0 and target 1.
4. For multi-qubit gates like CNOT, always specify 'control' and 'target'.
5. If the user wants to measure, include "MEASURE" gates for all relevant qubits.
6. Ensure the number of 'qubits' matches the highest index used in 'gates'.

### Examples:
User: "Create a Bell State"
Output: {"qubits": 2, "gates": [{"type": "H", "target": 0}, {"type": "CNOT", "control": 0, "target": 1}, {"type": "MEASURE", "target": 0}, {"type": "MEASURE", "target": 1}]}

User: "Apply Hadamard to qubit 0 and then a rotation of pi/2 around X on qubit 1"
Output: {"qubits": 2, "gates": [{"type": "H", "target": 0}, {"type": "RX", "target": 1, "params": [1.570796]}, {"type": "MEASURE", "target": 0}, {"type": "MEASURE", "target": 1}]}
"""

def generate_circuit_json(prompt: str):
    if not GENAI_API_KEY:
        # Fallback for testing if API key is missing
        if "bell" in prompt.lower():
            return {"qubits": 2, "gates": [{"type": "H", "target": 0}, {"type": "CNOT", "control": 0, "target": 1}, {"type": "MEASURE", "target": 0}, {"type": "MEASURE", "target": 1}]}
        return {"error": "API Key not configured"}

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser Prompt: {prompt}")
    
    try:
        # Clean response text in case of accidental markdown
        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_json)
    except Exception as e:
        return {"error": f"Failed to parse AI output: {str(e)}", "raw": response.text}
