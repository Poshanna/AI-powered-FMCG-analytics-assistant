
# AI-Powered FMCG Analytics Assistant

A conversational AI assistant that allows business users to query FMCG (Fast-Moving Consumer Goods) data using natural language, powered by Google Gemini and Streamlit.

## Project Overview

This application bridges the gap between business users and data analysts by enabling natural language questions about sales, inventory, promotions, and store performance. The assistant handles intent understanding, SQL generation, query validation, execution, visualization, and insight generation in a single seamless workflow.

## Architecture

```
User Question
    ↓
Gemini Intent Understanding
    ↓
Text-to-SQL Generation
    ↓
SQL Validation Layer
    ↓
SQLite Query Execution
    ↓
Plotly Visualization
    ↓
Gemini Business Insight Generation
    ↓
Response to User
```

## Features

- 🗣️ **Natural Language Interface**: Ask questions in plain English
- 🔍 **Text-to-SQL Generation**: Powered by Google Gemini
- ✅ **SQL Validation**: Security and syntax checks before execution
- 📊 **Interactive Visualizations**: Auto-generated charts with Plotly
- 💡 **Business Insights**: AI-generated actionable insights
- 📱 **Clean UI**: Built with Streamlit for ease of use

## Example Questions

Try asking questions like:

- Which region generated the highest revenue?
- Compare North and South sales performance.
- Which products experienced the most stockouts?
- Did BOGO promotions improve sales?
- What were the top-selling products?
- Which store formats performed best?
- Which promotion type delivered the highest uplift?
- Which categories performed best during promotions?

## Local Setup

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database (if needed):
   ```bash
   python init_db.py
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Environment Variable Setup

For local development, you can set the API key in two ways:

### Option 1: Enter in UI
Run the app and enter your API key directly in the web interface.

### Option 2: Environment Variable
Set the `GEMINI_API_KEY` environment variable:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**macOS/Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Streamlit Deployment

The application is ready to deploy to Streamlit Cloud!

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect your repository
4. In the app settings, add a secret with key `GEMINI_API_KEY` and your API key as the value

## Project Structure

```
fmcg-ai-assistant/
├── app.py                      # Main Streamlit app
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── fmcg.db                     # SQLite database (generated)
├── utils/                      # Utility modules
│   ├── llm.py                  # LLM handling
│   ├── sql_generator.py        # Text-to-SQL
│   ├── sql_validator.py        # SQL validation
│   ├── query_executor.py       # Query execution
│   ├── visualizer.py           # Visualization generation
│   └── insight_generator.py    # Business insights
├── .streamlit/
│   └── secrets.toml.example    # Example secrets config
├── tests/                      # Test cases
└── screenshots/                # Screenshots directory
```

## Limitations

- **SQL Generation**: While powerful, the LLM may occasionally generate invalid or suboptimal SQL for very complex queries
- **Data Scope**: Limited to the data available in the SQLite database
- **Conversational Memory**: Current version doesn't maintain context across multiple questions
- **Visualization**: Chart type selection is heuristic and may not always be optimal

## Future Improvements (Version 2)

- [ ] **Conversational Memory**: Maintain context across multiple questions for follow-up queries
- [ ] **Multi-Agent Validation**: Add a second LLM check for critical queries
- [ ] **Role-Based Access Control**: Different permissions for different user roles
- [ ] **Enterprise Database Connectivity**: Support for PostgreSQL, BigQuery, Snowflake, etc.
- [ ] **Fine-Tuned Text-to-SQL Model**: Train a custom model on FMCG-specific queries
- [ ] **Query History**: Save and revisit past queries
- [ ] **Export Options**: Export results to Excel/PDF
- [ ] **Scheduled Reports**: Generate and send reports on a schedule

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
