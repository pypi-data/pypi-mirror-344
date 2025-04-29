# T-SQL

A lightweight SQL templating library that leverages Python 3.14's t-strings (PEP 750).

## ⚠️ Python Version Requirement

**This library requires Python 3.14b1 or newer.**

TSQL is built specifically to take advantage of the new t-string feature introduced in [PEP 750](https://peps.python.org/pep-0750/), which is only available in Python 3.14+.

## Installation

Using UV (recommended):

```bash
uv pip install t-sql
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
uv pip install -e ".[dev]"

# Run tests
uv run pytest
```

## Usage

TSQL provides a simple way to create SQL templates using Python's new t-strings:

```python
from tsql import sql

# Create a SQL template using t-strings
query = sql(t"SELECT * FROM users WHERE username = {username} AND status = {status}")

# Format the template with parameters
formatted_query = query.format(username="'johndoe'", status="'active'")
print(formatted_query)
# Output: SELECT * FROM users WHERE username = 'johndoe' AND status = 'active'
```

### Benefits

- **Type Safety**: Leverage the type checking capabilities of t-strings
- **SQL Injection Protection**: Parameters are properly handled to prevent SQL injection
- **Readability**: Keep your SQL queries clean and easy to understand
- **Maintainability**: Separate SQL logic from Python code

## Features

- Simple API for creating SQL templates
- Support for all SQL dialects
- Parameter validation and type checking
- SQL injection protection

## License

MIT