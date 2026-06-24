import os
import ast
import json
import re
import sys

# Regex pattern to detect common hardcoded credentials / tokens
SECRET_PATTERN = re.compile(r"(api_key|secret|password|token|credentials)\s*=\s*['\"][a-zA-Z0-9_\-\+\/]{8,}['\"]", re.IGNORECASE)

def audit_file_security(file_path):
    violations = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return [f"Could not read file: {e}"]
        
    # 1. Regex credential scanning
    matches = SECRET_PATTERN.findall(code)
    if matches:
        for match in matches:
            violations.append(f"Potential hardcoded credential or secret key variable: {match}")
            
    # 2. AST parsing to inspect function calls and imports
    try:
        tree = ast.parse(code, filename=file_path)
        for node in ast.walk(tree):
            # Check for eval() and exec()
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["eval", "exec"]:
                        violations.append(f"Line {node.lineno}: Dangerous builtin function '{node.func.id}()' used")
                        
                # Check for subprocess.run/Popen with shell=True
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in ["run", "Popen", "call", "check_output"]:
                        # Look for shell=True kwarg
                        for kw in node.keywords:
                            if kw.arg == "shell":
                                if isinstance(kw.value, ast.NameConstant) and kw.value.value is True:
                                    violations.append(f"Line {node.lineno}: subprocess called with shell=True which exposes to shell injections")
                                    
            # Check for insecure imports
            elif isinstance(node, ast.Import):
                for name in node.names:
                    if name.name == "random":
                        violations.append(f"Import of standard 'random' module (insecure for cryptography/security secrets)")
    except Exception:
        pass
        
    return violations

def audit_project_security(project_path):
    all_vulns = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py") and "tests" not in root:
                vulns = audit_file_security(os.path.join(root, file))
                all_vulns.extend([f"{file}: {v}" for v in vulns])
                
    severity = "Secure"
    score = 100
    
    if all_vulns:
        score = max(20, 100 - len(all_vulns) * 20)
        severity = "High" if len(all_vulns) >= 3 else "Medium"
        
    return {
        "security_score": score,
        "severity": severity,
        "vulnerabilities": all_vulns
    }

def run_security_audit():
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
            report[item] = audit_project_security(item_path)
            
    report_path = os.path.join(reports_dir, "security_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Security audit completed. Report saved to {report_path}")
    return report

if __name__ == "__main__":
    run_security_audit()
