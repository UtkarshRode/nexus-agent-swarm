import subprocess
import sys
import os
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SERVER_DIR = BASE_DIR / "server"
CLIENT_DIR = BASE_DIR / "client"

def main():
    print("\n=============================================================")
    print("🤖 NEXUS-SWARM: MULTI-AGENT ORCHESTRATION PLATFORM")
    print("⚡ Starting Python FastAPI Backend & React Client...")
    print("=============================================================\n")

    is_windows = sys.platform == "win32"
    npm_cmd = "npm.cmd" if is_windows else "npm"

    # 1. Start FastAPI backend
    print("📦 Launching FastAPI Backend (Port 8000)...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=str(SERVER_DIR),
        shell=False,
    )

    # 2. Start Vite Frontend
    print("⚡ Launching React Vite Frontend (Port 5173)...")
    client_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(CLIENT_DIR),
        shell=is_windows,
    )

    print("\n✅ NexusSwarm Active!")
    print("👉 Frontend: http://localhost:5173")
    print("👉 API Docs: http://localhost:8000/docs")
    print("Press Ctrl+C to terminate both servers.\n")

    try:
        while True:
            time.sleep(1)
            if server_process.poll() is not None:
                print("Server exited unexpectedly.")
                break
            if client_process.poll() is not None:
                print("Client exited unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\n🛑 Shutting down NexusSwarm...")
    finally:
        server_process.terminate()
        client_process.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
