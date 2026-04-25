from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_engine import generate_circuit_json
from services.quantum_engine import build_and_simulate_circuit
from services.validator import validate_circuit_json, correct_circuit_json
import os

app = FastAPI(title="AQC-GA Backend", description="AI-Powered Quantum Circuit Generation API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def health_check():
    return {"status": "online", "message": "AQC-GA Backend is running"}

@app.post("/generate")
async def generate_circuit(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # 1. Generate JSON from AI
    circuit_json = generate_circuit_json(request.prompt)
    
    if "error" in circuit_json:
        return {
            "success": False,
            "error": circuit_json["error"],
            "stage": "AI_GENERATION"
        }
    
    # 2. Correct and Validate Circuit
    circuit_json = correct_circuit_json(circuit_json)
    
    is_valid, validation_error = validate_circuit_json(circuit_json)
    if not is_valid:
        return {
            "success": False,
            "error": validation_error,
            "stage": "VALIDATION",
            "circuit_json": circuit_json
        }
    
    # 3. Build and Simulate Circuit
    execution_result = build_and_simulate_circuit(circuit_json)
    
    if not execution_result["success"]:
        return {
            "success": False,
            "error": execution_result["error"],
            "stage": "QUANTUM_EXECUTION",
            "circuit_json": circuit_json
        }
    
    return {
        "success": True,
        "prompt": request.prompt,
        "circuit_json": circuit_json,
        "results": execution_result["counts"],
        "metrics": execution_result["metrics"],
        "qasm": execution_result["qasm"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
