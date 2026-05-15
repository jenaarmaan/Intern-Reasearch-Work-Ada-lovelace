import os
import subprocess
import time

def deploy_on_hf():
    print("🛸 Preparing Hugging Face Deployment...")
    
    # In HF Spaces, we want to run both the FastAPI backend and Next.js
    # However, HF Spaces usually expects a single entry point (like app.py)
    # We will use a proxy or just run the backend if they only want the API,
    # but for a "platform", we'll launch both.

    # 1. Install dependencies
    subprocess.run(["pip", "install", "-r", "backend/requirements.txt"])
    
    # 2. Launch Backend
    print("📡 Launching Backend...")
    backend_proc = subprocess.Popen(["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"])

    # 3. Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        backend_proc.terminate()

if __name__ == "__main__":
    deploy_on_hf()
