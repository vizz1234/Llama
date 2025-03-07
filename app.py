import streamlit as st
import asyncio
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, insert
from llama_index.core import SQLDatabase, VectorStoreIndex, Document
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
from pathlib import Path

from sql_router import (
    RouterOutputAgentWorkflow,
    llama_cloud_tool,
    create_llama_tool
)

# Initialize session state for custom mode
if 'custom_mode' not in st.session_state:
    st.session_state.custom_mode = False
if 'custom_sql_tool' not in st.session_state:
    st.session_state.custom_sql_tool = None
if 'custom_llama_tool' not in st.session_state:
    st.session_state.custom_llama_tool = None

# Default database setup
engine = create_engine("sqlite:///:memory:", future=True)
metadata_obj = MetaData()

# Create city stats table
table_name = "city_stats"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("state", String(16), nullable=False),
)

metadata_obj.create_all(engine)

# Insert initial data
cities = ["New York City", "Los Angeles", "Chicago", "Houston", "Miami", "Seattle"]
rows = [
    {"city_name": "New York City", "population": 8336000, "state": "New York"},
    {"city_name": "Los Angeles", "population": 3822000, "state": "California"},
    {"city_name": "Chicago", "population": 2665000, "state": "Illinois"},
    {"city_name": "Houston", "population": 2303000, "state": "Texas"},
    {"city_name": "Miami", "population": 449514, "state": "Florida"},
    {"city_name": "Seattle", "population": 749256, "state": "Washington"},
]

for row in rows:
    stmt = insert(city_stats_table).values(**row)
    with engine.begin() as connection:
        connection.execute(stmt)

# Create default SQL tool
sql_database = SQLDatabase(engine, include_tables=[table_name])
sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=[table_name]
)

default_sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description=(
        "Useful for translating a natural language query into a SQL query over"
        " a table containing: city_stats, containing the population/state of"
        " each city located in the USA."
    ),
    name="sql_tool"
)

def create_custom_sql_tool(df, table_name="custom_stats"):
    # Create database engine and tables
    engine = create_engine("sqlite:///:memory:", future=True)
    metadata_obj = MetaData()

    # Dynamically create table columns based on DataFrame
    columns = []
    for col_name, dtype in df.dtypes.items():
        if dtype == 'object':
            columns.append(Column(col_name, String(255)))
        elif dtype == 'int64':
            columns.append(Column(col_name, Integer))

    # Create table
    custom_table = Table(table_name, metadata_obj, *columns)
    metadata_obj.create_all(engine)

    # Insert data
    with engine.begin() as connection:
        for _, row in df.iterrows():
            stmt = insert(custom_table).values(**row.to_dict())
            connection.execute(stmt)

    # Create SQL database and query engine
    sql_database = SQLDatabase(engine, include_tables=[table_name])
    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=[table_name]
    )

    return QueryEngineTool.from_defaults(
        query_engine=sql_query_engine,
        description=f"Useful for querying the {table_name} table containing custom data.",
        name="sql_tool"
    )

def load_pdfs(pdf_files):
    documents = []
    for pdf_file in pdf_files:
        with open(f"temp_{pdf_file.name}", "wb") as f:
            f.write(pdf_file.getvalue())
        text_path = Path(f"temp_{pdf_file.name}")
        documents.append(Document.from_file(str(text_path)))
        text_path.unlink()
    
    index = VectorStoreIndex.from_documents(documents)
    return index

st.title("City Information Query System")

# Add toggle for custom mode
custom_mode = st.sidebar.checkbox("Use Custom Data", value=st.session_state.custom_mode)

if custom_mode and not st.session_state.custom_mode:
    # Switching to custom mode
    st.session_state.custom_mode = True
    st.rerun()
elif not custom_mode and st.session_state.custom_mode:
    # Switching back to default mode
    st.session_state.custom_mode = False
    st.session_state.custom_sql_tool = None
    st.session_state.custom_llama_tool = None
    st.rerun()

if st.session_state.custom_mode:
    # Custom data setup
    st.sidebar.header("Custom Data Setup")
    
    # CSV Upload for SQL Tool
    csv_file = st.sidebar.file_uploader("Upload CSV Data", type="csv")
    if csv_file and not st.session_state.custom_sql_tool:
        df = pd.read_csv(csv_file)
        st.sidebar.write("Preview of uploaded data:")
        st.sidebar.write(df.head())
        st.session_state.custom_sql_tool = create_custom_sql_tool(df)
    
    # PDF Upload for LlamaIndex
    pdf_files = st.sidebar.file_uploader("Upload PDF Documents", type="pdf", accept_multiple_files=True)
    if pdf_files and not st.session_state.custom_llama_tool:
        st.sidebar.write(f"Uploaded {len(pdf_files)} PDF files")
        index = load_pdfs(pdf_files)
        st.session_state.custom_llama_tool = create_llama_tool(index)

    # Display current tools status
    st.sidebar.write("Tools Status:")
    st.sidebar.write(f"- Custom SQL Tool: {'✓' if st.session_state.custom_sql_tool else '✗'}")
    st.sidebar.write(f"- Custom LlamaIndex Tool: {'✓' if st.session_state.custom_llama_tool else '✗'}")

    # Reset custom tools button
    if st.sidebar.button("Reset Custom Tools"):
        st.session_state.custom_sql_tool = None
        st.session_state.custom_llama_tool = None
        st.rerun()

    # Only show query interface if both tools are ready
    if st.session_state.custom_sql_tool and st.session_state.custom_llama_tool:
        sql_tool = st.session_state.custom_sql_tool
        llama_tool = st.session_state.custom_llama_tool
    else:
        st.warning("Please upload both CSV and PDF files to proceed.")
        st.stop()
else:
    # Display default interface
    st.header("Available Cities")
    st.write(", ".join(cities))
    sql_tool = default_sql_tool
    llama_tool = llama_cloud_tool

# Display sample queries
st.header("Sample Queries")
sample_queries = [
    "Which city has the highest population?",
    "List all places to visit in Miami.",
    "How do people in Chicago get around?",
    "What is the historical name of Los Angeles?"
]
st.write("\n".join(f"- {query}" for query in sample_queries))

# User input
user_query = st.text_input("Enter your query:")

async def get_response(query):
    try:
        wf = RouterOutputAgentWorkflow(tools=[sql_tool, llama_tool], verbose=True, timeout=120)
        response = await wf.run(message=query)
        return response
    except Exception as e:
        return f"Error processing query: {str(e)}"

if st.button("Get Answer"):
    if user_query:
        with st.spinner("Processing your query..."):
            try:
                import nest_asyncio
                nest_asyncio.apply()
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(get_response(user_query))
                loop.close()
                
                if isinstance(result, str) and result.startswith("Error"):
                    st.error(result)
                else:
                    st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a query.")