
import unittest
import pandas as pd
from utils import Visualizer

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = Visualizer()
    
    def test_determine_chart_type_bar(self):
        df = pd.DataFrame({
            "region": ["North", "South", "East", "West"],
            "revenue": [1000, 2000, 1500, 1800]
        })
        chart_type = self.visualizer.determine_chart_type(df)
        self.assertEqual(chart_type, "bar")
    
    def test_determine_chart_type_pie(self):
        df = pd.DataFrame({
            "category": ["A", "B", "C"],
            "sales": [500, 300, 200]
        })
        chart_type = self.visualizer.determine_chart_type(df)
        self.assertEqual(chart_type, "pie")
    
    def test_determine_chart_type_line(self):
        df = pd.DataFrame({
            "week_start_date": ["2024-01-01", "2024-01-08", "2024-01-15"],
            "revenue": [1000, 1200, 1100]
        })
        chart_type = self.visualizer.determine_chart_type(df)
        self.assertEqual(chart_type, "line")
    
    def test_create_chart(self):
        df = pd.DataFrame({
            "region": ["North", "South", "East", "West"],
            "revenue": [1000, 2000, 1500, 1800]
        })
        fig = self.visualizer.create_chart(df)
        self.assertIsNotNone(fig)

if __name__ == "__main__":
    unittest.main()
