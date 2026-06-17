import streamlit as st
import logging
from utils import (
    LLMHandler,
    SQLGenerator,
    SQLValidator,
    QueryExecutor,
    Visualizer,
    InsightGenerator
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page Config
st.set_page_config(
    page_title="AI-Powered FMCG Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered FMCG Analytics Assistant")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
A conversational AI assistant for FMCG business analytics.

Ask natural language questions about:
- Sales
- Promotions
- Inventory
- Regional Performance
""")

    st.subheader("Example Questions")

    example_questions = [
        "Which region generated the highest revenue?",
        "Compare North and South sales.",
        "Which products had the highest stockouts?",
        "Did BOGO promotions improve sales?",
        "What were the top-selling products?",
        "Which store formats performed best?"
    ]

    for q in example_questions:
        if st.button(q):
            st.session_state.messages.append(
                {"role": "user", "content": q}
            )

    st.subheader("Database Statistics")

    try:
        query_executor = QueryExecutor()
        stats_df = query_executor.get_table_stats()
        st.dataframe(stats_df, hide_index=True)

    except Exception as e:
        st.error(f"Could not load database stats: {e}")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# API Key
if not st.session_state.api_key:
    st.info("Please enter your Gemini API key.")

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    if api_key:
        st.session_state.api_key = api_key
        st.rerun()

    st.stop()

# Display History
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "sql" in message:
            with st.expander("Generated SQL"):
                st.code(message["sql"], language="sql")

        if "data" in message:
            st.dataframe(message["data"], hide_index=True)

        if "chart" in message and message["chart"] is not None:
            st.plotly_chart(
                message["chart"],
                use_container_width=True
            )

        if "insights" in message and message["insights"]:
            with st.expander("Business Insights"):
                st.markdown(message["insights"])

# User Input
user_input = st.chat_input(
    "Ask a question about FMCG data..."
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        try:
            with st.spinner("Processing..."):

                llm = LLMHandler(
                    api_key=st.session_state.api_key
                )

                sql_generator = SQLGenerator(llm)

                sql_validator = SQLValidator()

                query_executor = QueryExecutor()

                visualizer = Visualizer()

                insight_generator = InsightGenerator(llm)

                # Generate SQL
                sql = sql_generator.generate_sql(user_input)

                # DEBUG
                st.subheader("🔍 Generated SQL")
                st.code(sql, language="sql")

                # Validate SQL
                is_valid, error = sql_validator.validate(sql)

                if not is_valid:

                    st.error(
                        f"Validation Error: {error}"
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content":
                            f"Validation Error: {error}",
                            "sql": sql
                        }
                    )

                else:

                    # Execute Query
                    df, query_error = query_executor.execute(sql)

                    if query_error:

                        st.error(
                            f"Query Error: {query_error}"
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content":
                                f"Query Error: {query_error}",
                                "sql": sql
                            }
                        )

                    elif df is None or df.empty:

                        st.warning(
                            "No results found."
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content":
                                "No results found.",
                                "sql": sql
                            }
                        )

                    else:

                        # Visualization
                        fig = visualizer.create_chart(df)

                        # Insights
                        insights = (
                            insight_generator
                            .generate_insights(
                                user_input,
                                sql,
                                df
                            )
                        )

                        response = (
                            "Here's what I found!"
                        )

                        st.markdown(response)

                        with st.expander(
                            "Generated SQL"
                        ):
                            st.code(
                                sql,
                                language="sql"
                            )

                        st.dataframe(
                            df,
                            hide_index=True
                        )

                        if fig is not None:
                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                        if insights:
                            with st.expander(
                                "Business Insights"
                            ):
                                st.markdown(
                                    insights
                                )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": response,
                                "sql": sql,
                                "data": df,
                                "chart": fig,
                                "insights": insights
                            }
                        )

        except Exception as e:

            logger.error(
                str(e),
                exc_info=True
            )

            st.error(
                f"An error occurred: {str(e)}"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content":
                    f"An error occurred: {str(e)}"
                }
            )
