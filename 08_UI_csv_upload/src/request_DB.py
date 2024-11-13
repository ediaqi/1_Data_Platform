import os
import psycopg2
import streamlit as st

# Define your connection parameters
database = os.environ['DATABASE']
user = os.environ['DB_USER']
host= os.environ['DB_HOST']
port = os.environ['DB_PORT']
password = os.environ['DB_PASSWORD']

# @st.cache_data
def retrieve_data(query):
    conn_params = {
        'dbname': database,
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }

    # Establish the connection
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()        

        # Execute the query
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchall()

        return result

    except Exception as e:
        st.write(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return None
