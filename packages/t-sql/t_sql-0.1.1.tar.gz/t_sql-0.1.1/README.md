# T-SQL

A lightweight SQL templating library that leverages Python 3.14's t-strings (PEP 750).

NOTE: This library currently doesn't work. It is still under active developement and is being used to hold ideas.

## ⚠️ Python Version Requirement

**This library requires Python 3.14b1 or newer.**

TSQL is built specifically to take advantage of the new t-string feature introduced in [PEP 750](https://peps.python.org/pep-0750/), which is only available in Python 3.14+.

## Installation

Using UV (recommended):

```bash
uv add t-sql
```

Or using traditional pip:

```bash
pip install t-sql
```

## Development Setup

The project uses UV for dependency management:

```bash
# Install UV if you don't have it
curl -sSf https://install.python-uvx.us | python

# Install development dependencies
uv sync

# Run tests
uv run pytest

# build project
uv build

# publish to pypi
uv publish
```

## Usage

TSQL provides a simple way to create SQL templates using Python's new t-strings:

```python
import tsql

# Run a SQL template using t-strings
results = tsql.run(t"SELECT * FROM users WHERE username = {username} AND status = {status}")
```


### Benefits

- **SQL Injection Protection**: Parameters are properly handled to prevent SQL injection
- **Readability**: Keep your SQL queries clean and easy to understand
- **Maintainability**: Separate SQL logic from Python code

## Features

- SQL injection protection

## License

MIT
