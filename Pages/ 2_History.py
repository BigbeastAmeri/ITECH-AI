import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Repair History", layout="wide")

st.title("📜 Repair History")
st.markdown("View all past diagnoses and repairs")

conn = sqlite3.connect("repairs.db", check_same_thread=False)
df = pd.read_sql("SELECT * FROM repairs ORDER BY timestamp DESC", conn)

if df.empty:
    st.info("No repairs logged yet. Go to Diagnose page to add one.")
else:
    st.dataframe(df, use_container_width=True)
    st.metric("Total Repairs", len(df))

conn.close()
