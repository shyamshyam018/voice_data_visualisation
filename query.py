import mysql.connector
import streamlit as st
from langchain import SQLDatabaseChain

# Establish MySQL database connection
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",  # Provide your database password here
    db="mydb"
)

# Create a cursor
c = conn.cursor()

# Streamlit app
def view_all_data():
    c.execute('SELECT * FROM insurance ORDER BY id ASC')
    data = c.fetchall()
    return data

# Streamlit UI
st.title("View All Data")
data = view_all_data()
st.write(data)

# Close the database connection when done
conn.close()
