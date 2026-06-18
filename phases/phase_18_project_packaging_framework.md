# Phase 18: Project Packaging Framework

## Objective
Allow projects to be distributed as installable packages.

## Deliverables
- Project packaging setup templates
- Dynamic build scripts generator
- Distribution pipeline integration

## Problem Statement
Currently, projects are only runnable inside the source directory. To let users import these projects elsewhere as reusable libraries, we need a standard packaging pipeline to generate wheel/sdist packages.

## GitHub Issue Details
*   **Title**: Project Packaging Framework - Phase 18
*   **Description**:
    ```markdown
    ### Phase 18: Project Packaging Framework
    
    **Objective**: Allow projects to be distributed as installable packages.
    
    **Deliverables**:
        - Project packaging setup templates
    - Dynamic build scripts generator
    - Distribution pipeline integration
    
    **Problem Statement**:
    Currently, projects are only runnable inside the source directory. To let users import these projects elsewhere as reusable libraries, we need a standard packaging pipeline to generate wheel/sdist packages.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── standards/
│   └── pyproject_template.toml
└── scripts/
    └── build_package.py
```

### Files to Create
#### [NEW] [build_package.py](file:///d:/mini/scripts/build_package.py)
- **Description**: Script to compile sub-projects into standard Python wheel packages.
```python
# Python packaging and distribution builder...
```



## Implementation Plan
1. Establish packaging blueprints using `pyproject.toml` templates.
2. Develop a script `scripts/build_package.py` to auto-populate metadata and configuration settings.
3. Use `build` and `setuptools` to package individual directories dynamically.
4. Support generating wheels locally under `dist/`.

## Acceptance Criteria
- [ ] Successful creation of `.whl` and `.tar.gz` packages.
- [ ] Packages correctly declare name, version, and dependencies.
- [ ] Packaged projects can be imported standardly via `pip install`.

## Unit Tests Verification
- Test build scripts compile standard package outputs without failing.
- Verify dependencies are correctly populated inside PKG-INFO metadata files.
- Verify packaging setup rejects invalid directory schemas.

## PR Specification
*   **PR Title**: `feat: Build distribution and packaging framework`
*   **PR Description**:
    ```markdown
    Closes # 18
    
    Establishes python-packaging configurations, allowing sub-projects to build wheel formats using template-driven setuptools workflows.
    ```
*   **Reviewer Update Comment**:
    > Check the wheels created in the `dist/` directory. They are fully importable!
