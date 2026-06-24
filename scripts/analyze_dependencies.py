import os
import json
import ast
import sys

# Standard library module names in Python 3.8+ to distinguish from third-party imports
STD_LIBS = sys.builtin_module_names

def get_stdlib_modules():
    # Build standard library list using standard references
    import distutils.sysconfig as sysconfig
    import glob
    std_modules = set(sys.builtin_module_names)
    stdlib_path = sysconfig.get_python_lib(standard_lib=True)
    for path in glob.glob(os.path.join(stdlib_path, "*.py")):
        name = os.path.basename(path).split(".")[0]
        std_modules.add(name)
    for path in glob.glob(os.path.join(stdlib_path, "*", "__init__.py")):
        name = os.path.basename(os.path.dirname(path))
        std_modules.add(name)
    # Common built-in aliases
    std_modules.update(["os", "sys", "time", "math", "re", "json", "ast", "subprocess", 
                        "collections", "shutil", "datetime", "hashlib", "urllib", 
                        "unittest", "pytest", "mock", "patch", "argparse", "logging"])
    return std_modules

def analyze_project_dependencies(project_path):
    std_modules = get_stdlib_modules()
    
    # Read declared dependencies
    declared = set()
    meta_path = os.path.join(project_path, "metadata.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                declared.update(meta.get("dependencies", []))
        except Exception:
            pass
            
    reqs_path = os.path.join(project_path, "requirements.txt")
    if os.path.exists(reqs_path):
        try:
            with open(reqs_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Parse package name (e.g., requests>=2.25.0 -> requests)
                        pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].strip()
                        declared.add(pkg)
        except Exception:
            pass
            
    # Gather actual imports in python files
    imported = set()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for name in node.names:
                                imported.add(name.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imported.add(node.module.split('.')[0])
                except Exception:
                    pass
                    
    # Map common package import aliases (e.g. pyyaml -> yaml)
    import_aliases = {
        "yaml": "pyyaml",
        "PIL": "pillow",
        "bs4": "beautifulsoup4"
    }
    
    normalized_imported = set()
    for imp in imported:
        normalized_imported.add(import_aliases.get(imp, imp))
        
    # Analyze difference
    # Third party packages imported but NOT declared
    # Exclusion list: ignore std_libs, self-imports (project directory files)
    local_modules = {os.path.basename(f).split(".")[0] for f in os.listdir(project_path) if f.endswith(".py")}
    local_modules.add("tests")
    local_modules.add("main")
    
    undeclared = []
    for imp in normalized_imported:
        if imp not in std_modules and imp not in local_modules and imp not in declared:
            undeclared.append(imp)
            
    unused = []
    # Declared but never imported in code
    for dec in declared:
        # Check standard name and alias representation
        reverse_aliases = [k for k, v in import_aliases.items() if v == dec]
        possible_names = [dec] + reverse_aliases
        if not any(name in imported for name in possible_names):
            unused.append(dec)
            
    return {
        "declared": list(declared),
        "imported_third_party": [imp for imp in normalized_imported if imp not in std_modules and imp not in local_modules],
        "unused": unused,
        "undeclared": undeclared
    }

def audit_all_dependencies():
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
            report[item] = analyze_project_dependencies(item_path)
            
    report_path = os.path.join(reports_dir, "dependency_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Dependency analysis completed. Saved to {report_path}")
    return report

if __name__ == "__main__":
    audit_all_dependencies()
