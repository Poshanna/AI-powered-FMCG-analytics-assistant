
import sqlite3
import pandas as pd
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class QueryExecutor:
    def __init__(self, db_path: str = "fmcg.db"):
        self.db_path = db_path

    def execute(self, sql: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Execute SQL query and return DataFrame
        Returns (df, error_message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df, None
        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {str(e)}")
            return None, f"Query execution failed: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None, f"Unexpected error: {str(e)}"

    def get_table_stats(self) -> pd.DataFrame:
        """Get basic statistics about database tables"""
        stats = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = len(cursor.fetchall())
            stats.append({
                "Table Name": table_name,
                "Row Count": count,
                "Column Count": columns
            })
            
        conn.close()
        return pd.DataFrame(stats)
