import subprocess
import os
import signal

def run_backend():
    backend_dir = os.path.join(os.getcwd(), "backend")
    conda_env = os.path.join(os.getcwd(), ".conda")
    print(f"Starting backend in: {backend_dir}")
    print(f"Using conda environment: {conda_env}")
    
    # Use conda environment's Python
    conda_python = os.path.join(conda_env, "Scripts", "python.exe")
    conda_uvicorn = os.path.join(conda_env, "Scripts", "uvicorn.exe")
    
    # Try uvicorn executable first, fallback to python -m uvicorn
    if os.path.exists(conda_uvicorn):
        cmd = [conda_uvicorn, "app.main:app", "--reload"]
    else:
        cmd = [conda_python, "-m", "uvicorn", "app.main:app", "--reload"]
    
    return subprocess.Popen(
        cmd,
        cwd=backend_dir,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def run_frontend():
    npm_path = "C:\\Program Files\\nodejs\\npm.cmd"
    frontend_dir = os.path.join(os.getcwd(), "mental-health-frontend")
    print(f"Starting frontend in: {frontend_dir}")
    if not os.path.exists(frontend_dir):
        raise FileNotFoundError(f"Frontend directory not found: {frontend_dir}")
    return subprocess.Popen(
        [npm_path, "run", "dev"],
        cwd=frontend_dir,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def main():
    backend_process = None
    frontend_process = None

    try:
        backend_process = run_backend()
        frontend_process = run_frontend()
        backend_process.wait()
        frontend_process.wait()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    except KeyboardInterrupt:
        print("\nShutting down...")
        if backend_process:
            backend_process.send_signal(signal.SIGINT)
        if frontend_process:
            frontend_process.send_signal(signal.SIGINT)
        if backend_process:
            backend_process.wait()
        if frontend_process:
            frontend_process.wait()

if __name__ == "__main__":
    main()