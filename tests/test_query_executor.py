
import unittest
import os
from utils import QueryExecutor

class TestQueryExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = QueryExecutor()
    
    def test_execute_valid_query(self):
        sql = "SELECT COUNT(*) FROM sales"
        df, error = self.executor.execute(sql)
        self.assertIsNotNone(df)
        self.assertIsNone(error)
        self.assertEqual(len(df), 1)
    
    def test_execute_invalid_query(self):
        sql = "SELECT * FROM nonexistent_table"
        df, error = self.executor.execute(sql)
        self.assertIsNone(df)
        self.assertIsNotNone(error)
    
    def test_get_table_stats(self):
        stats_df = self.executor.get_table_stats()
        self.assertIsNotNone(stats_df)
        self.assertGreater(len(stats_df), 0)
        self.assertIn("Table Name", stats_df.columns)
        self.assertIn("Row Count", stats_df.columns)

if __name__ == "__main__":
    unittest.main()
