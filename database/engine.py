import os
from supabase import create_client
from langchain_community.utilities import SQLDatabase
from supabase import create_client
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

# Load environment variables from .env
load_dotenv()

def create_db():
    """
    Creates and returns a database connected to Supabase
    
    Returns:
        SQLDatabase: Configured database
    """
    # Supabase credentials
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
    SUPABASE_PASSWORD = os.environ["SUPABASE_PASSWORD"]

    db = SQLDatabase.from_uri(
        f"postgresql://postgres.dopksmclclpxfgpscmto:{SUPABASE_PASSWORD}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres",
        schema="public",
        sample_rows_in_table_info=2
    )

    return db

def create_sqlalchemy_db():
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
    SUPABASE_PASSWORD = os.environ["SUPABASE_PASSWORD"]
    return create_engine(f"postgresql://postgres.dopksmclclpxfgpscmto:{SUPABASE_PASSWORD}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres")

def create_psycopg2_connection():
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
    SUPABASE_PASSWORD = os.environ["SUPABASE_PASSWORD"]
    return psycopg2.connect(f"postgresql://postgres.dopksmclclpxfgpscmto:{SUPABASE_PASSWORD}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres")

def create_supabase_client():
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def create_all_clients():
    return create_db(), create_sqlalchemy_db(), create_psycopg2_connection(), create_supabase_client()

import psycopg2
from pprint import pprint

def get_table_desc(table_name, db_psycopg2):
    # Connect to your PostgreSQL database
    cur = db_psycopg2.cursor()

    # Query to get the table description
    cur.execute(f"""
    SELECT d.description
    FROM pg_catalog.pg_description d
    JOIN pg_catalog.pg_class c ON d.objoid = c.oid
    WHERE c.relname = '{table_name}';
    """)
    description = cur.fetchone()

    # Query to get column definitions and their descriptions
    cur.execute(f"""
        SELECT 
            c.column_name, 
            c.data_type, 
            c.is_nullable, 
            c.column_default, 
            d.description
        FROM information_schema.columns c
        LEFT JOIN pg_catalog.pg_class cl ON cl.relname = '{table_name}' AND cl.relkind IN ('r', 'v')
        LEFT JOIN pg_catalog.pg_attribute a ON a.attrelid = cl.oid AND a.attname = c.column_name
        LEFT JOIN pg_catalog.pg_description d ON d.objoid = cl.oid AND d.objsubid = a.attnum
        WHERE c.table_name = '{table_name}';
    """)
    columns = cur.fetchall()


    # Query to get primary and foreign key constraints
    cur.execute(f"""
    SELECT conname, contype, pg_catalog.pg_get_constraintdef(oid) 
    FROM pg_catalog.pg_constraint 
    WHERE conrelid = '{table_name}'::regclass;
    """)
    constraints = cur.fetchall()

    # Query to get example rows
    cur.execute(f"SELECT * FROM {table_name} LIMIT 2;")
    example_rows = cur.fetchall()

    # Build the result string
    result = []
    result.append(f"Table Name: {table_name}")
    result.append(f"Description: {description[0] if description else '-'}")
    
    result.append("\nColumns:")
    for i, column in enumerate(columns):
        result.append(f"Name: {column[0]}, Type: {column[1]}, Nullable: {column[2]}, Default: {column[3]}, Description: {column[4] if column[4] else '-'}")

    result.append("\nConstraints:")
    for constraint in constraints:
        result.append(f"Name: {constraint[0]}, Type: {constraint[1]}, Definition: {constraint[2]}")

    result.append("\nExample Rows:")
    for row in example_rows:
        result.append(str(row))
        
    return "\n".join(result)
