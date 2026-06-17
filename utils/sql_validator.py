
import logging
import sqlite3
import re
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class SQLValidator:
    ALLOWED_TABLES = {"sales", "inventory", "products", "stores"}
    ALLOWED_COLUMNS = {
        "sales": ["week_start_date", "product_id", "store_id", "region", "units_sold", "revenue", "promotion_flag", "promotion_type", "discount_pct"],
        "inventory": ["week_start_date", "product_id", "store_id", "opening_stock", "units_received", "units_sold", "closing_stock", "stockout_flag"],
        "products": ["product_id", "product_name", "brand", "category", "sub_category", "pack_size_ml", "unit_price"],
        "stores": ["store_id", "store_name", "region", "city", "store_format"]
    }
    BLOCKED_KEYWORDS = {
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
        "EXECUTE", "EXEC", "UNION", "UNION ALL", "INTERSECT", "EXCEPT"
    }

    def __init__(self, db_path: str = "fmcg.db"):
        self.db_path = db_path

    def validate(self, sql: str) -> Tuple[bool, Optional[str]]:
        """
        Validate SQL query.
        Returns (is_valid, error_message)
        """
        sql_upper = sql.upper().strip()

        # Check 1: Must be SELECT only
        if not sql_upper.startswith("SELECT"):
            return False, "Only SELECT queries are allowed."

        # Check 2: No blocked keywords
        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in sql_upper:
                return False, f"Blocked keyword '{keyword}' found."

        # Check 3: Table names are valid
        tables = self._extract_tables(sql)
        for table in tables:
            if table not in self.ALLOWED_TABLES:
                return False, f"Invalid table name: {table}"

        # Check 4: Column names are valid
        columns, tables_used = self._extract_columns_and_tables(sql)
        for table in tables_used:
            if table not in self.ALLOWED_TABLES:
                continue
            for col in columns:
                if "." in col:
                    tbl, col_name = col.split(".", 1)
                    if tbl in self.ALLOWED_TABLES and col_name not in self.ALLOWED_COLUMNS[tbl]:
                        return False, f"Invalid column {col} for table {tbl}"

        # Check 5: Basic syntax check using SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"SQL syntax error: {str(e)}")
            return False, f"SQL syntax error: {str(e)}"

        return True, None

    def _extract_tables(self, sql: str) -> set:
        tables = set()
        sql_lower = sql.lower()
        
        # Look for FROM, JOIN clauses
        from_pattern = r'\bfrom\s+(\w+)'
        join_pattern = r'\bjoin\s+(\w+)'
        
        for match in re.finditer(from_pattern, sql_lower, re.IGNORECASE):
            tables.add(match.group(1))
        for match in re.finditer(join_pattern, sql_lower, re.IGNORECASE):
            tables.add(match.group(1))
            
        return tables

    def _extract_columns_and_tables(self, sql: str) -> Tuple[set, set]:
        columns = set()
        tables = set()
        sql_lower = sql.lower()
        
        # Find all identifiers
        # This is a simplified approach - for production you'd use a proper SQL parser
        words = re.findall(r'\b\w+\b', sql)
        i = 0
        while i < len(words):
            word = words[i]
            if word in self.ALLOWED_TABLES:
                tables.add(word)
                if i + 2 < len(words) and words[i+1] == 'as':
                    alias = words[i+2]
            i += 1
            
        return columns, tables
