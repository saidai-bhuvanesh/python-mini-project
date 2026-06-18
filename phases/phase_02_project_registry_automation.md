# Phase 2: Project Registry Automation

## Objective
Automatically detect and register projects into projects_registry.json.

## Deliverables
- Automatic registry generator script
- Project metadata extractor tool
- Project validation engine

## Problem Statement
Manually updating a central list of projects is prone to human error and easily goes out of sync. We need a script that scans the repository, validates each project's structure, extracts metadata, and updates a central registry dynamically.

## GitHub Issue Details
*   **Title**: Project Registry Automation - Phase 2
*   **Description**:
    ```markdown
    ### Phase 2: Project Registry Automation
    
    **Objective**: Automatically detect and register projects into projects_registry.json.
    
    **Deliverables**:
        - Automatic registry generator script
    - Project metadata extractor tool
    - Project validation engine
    
    **Problem Statement**:
    Manually updating a central list of projects is prone to human error and easily goes out of sync. We need a script that scans the repository, validates each project's structure, extracts metadata, and updates a central registry dynamically.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── scripts/
│   ├── register_projects.py
│   └── test_register_projects.py
├── projects_registry.json
└── standards/
    └── project_schema.json
```

### Files to Create
#### [NEW] [register_projects.py](file:///d:/mini/scripts/register_projects.py)
- **Description**: Python script to scan projects, validate metadata, and generate registry.
```python
import os
import json
# Automation registry generator logic goes here...
```



## Implementation Plan
1. Write a Python script `scripts/register_projects.py` that crawls `projects/`.
2. Implement a validator using `jsonschema` to validate each project's `metadata.json` against Phase 1's schema.
3. Compile all valid projects into a single `projects_registry.json` at the root.
4. Set up a CLI option to dry-run validation and fail with non-zero code on violation.

## Acceptance Criteria
- [ ] Registry generator scans all folders under `projects/`.
- [ ] Invalid projects are flagged and cause a non-zero exit code during CI dry-run.
- [ ] Valid projects are successfully outputted to `projects_registry.json` at the root.

## Unit Tests Verification
- Test metadata extraction for valid schema layouts.
- Test registry generator error raising on invalid JSON schema properties.
- Verify registry output updates existing list without deleting active valid projects.

## PR Specification
*   **PR Title**: `feat: Automate project detection and central registry generation`
*   **PR Description**:
    ```markdown
    Closes # 2
    
    Introduces `register_projects.py` which scans the repository, validates project schemas, and writes results to a master registry. This automated registry is critical for downstream dashboarding.
    ```
*   **Reviewer Update Comment**:
    > I have created the validation engine and generator. Please verify the registry layout in `projects_registry.json`.
