import subprocess
import time
import os
import sys

def print_status(message):
    print(f"--- {message} ---")

if __name__ == "__main__":
    print_status("Rendszer indítása...")

    # Backend 
    print_status("Backend indítása (Port: 8000)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        env=os.environ.copy()
    )

    time.sleep(3)

    # Frontend
    print_status("Frontend indítása...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        env=os.environ.copy()
    )

    print_status("Minden fut! Nyomj CTRL+C-t a leállításhoz.")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print_status("Leállítás folyamatban...")
        backend_process.terminate()
        frontend_process.terminate()
        print_status("Viszlát!")