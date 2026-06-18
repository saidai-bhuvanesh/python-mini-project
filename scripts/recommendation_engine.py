import os
import json
import sys

class RecommendationEngine:
    def __init__(self, registry_path, health_report_path=None):
        self.projects = []
        self.health = {}
        
        if os.path.exists(registry_path):
            try:
                with open(registry_path, "r", encoding="utf-8") as f:
                    self.projects = json.load(f)
            except Exception:
                pass
                
        if health_report_path and os.path.exists(health_report_path):
            try:
                with open(health_report_path, "r", encoding="utf-8") as f:
                    self.health = json.load(f)
            except Exception:
                pass

    def get_recommendations(self, user_profile):
        """
        user_profile: {
            "interests": ["math", "cli"],
            "skill_level": "Beginner"
        }
        """
        user_interests = [i.lower() for i in user_profile.get("interests", [])]
        user_level = user_profile.get("skill_level", "Beginner")
        
        level_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
        user_level_val = level_map.get(user_level, 1)
        
        scored = []
        for p in self.projects:
            score = 0
            p_name = p.get("name", "")
            
            # 1. Skill Level Matching
            p_level = p.get("difficulty", "Beginner")
            p_level_val = level_map.get(p_level, 1)
            
            diff = abs(user_level_val - p_level_val)
            if diff == 0:
                score += 100 # Exact match
            elif diff == 1:
                score += 50  # Next level up/down
            else:
                score += 10  # Far match
                
            # 2. Tag Interest Matching
            p_tags = [t.lower() for t in p.get("tags", [])]
            common_tags = set(user_interests).intersection(p_tags)
            score += len(common_tags) * 30
            
            # 3. Project Health Weight
            p_health = self.health.get(p_name, {}).get("health_score", 100)
            score += p_health * 0.2
            
            scored.append({
                "project": p,
                "score": round(score, 1),
                "reasons": [
                    f"Matches your skill level ({p_level})" if diff == 0 else f"Progressive skill step ({p_level})",
                    f"Matches interests: {', '.join(common_tags)}" if common_tags else None
                ]
            })
            
        # Filter reasons and sort
        for item in scored:
            item["reasons"] = [r for r in item["reasons"] if r]
            
        return sorted(scored, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reg = os.path.join(base_dir, "projects_registry.json")
    health = os.path.join(base_dir, "reports", "broken_projects_report.json")
    
    engine = RecommendationEngine(reg, health)
    profile = {
        "interests": ["math", "cli"],
        "skill_level": "Beginner"
    }
    
    recs = engine.get_recommendations(profile)
    print("Recommendations:")
    for r in recs[:5]:
        print(f" - {r['project']['name']} (Score: {r['score']})")
        for reason in r['reasons']:
            print(f"   * {reason}")
