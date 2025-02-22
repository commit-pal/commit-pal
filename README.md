# commit-pal

A CLI AI assistant that helps you write commit messages at the speed of light

## Install Poetry

It is recommended to use Python virtual environment, so you don't pollute your system Python environment.

```bash
# Install dependencies
poetry install
```

```bash
# Activate Python Virtual Environment for Mac/Linux
eval "$(poetry env activate)"

# Activate Python Virtual Environment for Windows
.venv\Scripts\Activate.ps1
```

## Set up environment variables

```bash
# Create .env file (by copying from .env.example)
cp .env.example .env
```

## Run LLM Locally

- [Ollama](https://ollama.com/download) should be installed and running
- Pull a model to use with the library: `ollama pull <model>` e.g. `ollama pull llama3.2`
  - See [Ollama.com](https://ollama.com/search) for more information on the models available.

By default, Ollama will run on `localhost:11434`.

## Style Enforcement

```bash
make lint
```

## Quick Start to Test CLI App

```bash
pip uninstall cmpal -y # Uninstall old version of cmpal
pip install -e . -v # Install new version of cmpal
cmpal # Run cmpal
```

## Publish to PyPI

```bash
# Bump the semantic version in pyproject.toml before running this command
make publish
```

## Debugging notes

### Configure VSCode Python Interpreter to use Poetry's virtual environment

1. Close VSCode so that it is able to detect the newly created virtual environment. A lot of times, this alone is enough to fix the issue.
2. In the command palette, type `Python: Select Interpreter`
3. Type `poetry` in the search box
4. The first option should be what you want to use
