# Phase 9: Project Execution Sandbox

## Objective
Safely execute projects for validation and demonstrations.

## Deliverables
- Isolated sandbox execution environment
- Resource and security isolation controls
- Runtime monitoring and timeout manager

## Problem Statement
Running user-submitted Python projects locally poses security and stability risks, such as infinite loops, high CPU usage, or unauthorized filesystem access. We need a sandbox runner to execute projects safely.

## GitHub Issue Details
*   **Title**: Project Execution Sandbox - Phase 9
*   **Description**:
    ```markdown
    ### Phase 9: Project Execution Sandbox
    
    **Objective**: Safely execute projects for validation and demonstrations.
    
    **Deliverables**:
        - Isolated sandbox execution environment
    - Resource and security isolation controls
    - Runtime monitoring and timeout manager
    
    **Problem Statement**:
    Running user-submitted Python projects locally poses security and stability risks, such as infinite loops, high CPU usage, or unauthorized filesystem access. We need a sandbox runner to execute projects safely.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── sandbox_runner.py
```

### Files to Create
#### [NEW] [sandbox_runner.py](file:///d:/mini/scripts/sandbox_runner.py)
- **Description**: Safely manages subprocess executions with limits and environments.
```python
# Sandboxed execution engine with timeouts...
```



## Implementation Plan
1. Create a sandbox module `scripts/sandbox_runner.py`.
2. Use subprocesses with limited resource boundaries (timeout, memory, directory access).
3. Implement a virtual environment manager to automatically build isolated virtualenvs for execution.
4. Record standard output, error, exit codes, and runtime durations.

## Acceptance Criteria
- [ ] Execution is terminated if it exceeds a specified timeout (e.g. 5 seconds).
- [ ] Dependencies are isolated within their own virtual environments.
- [ ] Outputs (stdout, stderr, runtime) are captured in a structured format.

## Unit Tests Verification
- Test sandbox terminates infinite loops successfully.
- Test environment isolation by running script with custom dependencies.
- Verify stdout/stderr capture works correctly.

## PR Specification
*   **PR Title**: `feat: Create safe project execution sandbox`
*   **PR Description**:
    ```markdown
    Closes # 9
    
    Introduces a sandbox manager that sets limits on timeouts, environment isolation, and captures execution metrics safely.
    ```
*   **Reviewer Update Comment**:
    > This execution sandbox is key for project demos in the web interface. Review the sandbox constraints in `scripts/sandbox_runner.py`.
