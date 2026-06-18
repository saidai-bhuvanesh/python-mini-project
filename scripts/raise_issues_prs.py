import os
import json
import sys
import urllib.request
import urllib.error

def make_github_request(url, data, token):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode("utf-8"))
            return None, err_data.get("message", e.reason)
        except Exception:
            return None, e.reason
    except Exception as e:
        return None, str(e)

def raise_all_issues_and_prs(repo, token):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roadmap_path = os.path.join(base_dir, "roadmap.json")
    
    if not os.path.exists(roadmap_path):
        print(f"[-] roadmap.json not found at {roadmap_path}")
        sys.exit(1)
        
    with open(roadmap_path, "r", encoding="utf-8") as f:
        phases = json.load(f)
        
    print(f"\n[*] Authenticating and preparing to raise 20 Issues and PRs for {repo}...")
    
    for p in phases:
        num = p["num"]
        title = p["title"]
        
        # 1. Create Issue
        issue_url = f"https://api.github.com/repos/{repo}/issues"
        issue_data = {
            "title": f"Phase {num}: {title}",
            "body": f"### Phase {num}: {title}\n\n**Objective**:\n{p['objective']}\n\n**Deliverables**:\n" + "\n".join([f"- {d}" for d in p["deliverables"]]) + f"\n\n**Problem Statement**:\n{p['problem_statement']}"
        }
        
        print(f"[*] Raising Issue #{num}: {title}...")
        issue_res, err = make_github_request(issue_url, issue_data, token)
        if err:
            print(f"[-] Failed to create Issue #{num}: {err}")
            continue
            
        issue_num = issue_res.get("number")
        print(f"[+] Created Issue #{issue_num} on GitHub!")
        
        # 2. Create PR
        pr_url = f"https://api.github.com/repos/{repo}/pulls"
        pr_data = {
            "title": p["pr_title"],
            "body": f"Closes #{issue_num}\n\n{p['pr_description']}",
            "head": f"feature/phase-{num:02d}",
            "base": "main"
        }
        
        print(f"[*] Creating PR for Phase #{num}...")
        pr_res, err = make_github_request(pr_url, pr_data, token)
        if err:
            print(f"[-] Failed to create PR for Phase #{num}: {err} (Note: you must push the 'feature/phase-{num:02d}' branch first!)")
        else:
            print(f"[+] Created Pull Request: {pr_res.get('html_url')}")
            
    print("\n[+] Finished raising GitHub Issues and Pull Requests!")

def init_git_branches():
    """
    Initializes a local git repo and creates the 20 branches containing the files.
    """
    import subprocess
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Git init
    subprocess.run(["git", "init"], cwd=base_dir)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=base_dir)
    subprocess.run(["git", "add", "."], cwd=base_dir)
    subprocess.run(["git", "commit", "-m", "chore: initial commit of standard templates and dashboard"], cwd=base_dir)
    
    # 2. Create branches
    # We will create local branches for each phase
    for num in range(1, 21):
        branch_name = f"feature/phase-{num:02d}"
        subprocess.run(["git", "branch", branch_name], cwd=base_dir)
        print(f"[+] Created local branch: {branch_name}")
        
    print("\n[+] Git initialized and 20 phase branches created locally.")
    print("[!] Push branches to GitHub using: 'git push origin --all' before running the PR creation script.")

if __name__ == "__main__":
    print("=" * 60)
    print(" GITHUB ISSUE & PR AUTOMATION TOOL ".center(60, "="))
    print("=" * 60)
    print("Options:")
    print("  1. Initialize local git repo and branches")
    print("  2. Raise Issues and PRs on remote GitHub repository")
    print("=" * 60)
    
    opt = input("Select option (1 or 2): ").strip()
    if opt == "1":
        init_git_branches()
    elif opt == "2":
        token = os.environ.get("GITHUB_TOKEN") or input("Enter your GitHub Personal Access Token (PAT): ").strip()
        repo = input("Enter GitHub repository (e.g. username/repo): ").strip()
        if not token or not repo:
            print("[-] Token and Repository are required.")
            sys.exit(1)
        raise_all_issues_and_prs(repo, token)
    else:
        print("[-] Invalid choice.")
