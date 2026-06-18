# Phase 5: Automated README Generator

## Objective
Generate README files for projects missing documentation.

## Deliverables
- Documentation automation script
- README templates based on project type
- Metadata-to-documentation extractor

## Problem Statement
Writing standard README files can be tedious for developers, leading to empty or sparse project descriptions. We need an automated script to parse `metadata.json`, source files, and tests to generate a professional, standardized `README.md` automatically.

## GitHub Issue Details
*   **Title**: Automated README Generator - Phase 5
*   **Description**:
    ```markdown
    ### Phase 5: Automated README Generator
    
    **Objective**: Generate README files for projects missing documentation.
    
    **Deliverables**:
        - Documentation automation script
    - README templates based on project type
    - Metadata-to-documentation extractor
    
    **Problem Statement**:
    Writing standard README files can be tedious for developers, leading to empty or sparse project descriptions. We need an automated script to parse `metadata.json`, source files, and tests to generate a professional, standardized `README.md` automatically.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── generate_readme.py
```

### Files to Create
#### [NEW] [generate_readme.py](file:///d:/mini/scripts/generate_readme.py)
- **Description**: Automatically generates README.md based on project details.
```python
# Script to generate documentation...
```



## Implementation Plan
1. Create `scripts/generate_readme.py`.
2. Extract features, entry points, and tests details from the project codebase.
3. Fill template placeholders based on project categories (CLI, Web, Utility).
4. Add safety check to prevent overwriting custom documentation unless `--force` is supplied.

## Acceptance Criteria
- [ ] Script generates a detailed README.md matching requirements.
- [ ] Existing customized READMEs are not overwritten by default.
- [ ] Successfully extracts installation details from `requirements.txt` if present.

## Unit Tests Verification
- Verify template variables are replaced correctly.
- Verify CLI parameters (like `--force`) actuate correctly.
- Test behavior when `requirements.txt` is missing.

## PR Specification
*   **PR Title**: `feat: Add automated README generator`
*   **PR Description**:
    ```markdown
    Closes # 5
    
    Introduces a utility to generate project READMEs from code metadata. Saves developer time and maintains repository documentation consistency.
    ```
*   **Reviewer Update Comment**:
    > Let's review the templates used for the README generator. We can expand this with AI integration in the future.
