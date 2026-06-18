import os
import sys
import subprocess
import time
import json

def run_in_sandbox(script_path, args=None, timeout_seconds=3):
    """
    Safely executes a Python script in a subprocess sandbox.
    Restricts runtime duration to prevent hang-ups, captures outputs.
    """
    if not os.path.exists(script_path):
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Script file not found.",
            "duration_ms": 0
        }
        
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
        
    start_time = time.time()
    
    try:
        # Run subprocess with clean environment to enforce safety boundaries
        clean_env = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
            "PYTHONPATH": os.path.dirname(script_path)
        }
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=clean_env,
            timeout=timeout_seconds
        )
        
        duration = (time.time() - start_time) * 1000
        return {
            "success": (result.returncode == 0),
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_ms": round(duration, 2)
        }
        
    except subprocess.TimeoutExpired:
        duration = (time.time() - start_time) * 1000
        return {
            "success": False,
            "exit_code": -9,
            "stdout": "",
            "stderr": f"Process exceeded time limit of {timeout_seconds} seconds.",
            "duration_ms": round(duration, 2)
        }
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        return {
            "success": False,
            "exit_code": -2,
            "stdout": "",
            "stderr": f"Execution error: {e}",
            "duration_ms": round(duration, 2)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sandbox_runner.py <script_path> [args...]")
        sys.exit(1)
        
    target_script = sys.argv[1]
    passed_args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    res = run_in_sandbox(target_script, passed_args)
    print(json.dumps(res, indent=2))
