import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Repair History", layout="wide")

st.title("📜 Repair History")
st.markdown("View all past diagnoses and repairs")

# Create database and table if they don't exist
conn = sqlite3.connect("itechai.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS repairs
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              timestamp TEXT, 
              issue TEXT, 
              solution TEXT)''')
conn.commit()
df = pd.read_sql("SELECT * FROM repairs ORDER BY timestamp DESC", conn)

if df.empty:
    st.info("No repairs logged yet. Go to Diagnose page to add one.")
else:
    st.dataframe(df, use_container_width=True)
    st.metric("Total Repairs", len(df))

conn.close()
