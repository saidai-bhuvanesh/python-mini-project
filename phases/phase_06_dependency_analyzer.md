# Phase 6: Dependency Analyzer

## Objective
Analyze dependencies across all projects and detect unused packages.

## Deliverables
- Dependency graph generator
- Unused dependency reporting tools
- Version audit engine

## Problem Statement
Over time, projects accumulate unused packages in `requirements.txt` or use conflicting versions of common dependencies. We need a dependency analyzer to map package references, flag unused imports, and audit outdated/vulnerable libraries.

## GitHub Issue Details
*   **Title**: Dependency Analyzer - Phase 6
*   **Description**:
    ```markdown
    ### Phase 6: Dependency Analyzer
    
    **Objective**: Analyze dependencies across all projects and detect unused packages.
    
    **Deliverables**:
        - Dependency graph generator
    - Unused dependency reporting tools
    - Version audit engine
    
    **Problem Statement**:
    Over time, projects accumulate unused packages in `requirements.txt` or use conflicting versions of common dependencies. We need a dependency analyzer to map package references, flag unused imports, and audit outdated/vulnerable libraries.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── analyze_dependencies.py
```

### Files to Create
#### [NEW] [analyze_dependencies.py](file:///d:/mini/scripts/analyze_dependencies.py)
- **Description**: Dependency audit and graph creation tool.
```python
# Python script to audit dependencies...
```



## Implementation Plan
1. Write `scripts/analyze_dependencies.py`.
2. Parse `requirements.txt` or `pyproject.toml` and search python files for corresponding `import` statements.
3. Generate a dependency graph showing inter-project dependency patterns.
4. Report unused dependencies and identify version mismatches.

## Acceptance Criteria
- [ ] Finds imported modules that are not listed in requirements.
- [ ] Flags libraries in requirements that are never imported.
- [ ] Saves a version audit report showing version conflicts.

## Unit Tests Verification
- Test import matching engine with complex multi-level imports.
- Verify unused warnings trigger correctly for unimported libraries.
- Verify correct matching of packaging aliases (e.g. `pyyaml` vs `import yaml`).

## PR Specification
*   **PR Title**: `feat: Add dependency analyzer and version audit tools`
*   **PR Description**:
    ```markdown
    Closes # 6
    
    Adds a tool to audit repository dependencies, mapping imported python modules back to requirements lists, checking for unused requirements, and flagging version mismatches.
    ```
*   **Reviewer Update Comment**:
    > I've handled import alias mappings for popular packages. Let me know if you encounter any edge cases with complex imports.
