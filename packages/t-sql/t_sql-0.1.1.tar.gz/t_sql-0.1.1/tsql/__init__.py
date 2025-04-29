from .tsql import sql, SQLTemplate

__version__ = "0.1.0"
__all__ = ["sql", "SQLTemplate"]

# Package renamed to t-sql for PyPI compatibility
# but the import name remains 'tsql' for simplicity