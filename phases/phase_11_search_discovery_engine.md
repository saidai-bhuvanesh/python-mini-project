# Phase 11: Search & Discovery Engine

## Objective
Enable users to search projects using tags, categories, and keywords.

## Deliverables
- Unified Search API and class
- Tag indexing engine
- Filtering and sorting middleware

## Problem Statement
As the project registry grows to dozens or hundreds of projects, finding specific types of projects (e.g. 'game', 'data science') becomes difficult. We need a search and discovery engine for fast lookups.

## GitHub Issue Details
*   **Title**: Search & Discovery Engine - Phase 11
*   **Description**:
    ```markdown
    ### Phase 11: Search & Discovery Engine
    
    **Objective**: Enable users to search projects using tags, categories, and keywords.
    
    **Deliverables**:
        - Unified Search API and class
    - Tag indexing engine
    - Filtering and sorting middleware
    
    **Problem Statement**:
    As the project registry grows to dozens or hundreds of projects, finding specific types of projects (e.g. 'game', 'data science') becomes difficult. We need a search and discovery engine for fast lookups.
    ```

## Proposed Changes
### Folder Structure
```text
python-mini-project/
└── scripts/
    └── search_engine.py
```

### Files to Create
#### [NEW] [search_engine.py](file:///d:/mini/scripts/search_engine.py)
- **Description**: Fuzzy keyword indexing and tag filtering search engine.
```python
# Fuzzy search index matching logic...
```



## Implementation Plan
1. Write `scripts/search_engine.py` with indexing capabilities.
2. Parse `projects_registry.json` and build an inverted index of keywords, tags, and titles.
3. Implement scoring (e.g. BM25 or basic term frequency matching) for fuzzy text search.
4. Support advanced filters (difficulty level, tags, dependency count).

## Acceptance Criteria
- [ ] Fast keyword matching over titles, description, and tags.
- [ ] Support filtering by multiple tags (AND/OR logic).
- [ ] Sorting results by project name, difficulty, or health rating.

## Unit Tests Verification
- Verify search returns relevant matches for partial queries.
- Test filters with combinations of tags and difficulty levels.
- Verify index updates correctly when projects are modified.

## PR Specification
*   **PR Title**: `feat: Build search and discovery engine`
*   **PR Description**:
    ```markdown
    Closes # 11
    
    Implements a backend indexing and search engine that supports fuzzy text queries and metadata filters over all registered projects.
    ```
*   **Reviewer Update Comment**:
    > This indexer will run at build-time to keep search fast. Let me know if you think we should support regex searches.
