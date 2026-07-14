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
    st.metric("Total Repairs", len(df))

    # ====== SEARCH + FILTER SECTION ======
    col1, col2 = st.columns(2)

    with col1:
        search_term = st.text_input("🔍 Search repairs", placeholder="Type device or customer")

    with col2:
        devices = ["All"] + sorted(df['device'].unique().tolist())
        device_filter = st.selectbox("Filter by Device", devices)

    # Apply filters
    filtered_df = df.copy()

    if search_term:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]

    if device_filter != "All":
        filtered_df = filtered_df[filtered_df['device'] == device_filter]

    st.dataframe(filtered_df, use_container_width=True)

conn.close()
