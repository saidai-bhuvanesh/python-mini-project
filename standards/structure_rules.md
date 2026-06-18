# Repository Structure Rules

To keep the Python Mini Project Hub maintainable and automated, all projects added under `projects/` must adhere to these standard rules.

## Folder Layout Requirements
Every project must be a self-contained directory containing:
1.  **`metadata.json`**: Describes the project name, author, difficulty level, dependencies, and main entrypoint. Must match `standards/project_schema.json`.
2.  **`README.md`**: Project documentation based on the `standards/README_TEMPLATE.md`.
3.  **Entry Point**: A primary executable script (e.g. `main.py` or `cli.py`), matching the `"entry_point"` in `metadata.json`.
4.  **`tests/`**: A subdirectory containing unit tests (e.g. `test_main.py` or similar).

## Folder Naming Conventions
- Project directory names must be lowercase.
- Use snake_case or hyphen-separated names for directories (e.g., `calculator` or `weather-cli`).
- Avoid special characters, spaces, or numbers at the beginning of folder names.
