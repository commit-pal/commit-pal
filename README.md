# commit-pal ⚡️

A CLI AI assistant that helps you write commit messages at the speed of light using locally run LLMs.

## Quick Start

### Install and setup commit-pal

Install the latest version of `commit-pal` from PyPI:

```bash
pip install commit-pal
```

```bash
cm --setup # Configure the style of the commit messages
```

### Run LLM locally with Ollama

- [Ollama](https://ollama.com/download) should be installed and running
- Pull and run a model to use with the library: `ollama run <model>` e.g. `ollama run qwen2.5-coder:7b`
  - See [Ollama.com](https://ollama.com/search) for more information on the models available.
  - We have seen the best performance with [qwen2.5-coder:7b](https://ollama.com/library/qwen2.5-coder:7b) model so far.

By default, Ollama will run on `localhost:11434`.

### Generate commit message

After staging your changes, run the following command to generate a commit message:

```bash
cm
```

The proposed commit message will be displayed in the terminal for you to review and confirm

## Development Setup

### Install Poetry

Please follow the official [installation guide](https://python-poetry.org/docs/#installation) to install Poetry, which will be used to manage dependencies and environments.

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

### Style Enforcement

```bash
make lint
```

### Quick Start to Test CLI App

```bash
pip uninstall cm -y # Uninstall old version of commit-pal
pip install -e . -v # Install new version of commit-pal
cm # Run commit-pal
```

### Publish to PyPI

```bash
# Bump the semantic version in pyproject.toml before running this command
make publish
```
