import os
import json
import sys

def generate_readme(project_path, force=False):
    readme_path = os.path.join(project_path, "README.md")
    meta_path = os.path.join(project_path, "metadata.json")
    
    if os.path.exists(readme_path) and not force:
        return False, "README.md already exists. Use force=True to overwrite."
        
    if not os.path.exists(meta_path):
        return False, "metadata.json not found. Cannot generate README."
        
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        return False, f"Failed to parse metadata.json: {e}"
        
    name = meta.get("name", os.path.basename(project_path))
    desc = meta.get("description", "A Python mini project.")
    difficulty = meta.get("difficulty", "Beginner")
    tags = ", ".join(meta.get("tags", []))
    entry = meta.get("entry_point", "main.py")
    
    # Read requirements if present
    reqs_str = ""
    reqs_path = os.path.join(project_path, "requirements.txt")
    if os.path.exists(reqs_path):
        reqs_str = "\n## Dependencies\nInstall dependencies via requirements.txt:\n```bash\npip install -r requirements.txt\n```\n"
    elif meta.get("dependencies"):
        reqs_str = f"\n## Dependencies\nRequires the following packages:\n" + "\n".join([f"- {d}" for d in meta["dependencies"]]) + "\n"

    content = f"""# {name.capitalize()}

{desc}

---

*   **Difficulty**: {difficulty}
*   **Tags**: {tags}

## Getting Started

### Run the Project
Ensure you have Python installed, then run the entry script:
```bash
python {entry}
```
{reqs_str}
## Running Tests
Run unit tests within the project directory:
```bash
pytest tests/
```
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return True, "README.md generated successfully."

def auto_generate_all(force=False):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projects_dir = os.path.join(base_dir, "projects")
    
    if not os.path.exists(projects_dir):
        print("Projects directory not found.")
        sys.exit(1)
        
    generated_count = 0
    for item in os.listdir(projects_dir):
        item_path = os.path.join(projects_dir, item)
        if os.path.isdir(item_path):
            readme_path = os.path.join(item_path, "README.md")
            if not os.path.exists(readme_path) or force:
                success, msg = generate_readme(item_path, force)
                if success:
                    print(f"Generated README for {item}")
                    generated_count += 1
                else:
                    print(f"Failed to generate README for {item}: {msg}")
                    
    print(f"Completed readme generation. Created/updated {generated_count} files.")

if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    auto_generate_all(force_flag)
