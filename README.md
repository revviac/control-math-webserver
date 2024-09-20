# python-template
A template for a python project with poetry dependency management and pytest tests.

# Initializing the environment
## Initializing the virtual environment
1. Install dependencies:
    - With poetry: `poetry install --with=dev --with=test` (will create a .venv directory in the root project directory)
    - With pip: `pip install -r requirements.txt`
2. Initialize the virtual environment:
    - With poetry: `poetry shell`
    - Without poetry: source `{PATH_TO_VENV}/Scripts/{ACTIVATE_SCRIPT}` (e.g. powershell: `.venv/Scripts/activate.ps1`, shell: `source .venv/Scripts/activate`)
3. Update requirements:
    - If updating through poetry, run `./scripts/export-poetry.[...]` (depending on your shell)

## Installing pre-commit hooks
Use `pre-commit install` after activating the environment. See pre-commit hooks in `.pre-commit-config.yaml` file.
