import os
import sys
import json
import pytest

# Append scripts directory to path to allow importing
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from register_projects import validate_metadata
from detect_broken_projects import check_syntax_and_imports
from search_engine import SearchEngine
from recommendation_engine import RecommendationEngine
from classify_difficulty import compute_complexity_metrics, classify_project_difficulty
from security_audit import audit_file_security
from learning_paths import LearningPathGenerator

# 1. Test Metadata Schema Validation
def test_validate_metadata():
    valid_data = {
        "name": "test_project",
        "description": "A test project description",
        "author": "Tester",
        "difficulty": "Beginner",
        "tags": ["testing", "unit"],
        "dependencies": ["pytest"],
        "entry_point": "main.py"
    }
    is_valid, msg = validate_metadata(valid_data)
    assert is_valid is True, f"Failed: {msg}"
    
    invalid_data = valid_data.copy()
    invalid_data["difficulty"] = "Super-Advanced" # Not in enum
    is_valid, msg = validate_metadata(invalid_data)
    assert is_valid is False
    
    missing_key = valid_data.copy()
    del missing_key["name"]
    is_valid, msg = validate_metadata(missing_key)
    assert is_valid is False

# 2. Test AST Parsing and Syntax Checks
def test_syntax_checker(tmp_path):
    # Valid python script
    valid_file = tmp_path / "valid.py"
    valid_file.write_text("def run():\n    print('Hello')\n")
    errors, imports = check_syntax_and_imports(str(valid_file), [])
    assert len(errors) == 0
    
    # Invalid python script (syntax error)
    invalid_file = tmp_path / "invalid.py"
    invalid_file.write_text("def run()\n    print('Hello')\n")
    errors, imports = check_syntax_and_imports(str(invalid_file), [])
    assert len(errors) > 0
    assert "SyntaxError" in errors[0]

# 3. Test Search Engine
def test_search_engine(tmp_path):
    # Mock registry
    reg_file = tmp_path / "registry.json"
    projects = [
        {"name": "calculator", "description": "basic arithmetic addition", "difficulty": "Beginner", "tags": ["math", "cli"]},
        {"name": "weather_cli", "description": "api tool", "difficulty": "Intermediate", "tags": ["weather", "api"]}
    ]
    reg_file.write_text(json.dumps(projects))
    
    engine = SearchEngine(str(reg_file))
    
    # Keyword search
    res = engine.search("math")
    assert len(res) == 1
    assert res[0]["name"] == "calculator"
    
    # Tag and difficulty filter
    res = engine.search("", tags=["api"], difficulty="Intermediate")
    assert len(res) == 1
    assert res[0]["name"] == "weather_cli"

# 4. Test Recommendation Engine
def test_recommendation_engine(tmp_path):
    reg_file = tmp_path / "registry.json"
    projects = [
        {"name": "calculator", "description": "arithmetic", "difficulty": "Beginner", "tags": ["math"]},
        {"name": "weather_cli", "description": "api", "difficulty": "Intermediate", "tags": ["weather"]}
    ]
    reg_file.write_text(json.dumps(projects))
    
    engine = RecommendationEngine(str(reg_file))
    profile = {"interests": ["math"], "skill_level": "Beginner"}
    
    recs = engine.get_recommendations(profile)
    assert len(recs) == 2
    assert recs[0]["project"]["name"] == "calculator" # Should rank first due to skill level & tags

# 5. Test Difficulty Classification
def test_complexity_metrics(tmp_path):
    file = tmp_path / "metrics.py"
    file.write_text("def f(x):\n    if x > 10:\n        return x\n    else:\n        return 0\n")
    metrics = compute_complexity_metrics(str(file))
    assert metrics["loc"] == 5
    assert metrics["functions"] == 1
    # Base is 1, plus 1 branch for 'If' = 2
    assert metrics["complexity"] == 2

# 6. Test Security Auditor
def test_security_auditor(tmp_path):
    # Dangerous eval usage
    insecure_file = tmp_path / "insecure.py"
    insecure_file.write_text("eval('print(123)')\n")
    vulns = audit_file_security(str(insecure_file))
    assert any("eval()" in v for v in vulns)
    
    # Clear file
    secure_file = tmp_path / "secure.py"
    secure_file.write_text("print('Safe execution')\n")
    vulns = audit_file_security(str(secure_file))
    assert len(vulns) == 0

# 7. Test Learning Paths topological sorting
def test_learning_paths(tmp_path):
    reg_file = tmp_path / "registry.json"
    projects = [
        {"name": "p1", "description": "A beginner math tool", "difficulty": "Beginner", "tags": ["math"]},
        {"name": "p2", "description": "An intermediate math app", "difficulty": "Intermediate", "tags": ["math"]}
    ]
    reg_file.write_text(json.dumps(projects))
    
    gen = LearningPathGenerator(str(reg_file))
    paths = gen.generate_paths()
    
    # p1 should precede p2 since it's Beginner and they share the 'math' tag
    seq = paths["master_sequence"]
    assert seq.index("p1") < seq.index("p2")
