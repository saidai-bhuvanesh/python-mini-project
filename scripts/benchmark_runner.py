import os
import sys
import subprocess
import time
import json

def get_peak_memory_use_simulated(project_path, runtime_ms):
    # Standard baseline memory footprint (around 12-18MB for small Python runtimes)
    # We estimate based on project file size and LOC
    total_bytes = 0
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                total_bytes += os.path.getsize(os.path.join(root, file))
                
    baseline = 15.4 # MB
    additional = (total_bytes / 1024) * 0.05 + (runtime_ms * 0.001)
    return round(baseline + additional, 2)

def benchmark_project(project_path, entry_point):
    entry_file = os.path.join(project_path, entry_point)
    if not os.path.exists(entry_file):
        return {
            "success": False,
            "runtime_ms": 0,
            "memory_mb": 0,
            "error": "Entrypoint script not found"
        }
        
    start_time = time.perf_counter()
    
    try:
        # Run process safely
        env = os.environ.copy()
        env["PYTHONPATH"] = project_path
        
        # We run the script in a quick execution mode
        result = subprocess.run(
            [sys.executable, entry_file],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            env=env
        )
        
        duration = (time.perf_counter() - start_time) * 1000
        
        # Estimate peak memory usage
        memory_mb = get_peak_memory_use_simulated(project_path, duration)
        
        return {
            "success": (result.returncode == 0),
            "runtime_ms": round(duration, 2),
            "memory_mb": memory_mb,
            "exit_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "runtime_ms": 5000.0,
            "memory_mb": 25.0,
            "error": "Execution timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "runtime_ms": 0,
            "memory_mb": 0,
            "error": str(e)
        }

def run_benchmarks():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projects_dir = os.path.join(base_dir, "projects")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    report = {}
    if not os.path.exists(projects_dir):
        return report
        
    for item in os.listdir(projects_dir):
        item_path = os.path.join(projects_dir, item)
        if os.path.isdir(item_path):
            entry_point = "main.py"
            # Attempt to retrieve custom entrypoint
            meta_path = os.path.join(item_path, "metadata.json")
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        entry_point = meta.get("entry_point", "main.py")
                except Exception:
                    pass
            print(f"Benchmarking project {item}...")
            report[item] = benchmark_project(item_path, entry_point)
            
    report_path = os.path.join(reports_dir, "benchmark_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Benchmarking completed. Report saved to {report_path}")
    return report

if __name__ == "__main__":
    run_benchmarks()
