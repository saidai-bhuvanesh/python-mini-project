# Phase 1: Repository Structure Standardization

## Objective
Standardize folder naming, project layout, README format, and contribution structure across the repository.

## Deliverables
- Folder structure validation rules
- Naming convention guidelines for projects
- Standardized README template
- Project metadata json schema specification

## Problem Statement
As the repository grows, contributors add projects with inconsistent directories, missing documentation, and custom layouts. This makes automatic scanning, testing, and discovery difficult. We need a strict standard for project layouts and naming.

## GitHub Issue Details
*   **Title**: Repository Structure Standardization - Phase 1
*   **Description**:
    ```markdown
    ### Phase 1: Repository Structure Standardization
    
    **Objective**: Standardize folder naming, project layout, README format, and contribution structure across the repository.
    
    **Deliverables**:
        - Folder structure validation rules
    - Naming convention guidelines for projects
    - Standardized README template
    - Project metadata json schema specification
    
    **Problem Statement**:
    As the repository grows, contributors add projects with inconsistent directories, missing documentation, and custom layouts. This makes automatic scanning, testing, and discovery difficult. We need a strict standard for project layouts and naming.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── .github/
│   └── workflows/
│       └── structure_linter.yml
├── standards/
│   ├── project_schema.json
│   ├── README_TEMPLATE.md
│   └── structure_rules.md
└── projects/
    └── example_project/
        ├── metadata.json
        ├── README.md
        ├── main.py
        └── tests/
            └── test_main.py
```

### Files to Create
#### [NEW] [project_schema.json](file:///d:/mini/standards/project_schema.json)
- **Description**: JSON Schema definition for project metadata (metadata.json).
```python
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProjectMetadata",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "description": { "type": "string" },
    "author": { "type": "string" },
    "difficulty": { "type": "string", "enum": ["Beginner", "Intermediate", "Advanced"] },
    "tags": { "type": "array", "items": { "type": "string" } },
    "dependencies": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["name", "description", "difficulty", "tags"]
}
```

#### [NEW] [README_TEMPLATE.md](file:///d:/mini/standards/README_TEMPLATE.md)
- **Description**: Standard README template to be used by all sub-projects.
```python
# Project Name

Brief description of the project.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the project: `python main.py`

## Running Tests
Run tests using `pytest`
```



## Implementation Plan
1. Define the standardized folder layout (e.g., standard folders for source, tests, assets).
2. Create a schema for `metadata.json` that every project must include.
3. Write a lint-like validation configuration to enforce these rules.
4. Draft a README template with required sections (Introduction, Installation, Usage, Tests).

## Acceptance Criteria
- [ ] All new projects must match the standards folder layout.
- [ ] Projects must contain a valid `metadata.json` matching the standard JSON Schema.
- [ ] Projects must contain a `README.md` based on the standard template.

## Unit Tests Verification
- Verify that a project with a valid structure and metadata passes validation.
- Verify that a project with a missing `metadata.json` or invalid fields fails validation.
- Verify that folders with non-standard names are flagged.

## PR Specification
*   **PR Title**: `feat: Establish repository standards and templates`
*   **PR Description**:
    ```markdown
    Closes # 1
    
    This PR introduces standardized repository rules, a schema for project metadata, a standardized README template, and a workflow specification to validate them. This acts as the baseline for Phase 2 automation.
    ```
*   **Reviewer Update Comment**:
    > Hi team, the repository structures and standards have been established. Please review the schema in `standards/project_schema.json` and the folder structures.
