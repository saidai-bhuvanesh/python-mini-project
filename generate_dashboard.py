import os
import sys
import json
import subprocess
import time

def run_script(script_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "scripts", script_name)
    if not os.path.exists(script_path):
        print(f"[-] Script not found: {script_name}")
        return False
    print(f"[*] Running diagnostics: {script_name}...")
    try:
        # Run using python subprocess
        res = subprocess.run(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        if res.returncode == 0:
            print(f"[+] Successfully finished: {script_name}")
            return True
        else:
            print(f"[-] Failed: {script_name} (Exit code: {res.returncode})")
            print(res.stderr)
            return False
    except Exception as e:
        print(f"[-] Error executing {script_name}: {e}")
        return False

def build_health_registry():
    print("=" * 60)
    print(" PYTHON MINI PROJECT HUB 2.0 - REPOSITORY DIAGNOSTIC AGGREGATOR ".center(60, "="))
    print("=" * 60)
    
    # 1. First scan and register projects
    if not run_script("register_projects.py"):
        print("[-] Registry compilation failed. Aborting build.")
        sys.exit(1)
        
    # 2. Run all analyzers in sequence
    analyzers = [
        "detect_broken_projects.py",
        "analyze_dependencies.py",
        "lint_scanner.py",
        "run_tests.py",
        "security_audit.py",
        "benchmark_runner.py",
        "learning_paths.py",
        "analyze_contributors.py"
    ]
    
    success_count = 0
    for analyzer in analyzers:
        if run_script(analyzer):
            success_count += 1
            
    print("-" * 60)
    print(f"[*] Dashboard compilation complete: {success_count}/{len(analyzers)} analyzers successfully run.")
    print("-" * 60)
    
    # 3. Read statistics and render a clean CLI summary
    base_dir = os.path.dirname(os.path.abspath(__file__))
    registry_file = os.path.join(base_dir, "projects_registry.json")
    
    projects_count = 0
    if os.path.exists(registry_file):
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                projects_count = len(json.load(f))
        except Exception:
            pass
            
    print(f"Summary metrics:")
    print(f"  * Total Registered Projects: {projects_count}")
    
    # Read broken projects report
    broken_report = os.path.join(base_dir, "reports", "broken_projects_report.json")
    if os.path.exists(broken_report):
        try:
            with open(broken_report, "r", encoding="utf-8") as f:
                data = json.load(f)
                broken = len([p for p in data.values() if p["status"] == "Broken"])
                warning = len([p for p in data.values() if p["status"] == "Warning"])
                healthy = len([p for p in data.values() if p["status"] == "Healthy"])
                print(f"  * Diagnostics: {healthy} Healthy, {warning} Warnings, {broken} Broken")
        except Exception:
            pass
            
    print("=" * 60)
    print("To explore interactively:")
    print("  1. Run the interactive CLI Dashboard: 'python generate_dashboard.py --cli'")
    print("  2. Open the modern Web Hub: 'dashboard/index.html' in your browser.")
    print("=" * 60)

def show_cli_dashboard():
    # Interactive CLI Menu
    base_dir = os.path.dirname(os.path.abspath(__file__))
    registry_path = os.path.join(base_dir, "projects_registry.json")
    
    if not os.path.exists(registry_path):
        print("[-] registry files not found. Run 'python generate_dashboard.py' first to initialize.")
        sys.exit(1)
        
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            projects = json.load(f)
    except Exception as e:
        print(f"[-] Failed to read registry: {e}")
        sys.exit(1)
        
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" PYTHON MINI PROJECT HUB 2.0 - ROADMAP DASHBOARD ".center(60, "="))
        print("=" * 60)
        print("Select a project to view metrics & diagnostics details:\n")
        
        for idx, p in enumerate(projects):
            print(f" [{idx + 1:02d}] {p['name']} ({p['difficulty']})")
        print("\n [Q] Quit dashboard")
        print("=" * 60)
        
        choice = input("Enter choice: ").strip()
        if choice.lower() == 'q':
            print("Goodbye!")
            break
            
        try:
            num = int(choice)
            if 1 <= num <= len(projects):
                p = projects[num - 1]
                show_project_details(p)
            else:
                input("Invalid index. Press Enter to continue...")
        except ValueError:
            input("Invalid choice. Press Enter to continue...")

def show_project_details(p):
    os.system('cls' if os.name == 'nt' else 'clear')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    name = p["name"]
    
    print("=" * 60)
    print(f" PROJECT DETAILS: {name.upper()} ".center(60, "="))
    print("=" * 60)
    print(f"\nDescription:\n  {p['description']}\n")
    print(f"Author: {p.get('author', 'Anonymous')}")
    print(f"Entrypoint: {p.get('entry_point', 'main.py')}")
    print(f"Tags: {', '.join(p.get('tags', []))}")
    print(f"Dependencies: {', '.join(p.get('dependencies', [])) or 'None'}")
    print("\n" + "-" * 60)
    
    # Load test stats
    test_path = os.path.join(base_dir, "reports", "test_report.json")
    if os.path.exists(test_path):
        try:
            with open(test_path, "r", encoding="utf-8") as f:
                tests = json.load(f).get(name, {})
                if tests.get("ran"):
                    print(f"Unit Tests: {tests['passed']}/{tests['total']} Passed ({tests['pass_rate']}% rate) | Coverage: {tests['coverage']}%")
                else:
                    print(f"Unit Tests: No tests run. Reason: {tests.get('error', 'None')}")
        except Exception:
            pass
            
    # Load lint stats
    lint_path = os.path.join(base_dir, "reports", "lint_report.json")
    if os.path.exists(lint_path):
        try:
            with open(lint_path, "r", encoding="utf-8") as f:
                lint = json.load(f).get(name, {})
                print(f"Code Style Quality: Score {lint.get('score', 100)}% (Grade {lint.get('grade', 'A')})")
        except Exception:
            pass
            
    # Load benchmark stats
    bench_path = os.path.join(base_dir, "reports", "benchmark_report.json")
    if os.path.exists(bench_path):
        try:
            with open(bench_path, "r", encoding="utf-8") as f:
                bench = json.load(f).get(name, {})
                if bench.get("success"):
                    print(f"Execution Benchmarks: Speed: {bench['runtime_ms']}ms | Peak Memory: {bench['memory_mb']}MB")
        except Exception:
            pass
            
    print("=" * 60)
    input("Press Enter to return to project list...")

if __name__ == "__main__":
    if "--cli" in sys.argv:
        show_cli_dashboard()
    else:
        build_health_registry()
