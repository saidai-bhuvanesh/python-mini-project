import os
import ast
import json
import sys

def compute_complexity_metrics(file_path):
    """
    Statically analyzes python AST to compute complexity features:
    - LOC
    - Function count
    - Class count
    - Control flow branching nodes (to approximate cyclomatic complexity)
    """
    if not os.path.exists(file_path):
        return {"loc": 0, "functions": 0, "classes": 0, "complexity": 1}
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        lines = code.splitlines()
        loc = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
        
        tree = ast.parse(code, filename=file_path)
    except Exception:
        return {"loc": 0, "functions": 0, "classes": 0, "complexity": 1}
        
    functions = 0
    classes = 0
    branching_nodes = 1 # Base complexity is 1
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
        # Count control flow branching for cyclomatic complexity
        elif isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
            branching_nodes += 1
        elif isinstance(node, ast.BoolOp):
            branching_nodes += len(node.values) - 1
            
    return {
        "loc": loc,
        "functions": functions,
        "classes": classes,
        "complexity": branching_nodes
    }

def classify_project_difficulty(project_path):
    total_loc = 0
    total_funcs = 0
    total_classes = 0
    max_complexity = 1
    dep_count = 0
    
    # Check dependencies count
    meta_path = os.path.join(project_path, "metadata.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                dep_count = len(meta.get("dependencies", []))
        except Exception:
            pass
            
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py") and "tests" not in root:
                metrics = compute_complexity_metrics(os.path.join(root, file))
                total_loc += metrics["loc"]
                total_funcs += metrics["functions"]
                total_classes += metrics["classes"]
                max_complexity = max(max_complexity, metrics["complexity"])
                
    # Rules logic
    if total_loc <= 60 and max_complexity <= 6 and dep_count == 0:
        difficulty = "Beginner"
    elif total_loc <= 250 and max_complexity <= 15 and dep_count <= 2:
        difficulty = "Intermediate"
    else:
        difficulty = "Advanced"
        
    return {
        "loc": total_loc,
        "functions": total_funcs,
        "classes": total_classes,
        "max_complexity": max_complexity,
        "difficulty": difficulty
    }

def classify_all():
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
            report[item] = classify_project_difficulty(item_path)
            
    report_path = os.path.join(reports_dir, "complexity_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Difficulty classification completed. Saved to {report_path}")
    return report

if __name__ == "__main__":
    classify_all()
