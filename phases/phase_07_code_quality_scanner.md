# Phase 7: Code Quality Scanner

## Objective
Perform repository-wide PEP8, linting, and style validation.

## Deliverables
- Flake8 and Black integration configurations
- Code quality report generator
- Linter scoring metrics dashboard

## Problem Statement
Code style consistency is critical for maintaining codebases. Without automated formatting checks, code quality deteriorates. We need a quality scanner that runs code formatters/linters, scores file qualities, and formats reports.

## GitHub Issue Details
*   **Title**: Code Quality Scanner - Phase 7
*   **Description**:
    ```markdown
    ### Phase 7: Code Quality Scanner
    
    **Objective**: Perform repository-wide PEP8, linting, and style validation.
    
    **Deliverables**:
        - Flake8 and Black integration configurations
    - Code quality report generator
    - Linter scoring metrics dashboard
    
    **Problem Statement**:
    Code style consistency is critical for maintaining codebases. Without automated formatting checks, code quality deteriorates. We need a quality scanner that runs code formatters/linters, scores file qualities, and formats reports.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── .flake8
├── pyproject.toml
└── scripts/
    └── lint_scanner.py
```

### Files to Create
#### [NEW] [lint_scanner.py](file:///d:/mini/scripts/lint_scanner.py)
- **Description**: Linter runner and quality score calculation wrapper.
```python
# Quality scanner orchestration script...
```



## Implementation Plan
1. Configure Flake8, Black, and Ruff configurations in the repo root.
2. Develop a wrapper script `scripts/lint_scanner.py` that executes these linters.
3. Parse output logs to score each project based on quality guidelines.
4. Integrate the results into the repository health dashboard.

## Acceptance Criteria
- [ ] All projects are scanned for linting errors.
- [ ] Outputs unified code quality rating (e.g., A/B/C/D) per project.
- [ ] Build fails if formatting violates Black style rules.

## Unit Tests Verification
- Verify ruff/flake8 logs are parsed correctly.
- Verify that score calculations weight errors correctly.
- Ensure linter ignores virtual environments or standard libraries.

## PR Specification
*   **PR Title**: `feat: Standardize code quality checking and lint scoring`
*   **PR Description**:
    ```markdown
    Closes # 7
    
    Establishes linter configurations, implements formatting verification, and introduces a script to generate quality health reports for each sub-project.
    ```
*   **Reviewer Update Comment**:
    > The ruff / flake8 rules are configured in `.flake8` and `pyproject.toml`. Please make sure your IDE auto-formats on save.
