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

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="AI-Powered FMCG Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered FMCG Analytics Assistant")

# -----------------------------
# Session State Initialization
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = None

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("About")
    st.write(
        """
        A conversational AI assistant for FMCG business analytics.

        Ask natural language questions about:
        - Sales
        - Promotions
        - Inventory
        - Regional Performance
        """
    )

    st.subheader("Example Questions")

    example_questions = [
        "Which region generated the highest revenue?",
        "Compare North and South sales.",
        "Which products had the highest stockouts?",
        "Did BOGO promotions improve sales?",
        "What were the top-selling products?",
        "Which store formats performed best?"
    ]

    for question in example_questions:
        if st.button(question):
            st.session_state.messages.append(
                {"role": "user", "content": question}
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

# -----------------------------
# API Key Section
# -----------------------------
if not st.session_state.api_key:
    st.info("Please enter your Google Gemini API key to get started.")

    api_key_input = st.text_input(
        "Gemini API Key",
        type="password"
    )

    if api_key_input:
        st.session_state.api_key = api_key_input
        st.rerun()

    st.stop()

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "sql" in message:
            with st.expander("Generated SQL"):
                st.code(message["sql"], language="sql")

        if "data" in message:
            st.dataframe(
                message["data"],
                hide_index=True
            )

        if "chart" in message and message["chart"] is not None:
            st.plotly_chart(
                message["chart"],
                use_container_width=True
            )

        if "insights" in message and message["insights"]:
            with st.expander("Business Insights"):
                st.markdown(message["insights"])

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input(
    "Ask a question about FMCG data..."
)

if user_input:

    # Display User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant Response
    with st.chat_message("assistant"):

        try:
            with st.spinner("Processing your request..."):

                # Initialize Components
                llm = LLMHandler(
                    api_key=st.session_state.api_key
                )

                sql_generator = SQLGenerator(llm)

                sql_validator = SQLValidator()

                query_executor = QueryExecutor()

                visualizer = Visualizer()

                insight_generator = InsightGenerator(llm)

                # -----------------------------
                # Step 1: Generate SQL
                # -----------------------------
                sql = sql_generator.generate_sql(
                    user_input
                )

                # -----------------------------
                # Step 2: Validate SQL
                # -----------------------------
                is_valid, validation_error = (
                    sql_validator.validate(sql)
                )

                if not is_valid:

                    error_message = (
                        f"Validation Error: "
                        f"{validation_error}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": (
                                "Sorry, I encountered "
                                f"an issue: {validation_error}"
                            )
                        }
                    )

                else:

                    # -----------------------------
                    # Step 3: Execute Query
                    # -----------------------------
                    df, query_error = (
                        query_executor.execute(sql)
                    )

                    if query_error:

                        st.error(
                            f"Query Error: {query_error}"
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": (
                                    "Sorry, I couldn't "
                                    "execute that query: "
                                    f"{query_error}"
                                )
                            }
                        )

                    elif df is None or df.empty:

                        st.warning(
                            "No results found "
                            "for your query."
                        )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": (
                                    "No results found "
                                    "for your query."
                                ),
                                "sql": sql
                            }
                        )

                    else:

                        # -----------------------------
                        # Step 4: Visualization
                        # -----------------------------
                        fig = visualizer.create_chart(df)

                        # -----------------------------
                        # Step 5: Insights
                        # -----------------------------
                        insights = (
                            insight_generator.generate_insights(
                                user_input,
                                sql,
                                df
                            )
                        )

                        response_message = (
                            "Here's what I found!"
                        )

                        # Display Output
                        st.markdown(response_message)

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

                        # Save Chat
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": response_message,
                                "sql": sql,
                                "data": df,
                                "chart": fig,
                                "insights": insights
                            }
                        )

        except Exception as e:

            logger.error(
                f"Unexpected error: {str(e)}",
                exc_info=True
            )

            st.error(
                f"An error occurred: {str(e)}"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "Sorry, I encountered "
                        f"an error: {str(e)}"
                    )
                }
            )