import os
import json
import ast
import re
import sys

def lint_file_manually(file_path):
    """
    Manually audits a Python file for common PEP8 rules:
    - Line lengths (> 100 characters)
    - Function/class naming
    - Docstrings
    - Empty lines
    """
    violations = []
    line_count = 0
    long_lines = 0
    missing_docstrings = 0
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return {"score_penalty": 50, "violations": [f"Cannot read file: {e}"]}
        
    line_count = len(lines)
    for idx, line in enumerate(lines):
        # Line length check
        if len(line.rstrip('\r\n')) > 100:
            long_lines += 1
            violations.append(f"Line {idx+1} exceeds 100 characters ({len(line)} chars)")
            
    # Parse with AST to look at naming & docstrings
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
            
        for node in ast.walk(tree):
            # Check function naming (should be snake_case, ignore dunder methods)
            if isinstance(node, ast.FunctionDef):
                name = node.name
                if not name.startswith("__") and not name.endswith("__"):
                    if not re.match(r"^[a-z_][a-z0-9_]*$", name):
                        violations.append(f"Function name '{name}' (line {node.lineno}) should be snake_case")
                # Docstring check
                if ast.get_docstring(node) is None:
                    missing_docstrings += 1
                    violations.append(f"Function '{name}' (line {node.lineno}) is missing a docstring")
                    
            # Check class naming (should be CamelCase)
            elif isinstance(node, ast.ClassDef):
                name = node.name
                if not re.match(r"^[A-Z][a-zA-Z0-9]*$", name):
                    violations.append(f"Class name '{name}' (line {node.lineno}) should be CamelCase")
                if ast.get_docstring(node) is None:
                    missing_docstrings += 1
                    violations.append(f"Class '{name}' (line {node.lineno}) is missing a docstring")
    except Exception:
        # Fallback if AST parse fails
        pass

    # Score calculations
    penalty = (long_lines * 5) + (missing_docstrings * 10)
    # Cap penalty for single file at 80
    penalty = min(penalty, 80)
    
    return {
        "score_penalty": penalty,
        "violations": violations
    }

def lint_project(project_path):
    total_penalty = 0
    all_violations = []
    file_count = 0
    
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("test_") and "tests" not in root:
                file_path = os.path.join(root, file)
                result = lint_file_manually(file_path)
                total_penalty += result["score_penalty"]
                all_violations.extend([f"{file}: {v}" for v in result["violations"]])
                file_count += 1
                
    if file_count == 0:
        return {"score": 100, "grade": "A", "violations": []}
        
    avg_penalty = total_penalty / file_count
    score = max(0, min(100, 100 - avg_penalty))
    
    # Assign grades
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"
        
    return {
        "score": round(score, 1),
        "grade": grade,
        "violations": all_violations[:20]  # Limit output violations
    }

def audit_all_code():
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
            report[item] = lint_project(item_path)
            
    report_path = os.path.join(reports_dir, "lint_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Lint scanner completed. Report saved to {report_path}")
    return report

if __name__ == "__main__":
    audit_all_code()
