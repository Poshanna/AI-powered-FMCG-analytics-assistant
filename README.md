# 📊 AI-Powered FMCG Analytics Assistant

An end-to-end conversational analytics platform that enables FMCG stakeholders to interact with business data using natural language. The application transforms user questions into SQL queries using Large Language Models (LLMs), retrieves data from a structured database, generates visualizations, and provides actionable business insights.

Developed as part of an AI Engineering Internship Assessment, this project demonstrates the complete lifecycle of building and deploying an AI-powered application—from synthetic data generation to production deployment.

---

## 🌐 Live Demo

🔗 https://ai-powered-fmcg-analytics-assistant-tfexzq4jk8teqcwr9chrw4.streamlit.app/

> **Note:** The application uses the Google Gemini API for Text-to-SQL generation and business insight creation. Depending on API quota availability, users may need to configure a valid Gemini API key.

---

## 🎯 Problem Statement

FMCG organizations generate vast amounts of operational data every day. However, obtaining business insights often requires SQL expertise and support from data analysts.

Common challenges include:

- Business users cannot directly query data.
- Analysts spend significant time answering repetitive questions.
- Decision-making is delayed due to technical dependencies.
- Non-technical stakeholders struggle to interpret analytical outputs.

### Objective

To build an AI-powered conversational assistant that enables users to ask business questions in natural language and instantly receive insights without requiring SQL knowledge.

---

## 🚀 Features

### 💬 Natural Language Analytics
Ask business questions in plain English without writing SQL.

### 🤖 AI-Powered Text-to-SQL
Uses Google Gemini to convert natural language questions into executable SQLite queries.

### 🔒 SQL Validation Layer
Ensures safe execution by allowing only valid SELECT statements and blocking destructive operations.

### 📊 Interactive Visualizations
Automatically generates charts and graphs using Plotly based on query results.

### 📈 Business Insight Generation
Provides concise AI-generated explanations and interpretations of analytical outputs.

### 🏪 Synthetic FMCG Dataset
Simulates realistic FMCG business scenarios including promotions, stockouts, and regional variations.

### ☁️ Cloud Deployment
Deployed using Streamlit Cloud for easy accessibility.

---

## 🏗️ System Architecture

```text
Business User
      ↓
Streamlit Interface
      ↓
Google Gemini API
(Text-to-SQL)
      ↓
SQL Validator
      ↓
SQLite Database
      ↓
Query Executor
      ↓
Plotly Visualizations
      ↓
Insight Generator
      ↓
Business Insights
```

---

## 📂 Project Structure

```text
AI-powered-FMCG-analytics-assistant/
│
├── app.py
├── init_db.py
├── fmcg.db
├── requirements.txt
├── README.md
│
├── sales.csv
├── inventory.csv
├── products.csv
├── stores.csv
│
├── tests/
│   ├── __init__.py
│   ├── test_query_executor.py
│   ├── test_sql_validator.py
│   └── test_visualizer.py
│
├── utils/
│   ├── __init__.py
│   ├── llm.py
│   ├── sql_generator.py
│   ├── sql_validator.py
│   ├── query_executor.py
│   ├── visualizer.py
│   └── insight_generator.py
│
└── screenshots/
```

---

## 📊 Synthetic Dataset Design

Since no real dataset was provided, a synthetic FMCG beverage dataset was created to closely resemble real-world business operations.

### Dataset Composition

- 24 weeks of historical data
- 20 beverage products
- 40 retail stores
- 4 geographical regions
- Multiple store formats:
  - Supermarkets
  - Hypermarkets
  - Convenience Stores
  - Wholesale Outlets

### Dataset Files

- `sales.csv`
- `inventory.csv`
- `products.csv`
- `stores.csv`

---

## 🧠 Edge Case Modeling

The dataset incorporates realistic business complexities.

### Promotion Variability

- Price Cut promotions
- Buy-One-Get-One (BOGO) campaigns
- Display promotions
- Low-performing promotions

### Inventory Challenges

- Stockout scenarios
- Inventory depletion
- Lost sales opportunities
- Closing stock reaching zero

### Regional Demand Differences

- Region-specific purchasing behavior
- Product preference variations

### Store Format Effects

- Higher traffic in Hypermarkets
- Lower inventory buffers in Convenience Stores
- Bulk ordering patterns in Wholesale outlets

---

## 🔧 Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| LLM | Google Gemini API |
| Data Processing | Pandas |
| Visualization | Plotly |
| Testing | Pytest |

---

## 💡 Example Questions

The assistant can answer questions such as:

- Which region generated the highest revenue?
- Compare North and South sales.
- Which products had the highest stockouts?
- Did BOGO promotions improve sales?
- What were the top-selling products?
- Which store formats performed best?
- Which categories generated the highest revenue?

---

## 🔒 Security and Validation

To ensure safe execution:

- Only `SELECT` statements are allowed.
- SQL syntax is validated before execution.
- Database schema compliance is enforced.
- Dangerous SQL keywords are blocked.
- Query execution is isolated from user input.

---

## ⚙️ Local Setup

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-powered-FMCG-analytics-assistant.git
cd AI-powered-FMCG-analytics-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Gemini API Key

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

### Run the Application

```bash
streamlit run app.py
```

---

## ☁️ Deployment

The application is deployed on Streamlit Cloud.

### Live Application

https://ai-powered-fmcg-analytics-assistant-tfexzq4jk8teqcwr9chrw4.streamlit.app/

---

## 🧪 Testing

Run unit tests using:

```bash
pytest
```

The test suite covers:

- SQL validation
- Query execution
- Visualization generation

---

## 🚧 Challenges Faced

During development, several challenges were encountered:

- Gemini API quota limitations and expired API keys.
- Handling invalid SQL generated by the LLM.
- Designing a secure SQL validation mechanism.
- Creating realistic synthetic datasets without access to real FMCG data.
- Deploying API-driven applications using Streamlit Secrets.
- Dataset creation.
---

## 📈 Business Impact

This solution enables:

- Faster access to insights.
- Reduced dependency on technical teams.
- Improved decision-making speed.
- Enhanced accessibility for non-technical users.
- Better understanding of sales, inventory, and promotional performance.

---

## 🔮 Future Enhancements

Planned improvements include:

- Multi-database support (PostgreSQL, MySQL, Snowflake).
- Conversational memory for follow-up questions.
- Exportable reports and dashboards.
- Sales forecasting and predictive analytics.
- Role-based authentication and authorization.
- Fallback SQL generation mechanisms.

---

## 👨‍💻 Author

### Poshanna Durki

