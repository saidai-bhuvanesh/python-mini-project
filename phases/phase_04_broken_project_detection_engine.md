# Phase 4: Broken Project Detection Engine

## Objective
Automatically identify projects with missing files, import errors, or execution failures.

## Deliverables
- Broken project validation scanner
- Automated broken project reports generator
- Health scoring algorithms

## Problem Statement
Projects in the repository can break silently due to python updates, missing dependencies, or refactoring in standard libraries. We need a diagnostic tool to run check executions and detect imports, syntax errors, and missing files.

## GitHub Issue Details
*   **Title**: Broken Project Detection Engine - Phase 4
*   **Description**:
    ```markdown
    ### Phase 4: Broken Project Detection Engine
    
    **Objective**: Automatically identify projects with missing files, import errors, or execution failures.
    
    **Deliverables**:
        - Broken project validation scanner
    - Automated broken project reports generator
    - Health scoring algorithms
    
    **Problem Statement**:
    Projects in the repository can break silently due to python updates, missing dependencies, or refactoring in standard libraries. We need a diagnostic tool to run check executions and detect imports, syntax errors, and missing files.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── scripts/
│   └── detect_broken_projects.py
└── reports/
    └── broken_projects_report.json
```

### Files to Create
#### [NEW] [detect_broken_projects.py](file:///d:/mini/scripts/detect_broken_projects.py)
- **Description**: Scanner checking for syntax, imports, and execution failures.
```python
# Python script using AST to inspect project imports...
```



## Implementation Plan
1. Build a diagnostic tool `scripts/detect_broken_projects.py`.
2. Simulate file structure verification and dry-run execution checks (e.g. AST analysis for import safety).
3. Generate detailed report of broken projects and assign a health score (0-100) to each project.
4. Incorporate scanner into CI workflow to prevent merging broken projects.

## Acceptance Criteria
- [ ] Scanner must detect missing entrypoints or config files.
- [ ] Scanner must identify syntax errors and import errors using AST parsing without full unsafe execution.
- [ ] Reports are saved to `reports/broken_projects_report.json`.

## Unit Tests Verification
- Verify AST inspector catches invalid module imports.
- Verify scanner scores a perfect project as 100 health.
- Verify projects with critical issues are scored below 50 and flag failures.

## PR Specification
*   **PR Title**: `feat: Implement broken project detection engine`
*   **PR Description**:
    ```markdown
    Closes # 4
    
    Adds static verification and dry-run execution scanning for projects to check for import errors, syntax issues, and missing files. Generates JSON reports and assigns health scores.
    ```
*   **Reviewer Update Comment**:
    > This scanning engine checks imports and syntax statically using AST. This ensures safety as we don't execute arbitrary scripts yet.
