# Phase 15: Project Preview System

## Objective
Provide screenshots, demos, and previews for projects.

## Deliverables
- Interactive preview cards layout
- Project demo integration templates
- Media asset uploading and indexing support

## Problem Statement
Users cannot see what a project does or looks like without running it locally. We need a system to showcase screenshots, diagrams, and terminal recorded terminal sessions (e.g. asciinema) in the project cards.

## GitHub Issue Details
*   **Title**: Project Preview System - Phase 15
*   **Description**:
    ```markdown
    ### Phase 15: Project Preview System
    
    **Objective**: Provide screenshots, demos, and previews for projects.
    
    **Deliverables**:
        - Interactive preview cards layout
    - Project demo integration templates
    - Media asset uploading and indexing support
    
    **Problem Statement**:
    Users cannot see what a project does or looks like without running it locally. We need a system to showcase screenshots, diagrams, and terminal recorded terminal sessions (e.g. asciinema) in the project cards.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── standards/
    └── preview_assets_schema.md
```

### Files to Create
#### [NEW] [preview_assets_schema.md](file:///d:/mini/standards/preview_assets_schema.md)
- **Description**: Standard rules specifying screenshot sizes, image ratios, and formats.
```python
# Preview Assets Standards
All images should be inside the project's assets/ directory...
```



## Implementation Plan
1. Define standards for project asset storage (e.g., `projects/<name>/assets/`).
2. Update registry to catalogue previews and paths.
3. Build UI media players/carousels to display images, GIFs, or terminal recordings.
4. Integrate terminal recording files into the visual deck.

## Acceptance Criteria
- [ ] Registry indexes screenshot paths automatically.
- [ ] Dashboard renders image galleries if screenshots exist.
- [ ] Terminal recordings display correctly in sandboxed terminals.

## Unit Tests Verification
- Verify asset crawling registers files of correct extensions.
- Verify empty folder handling when searching screenshots.
- Verify asset path translations for web hosting paths.

## PR Specification
*   **PR Title**: `feat: Add media preview system and gallery cards`
*   **PR Description**:
    ```markdown
    Closes # 15
    
    Enables asset indexing for screenshots and terminal recordings. Updates project cards on the dashboard to render carousel visual displays.
    ```
*   **Reviewer Update Comment**:
    > Verify that your project assets folder contains images scaled to standard aspect ratios (16:9).
