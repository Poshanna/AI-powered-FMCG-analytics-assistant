import logging
import sqlite3
import re
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SQLValidator:
    ALLOWED_TABLES = {"sales", "inventory", "products", "stores"}

    BLOCKED_KEYWORDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "EXECUTE",
        "EXEC",
        "ATTACH",
        "DETACH",
        "PRAGMA"
    }

    def __init__(self, db_path: str = "fmcg.db"):
        self.db_path = db_path

    def validate(self, sql: str) -> Tuple[bool, Optional[str]]:
        """
        Validate SQL query.
        Returns:
            (True, None) if valid
            (False, error_message) if invalid
        """

        if not sql:
            return False, "Empty SQL query."

        sql = sql.strip()

        # Remove markdown blocks
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

        upper_sql = sql.upper()

        # Extract SQL from first SELECT onwards
        if "SELECT" in upper_sql:
            start = upper_sql.find("SELECT")
            sql = sql[start:]
            upper_sql = sql.upper()

        # Must start with SELECT
        if not upper_sql.startswith("SELECT"):
            return False, "Only SELECT queries are allowed."

        # Check blocked keywords
        for keyword in self.BLOCKED_KEYWORDS:
            if re.search(rf"\b{keyword}\b", upper_sql):
                return False, f"Blocked keyword '{keyword}' found."

        # Validate tables
        tables = self._extract_tables(sql)

        for table in tables:
            if table not in self.ALLOWED_TABLES:
                return False, f"Invalid table name: {table}"

        # SQLite syntax validation
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                f"EXPLAIN QUERY PLAN {sql}"
            )

            conn.close()

        except sqlite3.Error as e:
            logger.error(f"SQL syntax error: {str(e)}")
            return False, f"SQL syntax error: {str(e)}"

        return True, None

    def _extract_tables(self, sql: str) -> set:
        tables = set()

        from_pattern = r"\bfrom\s+(\w+)"
        join_pattern = r"\bjoin\s+(\w+)"

        for match in re.finditer(
            from_pattern,
            sql,
            re.IGNORECASE
        ):
            tables.add(match.group(1).lower())

        for match in re.finditer(
            join_pattern,
            sql,
            re.IGNORECASE
        ):
            tables.add(match.group(1).lower())

        return tables
