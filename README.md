# Codex Metrics Dashboard

This project provides a Streamlit dashboard for visualizing code metrics.

## Virtual Environment Setup

1. Ensure Python 3.9 or newer is installed.
2. Install [`uv`](https://github.com/astral-sh/uv) if not already available:

   ```bash
   pip install uv
   ```

3. Create and activate a virtual environment:

   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies with `uv pip`:

   ```bash
   uv pip install -r requirements.txt
   ```

## Type Checking

Install `mypy` for static analysis and run it from the project root. If any
stub packages are missing, install them (e.g. `types-requests`).

```bash
uv pip install mypy
mypy app
```

## Development Workflow

Always run the unit tests and type checks before committing code:

```bash
pytest -q
mypy app
```


## Running the Dashboard Locally

After installing dependencies, start the Streamlit server with:

```bash
streamlit run app/main.py
```

Then open <http://localhost:8501> in your browser to view the dashboard.

