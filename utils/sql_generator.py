
import logging
from typing import Tuple
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
Example queries:
1. Which region generated the highest revenue?
SELECT region, SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC
LIMIT 1;

2. Compare North and South sales.
SELECT region, SUM(revenue) AS total_revenue, SUM(units_sold) AS total_units
FROM sales
WHERE region IN ('North', 'South')
GROUP BY region;

3. Which products had the highest stockouts?
SELECT p.product_name, COUNT(*) AS stockout_count
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.stockout_flag = 1
GROUP BY p.product_name
ORDER BY stockout_count DESC;

4. Did BOGO promotions improve sales?
SELECT 
    s.promotion_type,
    AVG(s.units_sold) AS avg_units_sold,
    AVG(s.revenue) AS avg_revenue
FROM sales s
WHERE s.promotion_type = 'BOGO' OR s.promotion_flag = 0
GROUP BY s.promotion_type, s.promotion_flag;
"""

class SQLGenerator:
    def __init__(self, llm_handler: LLMHandler):
        self.llm = llm_handler
    
    def generate_sql(self, user_question: str) -> str:
        prompt = f"""
You are a SQLite query generator. Your task is to convert natural language questions about FMCG data into valid SQLite SELECT statements.

{DATABASE_SCHEMA}

{EXAMPLE_QUERIES}

IMPORTANT RULES:
1. Only generate SELECT statements - NO INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE statements allowed.
2. Use only SQLite syntax.
3. Ensure all table and column names exactly match the schema provided.
4. Always use proper JOIN syntax when combining tables are needed.
5. Do not include any explanations or extra text, only the SQL query.
6. For date comparisons, use date strings in 'YYYY-MM-DD' format.
7. Handle NULL values appropriately.
8. Use meaningful aliases for aggregated columns.

User Question: {user_question}

Output only the SQL query:
"""
        
        try:
            sql = self.llm.generate(prompt, temperature=0.0)
            sql = sql.strip()
            if sql.startswith("```sql"):
                sql = sql[6:]
            if sql.startswith("```"):
                sql = sql[3:]
            if sql.endswith("```"):
                sql = sql[:-3]
            return sql.strip()
        except Exception as e:
            logger.error(f"SQL generation failed: {str(e)}")
            raise
