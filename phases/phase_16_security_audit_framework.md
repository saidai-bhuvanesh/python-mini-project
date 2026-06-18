# Phase 16: Security Audit Framework

## Objective
Detect unsafe code patterns and vulnerabilities.

## Deliverables
- Bandit tool configuration and wrapper script
- Repository vulnerability reports
- Unsafe import scanner rules

## Problem Statement
Python mini-projects may unintentionally include insecure code practices (such as `eval()`, hardcoded secrets, or insecure random modules). We need a security checker that audits the code prior to registering or executing.

## GitHub Issue Details
*   **Title**: Security Audit Framework - Phase 16
*   **Description**:
    ```markdown
    ### Phase 16: Security Audit Framework
    
    **Objective**: Detect unsafe code patterns and vulnerabilities.
    
    **Deliverables**:
        - Bandit tool configuration and wrapper script
    - Repository vulnerability reports
    - Unsafe import scanner rules
    
    **Problem Statement**:
    Python mini-projects may unintentionally include insecure code practices (such as `eval()`, hardcoded secrets, or insecure random modules). We need a security checker that audits the code prior to registering or executing.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── .bandit
└── scripts/
    └── security_audit.py
```

### Files to Create
#### [NEW] [security_audit.py](file:///d:/mini/scripts/security_audit.py)
- **Description**: Runs security sweeps, audits codebases, and writes vuln warnings.
```python
# Python script wrapping bandit and custom checks...
```



## Implementation Plan
1. Integrate `bandit` as a security code audit engine.
2. Write `scripts/security_audit.py` to run audits per project.
3. Build custom ast checkers to intercept calls to unsafe functions (e.g. `subprocess.shell=True`).
4. Generate structured JSON safety reports.

## Acceptance Criteria
- [ ] Audits code for common vulnerabilities (eval, exec, hardcoded credentials).
- [ ] Flags insecure dependencies or library version vulnerabilities.
- [ ] Outputs severity flags (low, medium, high) and aborts execution on high vulnerabilities.

## Unit Tests Verification
- Test that files containing `eval()` trigger high severity flags.
- Test that files with hardcoded API keys trigger warnings.
- Verify clean files receive a secure rating.

## PR Specification
*   **PR Title**: `feat: Integrate security audit and vulnerability framework`
*   **PR Description**:
    ```markdown
    Closes # 16
    
    Adds Bandit configurations and custom AST scanners to check projects for insecure code patterns like eval or shell injection vectors before inclusion.
    ```
*   **Reviewer Update Comment**:
    > This scanning framework runs during the project registry generation. Any project with High-level security bugs will be blocked.
