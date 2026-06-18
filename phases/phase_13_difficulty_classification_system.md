# Phase 13: Difficulty Classification System

## Objective
Automatically classify projects as Beginner, Intermediate, or Advanced.

## Deliverables
- Code complexity assessment model
- Automatic difficulty scoring engine
- Learning progression sequencer

## Problem Statement
Manually classifying project difficulty is subjective and inconsistent across contributors. We need a system that calculates difficulty scores based on code features (LOC, Cyclomatic Complexity, dependency count, library usage).

## GitHub Issue Details
*   **Title**: Difficulty Classification System - Phase 13
*   **Description**:
    ```markdown
    ### Phase 13: Difficulty Classification System
    
    **Objective**: Automatically classify projects as Beginner, Intermediate, or Advanced.
    
    **Deliverables**:
        - Code complexity assessment model
    - Automatic difficulty scoring engine
    - Learning progression sequencer
    
    **Problem Statement**:
    Manually classifying project difficulty is subjective and inconsistent across contributors. We need a system that calculates difficulty scores based on code features (LOC, Cyclomatic Complexity, dependency count, library usage).
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── classify_difficulty.py
```

### Files to Create
#### [NEW] [classify_difficulty.py](file:///d:/mini/scripts/classify_difficulty.py)
- **Description**: Calculates complexity metrics and assigns difficulty classifications.
```python
# Code complexity analysis and grading...
```



## Implementation Plan
1. Develop `scripts/classify_difficulty.py`.
2. Integrate `radon` or `mccabe` to compute cyclomatic complexity.
3. Calculate features: lines of code, nesting depth, number of functions/classes, imports.
4. Write classifier thresholds to bin projects into Beginner, Intermediate, and Advanced categories.

## Acceptance Criteria
- [ ] Classifies difficulty without manual input.
- [ ] Accounts for code complexity, nesting, and library imports.
- [ ] Saves calculated difficulties directly into project registries.

## Unit Tests Verification
- Test simple code scripts classify as Beginner.
- Test scripts with high nesting/recursion levels get tagged Intermediate/Advanced.
- Verify threshold logic is stable across minor code format changes.

## PR Specification
*   **PR Title**: `feat: Add automatic project difficulty classifier`
*   **PR Description**:
    ```markdown
    Closes # 13
    
    Introduces code complexity analysis using cyclomatic complexity and code length metrics to automatically assign difficulty classifications to projects.
    ```
*   **Reviewer Update Comment**:
    > We use radon metrics for classifying. If a project uses complex libraries like socket or asyncio, it defaults to Intermediate/Advanced.
