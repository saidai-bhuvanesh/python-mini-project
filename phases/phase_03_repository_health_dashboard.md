# Phase 3: Repository Health Dashboard

## Objective
Create dashboard showing project count, test status, contributors, and coverage.

## Deliverables
- Dashboard frontend/UI design
- Health analytics and aggregator engine
- Repository insights and trends collector

## Problem Statement
Stakeholders and maintainers have no quick visual way to assess the health of the repository, including project counts, test pass rates, coverage metrics, and contributor distributions. A central health dashboard is required.

## GitHub Issue Details
*   **Title**: Repository Health Dashboard - Phase 3
*   **Description**:
    ```markdown
    ### Phase 3: Repository Health Dashboard
    
    **Objective**: Create dashboard showing project count, test status, contributors, and coverage.
    
    **Deliverables**:
        - Dashboard frontend/UI design
    - Health analytics and aggregator engine
    - Repository insights and trends collector
    
    **Problem Statement**:
    Stakeholders and maintainers have no quick visual way to assess the health of the repository, including project counts, test pass rates, coverage metrics, and contributor distributions. A central health dashboard is required.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
├── scripts/
│   └── generate_dashboard.py
├── dashboard/
│   ├── template.html
│   └── assets/
│       ├── dashboard.css
│       └── app.js
└── index.html (generated dashboard)
```

### Files to Create
#### [NEW] [generate_dashboard.py](file:///d:/mini/scripts/generate_dashboard.py)
- **Description**: Generates static HTML dashboard based on repository analytics.
```python
# Python code to aggregate stats and write HTML dashboard...
```



## Implementation Plan
1. Create a dashboard generator script `scripts/generate_dashboard.py`.
2. Read data from `projects_registry.json` and gather test execution results.
3. Build an HTML report generator that generates a modern, static dashboard with graphs.
4. Integrate summary cards showing total projects, overall test success rate, total lines of code, and contributor counts.

## Acceptance Criteria
- [ ] Generates a modern static dashboard `index.html`.
- [ ] Shows key metrics: project counts, passing tests percentage, total contributors.
- [ ] Responsive layout matching dark mode specifications.

## Unit Tests Verification
- Test statistics aggregator produces correct math calculations.
- Verify HTML generation doesn't crash on empty registry.
- Verify CSS/JS files copy correctly to target output directories.

## PR Specification
*   **PR Title**: `feat: Build static repository health dashboard generator`
*   **PR Description**:
    ```markdown
    Closes # 3
    
    Adds a tool to generate a visual repository dashboard detailing overall health metrics, test statuses, and contributor insights. Outputs to index.html.
    ```
*   **Reviewer Update Comment**:
    > The health dashboard generator is ready. We now have an aggregated view of the repository health. Let's discuss hosting it via GitHub Pages.
