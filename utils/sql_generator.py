import logging
from .llm import LLMHandler

logger = logging.getLogger(__name__)

DATABASE_SCHEMA = """
Database Schema for FMCG Database:

Table: sales
Columns:
- week_start_date (TEXT, DATE)
- product_id (TEXT)
- store_id (TEXT)
- region (TEXT)
- units_sold (INTEGER)
- revenue (REAL)
- promotion_flag (BOOLEAN)
- promotion_type (TEXT, nullable)
- discount_pct (REAL)

Table: inventory
Columns:
- week_start_date (TEXT, DATE)
- product_id (TEXT)
- store_id (TEXT)
- opening_stock (INTEGER)
- units_received (INTEGER)
- units_sold (INTEGER)
- closing_stock (INTEGER)
- stockout_flag (BOOLEAN)

Table: products
Columns:
- product_id (TEXT, PRIMARY KEY)
- product_name (TEXT)
- brand (TEXT)
- category (TEXT)
- sub_category (TEXT)
- pack_size_ml (INTEGER)
- unit_price (REAL)

Table: stores
Columns:
- store_id (TEXT, PRIMARY KEY)
- store_name (TEXT)
- region (TEXT)
- city (TEXT)
- store_format (TEXT)

Table Relationships:
- sales.product_id = products.product_id
- sales.store_id = stores.store_id
- inventory.product_id = products.product_id
- inventory.store_id = stores.store_id
- sales.week_start_date = inventory.week_start_date
"""

EXAMPLE_QUERIES = """
Example Queries:

1. Which region generated the highest revenue?
SELECT region,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC
LIMIT 1;

2. Compare North and South sales.
SELECT region,
       SUM(revenue) AS total_revenue,
       SUM(units_sold) AS total_units
FROM sales
WHERE region IN ('North', 'South')
GROUP BY region;

3. Which products had the highest stockouts?
SELECT p.product_name,
       COUNT(*) AS stockout_count
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
WHERE i.stockout_flag = 1
GROUP BY p.product_name
ORDER BY stockout_count DESC;

4. Did BOGO promotions improve sales?
SELECT promotion_type,
       AVG(units_sold) AS avg_units_sold,
       AVG(revenue) AS avg_revenue
FROM sales
WHERE promotion_type = 'BOGO'
GROUP BY promotion_type;
"""


class SQLGenerator:
    """
    Converts natural language questions into SQLite SELECT queries.
    """

    def __init__(self, llm_handler: LLMHandler):
        self.llm = llm_handler

    def generate_sql(self, user_question: str) -> str:
        """
        Generate a SQL query from a natural language question.
        """

        prompt = f"""
You are an expert SQLite query generator.

Convert the user's question into a VALID SQLite SELECT query.

DATABASE SCHEMA:
{DATABASE_SCHEMA}

EXAMPLE QUERIES:
{EXAMPLE_QUERIES}

STRICT RULES:
1. Return ONLY the SQL query.
2. The output MUST start with SELECT.
3. Do NOT include explanations.
4. Do NOT include markdown code blocks.
5. Do NOT include words like "sqlite", "SQL Query", etc.
6. Only generate SELECT statements.
7. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE statements.
8. Use exact table and column names from the schema.
9. Use JOINs when necessary.
10. Use meaningful aliases.

User Question:
{user_question}
"""

        try:
            response = self.llm.generate(
                prompt,
                temperature=0.0
            )

            sql = response.strip()

            # Remove markdown blocks
            sql = sql.replace("```sql", "")
            sql = sql.replace("```", "")

            # Remove extra prefixes before SELECT
            upper_sql = sql.upper()

            if "SELECT" in upper_sql:
                start_index = upper_sql.find("SELECT")
                sql = sql[start_index:]

            # Remove trailing semicolons/newlines
            sql = sql.strip()

            logger.info(f"Generated SQL: {sql}")

            return sql

        except Exception as e:
            logger.error(
                f"SQL generation failed: {str(e)}"
            )
            raise
