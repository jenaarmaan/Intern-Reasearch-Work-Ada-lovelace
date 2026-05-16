import subprocess
import time
import os
import sys

def launch_platform():
    print("Starting Luminary AI Platform...")
    
    # 1. Start Backend
    print("Starting Backend Engine (Port 8000)...")
    backend_proc = subprocess.Popen(
        ["python", "backend/main.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        shell=True
    )
    
    # 2. Start Frontend
    print("Starting Frontend Interface (Port 3000)...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend"),
        shell=True
    )
    
    print("\nPlatform is coming online!")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:3000")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down platform...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    launch_platform()
