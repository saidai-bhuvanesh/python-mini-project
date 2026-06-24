import os
import json
import ast
import sys

def check_syntax_and_imports(file_path, dependencies):
    """
    Parses a python file with AST to find syntax errors and track imported modules.
    """
    if not os.path.exists(file_path):
        return ["File not found"], []
        
    errors = []
    imports = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code, filename=file_path)
    except SyntaxError as se:
        return [f"SyntaxError on line {se.lineno}: {se.msg}"], []
    except Exception as e:
        return [f"Error reading/parsing file: {e}"], []
        
    # Analyze imports using AST node visitor
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
                
    # Check if imports are either stdlib or declared in dependencies
    # We will just verify local modules or standard packages
    # For now, collect imports to report
    return errors, list(set(imports))

def scan_health():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projects_dir = os.path.join(base_dir, "projects")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    report = {}
    
    if not os.path.exists(projects_dir):
        return report

    for item in os.listdir(projects_dir):
        item_path = os.path.join(projects_dir, item)
        if not os.path.isdir(item_path):
            continue
            
        score = 100
        issues = []
        imports_found = []
        
        # Check files
        meta_exists = os.path.exists(os.path.join(item_path, "metadata.json"))
        readme_exists = os.path.exists(os.path.join(item_path, "README.md"))
        tests_exists = os.path.exists(os.path.join(item_path, "tests"))
        
        if not meta_exists:
            score -= 50
            issues.append("Missing metadata.json")
            
        if not readme_exists:
            score -= 20
            issues.append("Missing README.md")
            
        if not tests_exists:
            score -= 10
            issues.append("Missing tests/ directory")
            
        # Parse metadata details if it exists
        entry_point = "main.py"
        declared_deps = []
        
        if meta_exists:
            try:
                with open(os.path.join(item_path, "metadata.json"), "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    entry_point = meta.get("entry_point", "main.py")
                    declared_deps = meta.get("dependencies", [])
            except Exception:
                score -= 15
                issues.append("Invalid metadata.json format")
                
        # Validate Entry point execution
        entry_path = os.path.join(item_path, entry_point)
        if not os.path.exists(entry_path):
            score -= 30
            issues.append(f"Entrypoint file '{entry_point}' not found")
        else:
            syntax_errors, file_imports = check_syntax_and_imports(entry_path, declared_deps)
            if syntax_errors:
                score -= 25
                issues.extend([f"Syntax error in {entry_point}: {err}" for err in syntax_errors])
            imports_found.extend(file_imports)
            
        # Keep score inside 0-100 bounds
        score = max(0, min(100, score))
        
        report[item] = {
            "name": item,
            "health_score": score,
            "status": "Healthy" if score >= 80 else "Warning" if score >= 50 else "Broken",
            "issues": issues,
            "imports": imports_found
        }
        
    report_path = os.path.join(reports_dir, "broken_projects_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Health audit completed. Reports written to {report_path}")
    return report

if __name__ == "__main__":
    scan_health()
