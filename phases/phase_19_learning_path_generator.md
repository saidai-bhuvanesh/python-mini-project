# Phase 19: Learning Path Generator

## Objective
Generate personalized learning journeys using repository projects.

## Deliverables
- Personalized learning roadmap builder
- Topic/skill progression analyzer
- Project sequencing graph

## Problem Statement
Users wanting to learn Python or web development have to choose projects blindly. We need a pathfinder tool to sequence projects logically (e.g., variables -> loops -> databases) so they form educational roadmaps.

## GitHub Issue Details
*   **Title**: Learning Path Generator - Phase 19
*   **Description**:
    ```markdown
    ### Phase 19: Learning Path Generator
    
    **Objective**: Generate personalized learning journeys using repository projects.
    
    **Deliverables**:
        - Personalized learning roadmap builder
    - Topic/skill progression analyzer
    - Project sequencing graph
    
    **Problem Statement**:
    Users wanting to learn Python or web development have to choose projects blindly. We need a pathfinder tool to sequence projects logically (e.g., variables -> loops -> databases) so they form educational roadmaps.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── learning_paths.py
```

### Files to Create
#### [NEW] [learning_paths.py](file:///d:/mini/scripts/learning_paths.py)
- **Description**: Generates education progressions and maps learning graphs.
```python
# Graph traversal and progression sequencing logic...
```



## Implementation Plan
1. Build `scripts/learning_paths.py`.
2. Model skill prerequisites and topic mappings for projects.
3. Create a Directed Acyclic Graph (DAG) of project progressions.
4. Generate customized learning pathways (e.g., 'Web Dev Track', 'Data Analyst Track').

## Acceptance Criteria
- [ ] Generates multi-step pathways mapped by skills.
- [ ] Inserts prerequisite projects before more advanced steps.
- [ ] Calculates total estimated learning times.

## Unit Tests Verification
- Verify DAG scheduler detects dependency loops correctly.
- Test pathgenerator prints correct paths based on selected categories.
- Verify behavior when requested topics contain zero registered projects.

## PR Specification
*   **PR Title**: `feat: Add learning path generator and sequencing graph`
*   **PR Description**:
    ```markdown
    Closes # 19
    
    Adds a learning path algorithm that organizes projects into educational sequences based on prerequisite skills and topics.
    ```
*   **Reviewer Update Comment**:
    > This generator uses a topological sort to make sure beginner projects come before intermediate ones. Take a look!
