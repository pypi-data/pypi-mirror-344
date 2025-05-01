# Contributing to SHLLM

## Setting up Git hooks

This repository uses Git hooks to ensure code quality and consistent versioning.

To set up the hooks, run the following command after cloning the repository:

```bash
git config core.hooksPath .githooks
```

### Pre-commit hook

The pre-commit hook checks if you've bumped the version in `pyproject.toml` when you modify it. This ensures that version changes are not missed when making changes to the project configuration.

If you need to temporarily bypass this check, you can use:

```bash
git commit --no-verify
```

## Development with uv

This project uses uv for dependency management:

1. Install uv:
   ```bash
   pip install uv
   ```

2. Create a virtual environment:
   ```bash
   uv venv .venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Unix/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   uv pip install -e .
   uv pip install pytest
   ```

## Running Tests

```bash
python -m pytest
```

## Building and Publishing

Pushing to the master branch will automatically:
1. Run tests
2. Build the package
3. Create a GitHub release
4. Publish to PyPI

Make sure to update the version in `pyproject.toml` before pushing to master. 