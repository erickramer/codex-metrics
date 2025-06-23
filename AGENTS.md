# Coding Agent Guidelines

## Languages and Libraries
- Use **Python** for all implementations.
- Focus on the following libraries:
  - `streamlit` for building the dashboard UI.
  - `plotly` for visualizations.
- Keep dependencies minimal and documented.

## Style
- Code should be **concise** and primarily **functional**.
- Favor pure functions; minimize side effects.
- Include type hints and docstrings for all public functions.

## Testing
- Provide unit tests for any new code or behavior changes.
- Use `pytest` for running tests.
- Always run `pytest` from the repository root before committing.

## Commit Practices
- Keep commits focused on a single concern.
- Ensure the working tree is clean (`git status`) before ending tasks.
