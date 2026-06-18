import os
import json
import sys

def validate_metadata(data):
    """
    Validates dictionary against standards/project_schema.json logic.
    We do this using a native validator to guarantee zero dependencies.
    """
    required_keys = ["name", "description", "difficulty", "tags", "entry_point"]
    for key in required_keys:
        if key not in data:
            return False, f"Missing required key: {key}"
    
    if not isinstance(data["name"], str) or not data["name"].strip():
        return False, "Key 'name' must be a non-empty string"
        
    if not isinstance(data["description"], str) or not data["description"].strip():
        return False, "Key 'description' must be a non-empty string"
        
    if data["difficulty"] not in ["Beginner", "Intermediate", "Advanced"]:
        return False, "Key 'difficulty' must be one of: Beginner, Intermediate, Advanced"
        
    if not isinstance(data["tags"], list) or not all(isinstance(t, str) for t in data["tags"]):
        return False, "Key 'tags' must be a list of strings"
        
    if not isinstance(data["entry_point"], str) or not data["entry_point"].strip():
        return False, "Key 'entry_point' must be a non-empty string"
        
    if "dependencies" in data:
        if not isinstance(data["dependencies"], list) or not all(isinstance(d, str) for d in data["dependencies"]):
            return False, "Key 'dependencies' must be a list of strings"
            
    return True, "Valid"

def scan_and_register():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projects_dir = os.path.join(base_dir, "projects")
    registry_file = os.path.join(base_dir, "projects_registry.json")
    
    registry = []
    errors = []
    
    if not os.path.exists(projects_dir):
        print(f"Projects directory not found at {projects_dir}")
        sys.exit(1)
        
    for item in sorted(os.listdir(projects_dir)):
        item_path = os.path.join(projects_dir, item)
        if os.path.isdir(item_path):
            meta_path = os.path.join(item_path, "metadata.json")
            if not os.path.exists(meta_path):
                errors.append(f"Project '{item}' is missing metadata.json")
                continue
                
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta_data = json.load(f)
            except Exception as e:
                errors.append(f"Project '{item}' has invalid JSON in metadata.json: {e}")
                continue
                
            is_valid, msg = validate_metadata(meta_data)
            if not is_valid:
                errors.append(f"Project '{item}' metadata validation failed: {msg}")
                continue
                
            # Verify entry_point exists
            entry_file = os.path.join(item_path, meta_data["entry_point"])
            if not os.path.exists(entry_file):
                errors.append(f"Project '{item}' entrypoint file not found: {meta_data['entry_point']}")
                continue
                
            # Register project info
            meta_data["path"] = f"projects/{item}"
            meta_data["relative_entry"] = f"projects/{item}/{meta_data['entry_point']}"
            registry.append(meta_data)
            
    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
        
    print(f"Successfully registered {len(registry)} projects in projects_registry.json")
    if errors:
        print("\nWarnings / Errors detected:")
        for err in errors:
            print(f" - {err}")
            
    return registry, errors

if __name__ == "__main__":
    scan_and_register()
