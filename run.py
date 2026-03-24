import subprocess
import sys
import signal
import time

def run_backend():
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

def run_frontend():
    return subprocess.Popen(
        ["streamlit", "run", "ui.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

def terminate_process(proc, name):
    if proc and proc.poll() is None:
        print(f"🛑 Terminating {name}...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"⚠️ {name} did not terminate in time, killing...")
            proc.kill()

if __name__ == "__main__":
    print("🚀 Starting FastAPI + Streamlit...")

    backend = run_backend()
    frontend = run_frontend()

    # Handle Ctrl+C safely
    def handle_exit(signum, frame):
        print("\n🔔 Exit signal received.")
        terminate_process(backend, "Backend")
        terminate_process(frontend, "Frontend")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    try:
        # Monitor both processes
        while True:
            if backend.poll() is not None:
                print("⚠️ Backend exited unexpectedly.")
                terminate_process(frontend, "Frontend")
                break
            if frontend.poll() is not None:
                print("⚠️ Frontend exited unexpectedly.")
                terminate_process(backend, "Backend")
                break
            time.sleep(1)
    finally:
        terminate_process(backend, "Backend")
        terminate_process(frontend, "Frontend")
        print("✅ Shutdown complete.")