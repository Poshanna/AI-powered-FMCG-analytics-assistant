
import logging
from typing import Optional
import pandas as pd
from .llm import LLMHandler

logger = logging.getLogger(__name__)

class InsightGenerator:
    def __init__(self, llm_handler: LLMHandler):
        self.llm = llm_handler

    def generate_insights(self, user_question: str, sql: str, df: pd.DataFrame) -> Optional[str]:
        try:
            data_str = df.to_csv(index=False)
            prompt = f"""
You are a business intelligence analyst. Your task is to generate concise, actionable business insights from the query results below.

User Question: {user_question}
SQL Query Executed: {sql}

Query Results:
{data_str}

Please provide:
1. A brief summary of what the data shows
2. Key findings or anomalies
3. Any business implications or recommendations

Guidelines:
- Use only the data provided - do not hallucinate or make up information
- Be concise (3-5 bullet points or short paragraphs)
- Use business-friendly language
- Focus on actionable insights

Insights:
"""
            
            insights = self.llm.generate(prompt, temperature=0.3)
            return insights
        except Exception as e:
            logger.error(f"Insight generation failed: {str(e)}")
            return None
