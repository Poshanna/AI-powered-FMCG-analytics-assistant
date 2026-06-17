
import plotly.express as px
import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Visualizer:
    def determine_chart_type(self, df: pd.DataFrame) -> str:
        """
        Determine appropriate chart type based on data structure:
        - Line chart: time series (has date column)
        - Pie chart: 1 categorical, 1 numeric column (<=10 categories)
        - Bar chart: everything else
        """
        columns = df.columns.tolist()
        
        # Check for time series
        date_cols = [col for col in columns if 'date' in col.lower() or 'week' in col.lower()]
        if date_cols and len(columns) >= 2:
            # Check if date column is actually a date
            try:
                pd.to_datetime(df[date_cols[0]])
                return "line"
            except:
                pass
        
        # Check for pie chart (1 categorical, 1 numeric, <=10 categories)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(numeric_cols) == 1 and len(categorical_cols) == 1 and len(df) <= 10:
            return "pie"
        
        # Default to bar chart
        return "bar"

    def create_chart(self, df: pd.DataFrame, chart_type: Optional[str] = None):
        try:
            if chart_type is None:
                chart_type = self.determine_chart_type(df)
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if chart_type == "line":
                date_cols = [col for col in df.columns if 'date' in col.lower() or 'week' in col.lower()]
                if date_cols:
                    x_col = date_cols[0]
                    y_cols = numeric_cols[:2] if len(numeric_cols) > 1 else numeric_cols
                    fig = px.line(df, x=x_col, y=y_cols, title="Trend Over Time")
                else:
                    chart_type = "bar"
            
            if chart_type == "bar":
                if categorical_cols:
                    x_col = categorical_cols[0]
                    y_cols = numeric_cols[:2] if len(numeric_cols) > 1 else numeric_cols
                    fig = px.bar(df, x=x_col, y=y_cols, title="Comparison Chart", barmode='group')
                else:
                    return None
            
            if chart_type == "pie":
                if categorical_cols and numeric_cols:
                    fig = px.pie(df, names=categorical_cols[0], values=numeric_cols[0], title="Distribution")
                else:
                    return None
            
            fig.update_layout(height=400)
            return fig
            
        except Exception as e:
            logger.error(f"Visualization creation failed: {str(e)}")
            return None
