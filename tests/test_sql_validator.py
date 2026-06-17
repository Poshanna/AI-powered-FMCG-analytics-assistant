
import unittest
from utils import SQLValidator

class TestSQLValidator(unittest.TestCase):
    def setUp(self):
        self.validator = SQLValidator()
    
    def test_valid_select_query(self):
        sql = "SELECT region, SUM(revenue) FROM sales GROUP BY region"
        is_valid, error = self.validator.validate(sql)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_blocked_keyword(self):
        sql = "INSERT INTO sales VALUES (1, 2, 3)"
        is_valid, error = self.validator.validate(sql)
        self.assertFalse(is_valid)
        self.assertIn("Blocked keyword", error)
    
    def test_invalid_table(self):
        sql = "SELECT * FROM invalid_table"
        is_valid, error = self.validator.validate(sql)
        self.assertFalse(is_valid)
    
    def test_non_select_query(self):
        sql = "UPDATE sales SET revenue = 100"
        is_valid, error = self.validator.validate(sql)
        self.assertFalse(is_valid)
        self.assertIn("Only SELECT queries", error)

if __name__ == "__main__":
    unittest.main()
