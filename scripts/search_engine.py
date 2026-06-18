import os
import json
import re
import sys

class SearchEngine:
    def __init__(self, registry_path):
        self.projects = []
        if os.path.exists(registry_path):
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    self.projects = json.load(f)
            except Exception:
                pass

    def search(self, query, tags=None, difficulty=None):
        if not query and not tags and not difficulty:
            return self.projects
            
        results = []
        query_words = re.findall(r"\w+", query.lower()) if query else []
        
        for p in self.projects:
            score = 0
            
            # Text relevance scoring
            name = p.get("name", "").lower()
            desc = p.get("description", "").lower()
            p_tags = [t.lower() for t in p.get("tags", [])]
            
            # Exact title matches have highest weight
            for word in query_words:
                if word in name:
                    score += 10
                if word in desc:
                    score += 3
                for tag in p_tags:
                    if word in tag:
                        score += 5
                        
            # Filter by tags (AND logic)
            if tags:
                # tags can be a list of strings
                if not all(t.lower() in p_tags for t in tags):
                    continue
                    
            # Filter by difficulty
            if difficulty:
                if p.get("difficulty", "").lower() != difficulty.lower():
                    continue
                    
            if (query and score > 0) or (not query and (tags or difficulty)):
                results.append((score, p))
                
        # Sort by relevance score desc, then name asc
        sorted_results = sorted(results, key=lambda x: (-x[0], x[1].get("name", "")))
        return [item[1] for item in sorted_results]

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    registry = os.path.join(base_dir, "projects_registry.json")
    
    engine = SearchEngine(registry)
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    print(f"Searching for: '{query}'")
    matches = engine.search(query)
    for m in matches:
        print(f" - [{m['difficulty']}] {m['name']}: {m['description']}")
