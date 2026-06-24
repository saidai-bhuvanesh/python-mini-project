import os
import json
import sys

class LearningPathGenerator:
    def __init__(self, registry_path):
        self.projects = []
        if os.path.exists(registry_path):
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    self.projects = json.load(f)
            except Exception:
                pass

    def build_dependency_graph(self):
        """
        Builds graph nodes. Dependencies are based on difficulty:
        Beginner -> Intermediate -> Advanced.
        Projects with overlapping tags under lower difficulty act as prerequisites.
        """
        adj = {p["name"]: [] for p in self.projects}
        in_degree = {p["name"]: 0 for p in self.projects}
        
        # Difficulty weights for comparison
        diff_weights = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
        
        for p1 in self.projects:
            name1 = p1["name"]
            w1 = diff_weights.get(p1["difficulty"], 1)
            t1 = set(p1["tags"])
            
            for p2 in self.projects:
                name2 = p2["name"]
                if name1 == name2:
                    continue
                w2 = diff_weights.get(p2["difficulty"], 1)
                t2 = set(p2["tags"])
                
                # If p1 is simpler than p2, and they share at least one tag
                # Make p1 a prerequisite for p2
                if w1 < w2 and t1.intersection(t2):
                    adj[name1].append(name2)
                    in_degree[name2] += 1
                    
        return adj, in_degree

    def generate_paths(self):
        adj, in_degree = self.build_dependency_graph()
        
        # Topological Sort
        queue = [name for name, deg in in_degree.items() if deg == 0]
        sorted_projects = []
        
        while queue:
            # Sort queue to ensure stable/alphabetical ordering for same degree
            queue.sort()
            curr = queue.pop(0)
            sorted_projects.append(curr)
            
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # Group by track / tags
        tracks = {
            "Core Python Mastery": sorted_projects,
            "CLI & Scripting": [p["name"] for p in self.projects if "cli" in p.get("tags", []) or "utility" in p.get("tags", [])]
        }
        
        # Resolve track order based on master sorted order
        for track_name in tracks:
            tracks[track_name] = [name for name in sorted_projects if name in tracks[track_name]]
            
        return {
            "master_sequence": sorted_projects,
            "tracks": tracks
        }

def compile_paths():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reg = os.path.join(base_dir, "projects_registry.json")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    gen = LearningPathGenerator(reg)
    paths = gen.generate_paths()
    
    report_path = os.path.join(reports_dir, "learning_paths.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(paths, f, indent=2)
        
    print(f"Learning paths compiled. Report saved to {report_path}")
    return paths

if __name__ == "__main__":
    compile_paths()
