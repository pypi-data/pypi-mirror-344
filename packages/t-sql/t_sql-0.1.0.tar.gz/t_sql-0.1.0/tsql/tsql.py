import inspect
from typing import Any, Dict, Optional, TypeVar, cast

T = TypeVar("T")

class SQLTemplate:
    """SQL Template using t-strings."""
    
    def __init__(self, query_template: str):
        self.query_template = query_template
        
    def format(self, **kwargs: Any) -> str:
        """Format the SQL template with the provided parameters."""
        return self.query_template.format(**kwargs)
    
    def __repr__(self) -> str:
        return f"SQLTemplate({self.query_template!r})"


def sql(template: str) -> SQLTemplate:
    """
    Create an SQL template from a t-string.
    
    Example:
        query = sql(t"SELECT * FROM users WHERE id = {user_id}")
        formatted_query = query.format(user_id=123)
    """
    # In a real implementation, we would validate and process the template
    # to ensure it's a valid t-string and handle potential SQL injection
    return SQLTemplate(template)