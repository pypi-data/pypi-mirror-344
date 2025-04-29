import unittest
from tsql import sql

class TestTSQL(unittest.TestCase):
    def test_basic_formatting(self):
        # Note: This test requires Python 3.14+ to run
        # The t-string prefix is used in the actual code
        query = sql("SELECT * FROM users WHERE id = {user_id}")
        formatted = query.format(user_id=123)
        self.assertEqual(formatted, "SELECT * FROM users WHERE id = 123")
        
    def test_multiple_params(self):
        query = sql("SELECT * FROM {table} WHERE {column} = {value}")
        formatted = query.format(table="users", column="email", value="'user@example.com'")
        self.assertEqual(formatted, "SELECT * FROM users WHERE email = 'user@example.com'")

if __name__ == "__main__":
    unittest.main()