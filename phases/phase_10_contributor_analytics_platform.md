# Phase 10: Contributor Analytics Platform

## Objective
Track contributor activity, commits, PRs, and project contributions.

## Deliverables
- Contributor leaderboard aggregator
- Git history analytics extractor
- Contribution activity report generator

## Problem Statement
Healthy open-source repositories require active communities. Currently, we lack an automated way to highlight contributor efforts, map git commits to specific projects, and reward active developers.

## GitHub Issue Details
*   **Title**: Contributor Analytics Platform - Phase 10
*   **Description**:
    ```markdown
    ### Phase 10: Contributor Analytics Platform
    
    **Objective**: Track contributor activity, commits, PRs, and project contributions.
    
    **Deliverables**:
        - Contributor leaderboard aggregator
    - Git history analytics extractor
    - Contribution activity report generator
    
    **Problem Statement**:
    Healthy open-source repositories require active communities. Currently, we lack an automated way to highlight contributor efforts, map git commits to specific projects, and reward active developers.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── analyze_contributors.py
```

### Files to Create
#### [NEW] [analyze_contributors.py](file:///d:/mini/scripts/analyze_contributors.py)
- **Description**: Queries git logs to calculate contributor stats per project.
```python
# Git log analysis script...
```



## Implementation Plan
1. Create `scripts/analyze_contributors.py`.
2. Use `GitPython` or shell out to `git log` to extract contributor data.
3. Associate commit directories with specific sub-projects to calculate project-level contributions.
4. Aggregate commits, lines added/removed, and active months, generating a scoreboard.

## Acceptance Criteria
- [ ] Correctly parses git history for authors and commit counts.
- [ ] Correctly attributes edits to specific project folders.
- [ ] Generates a contributors JSON report sorted by activity score.

## Unit Tests Verification
- Verify git log line parsing logic.
- Verify correct folder mapping for commit details.
- Test scoreboard sorting with mock data inputs.

## PR Specification
*   **PR Title**: `feat: Add git contributor analytics engine`
*   **PR Description**:
    ```markdown
    Closes # 10
    
    Establishes a contributor analytics utility that maps git commit records to project folders and counts contributions. This powers our community leaderboard.
    ```
*   **Reviewer Update Comment**:
    > I've added support for custom mailmaps to handle authors with multiple email addresses. Take a look!
