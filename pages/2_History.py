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
st.divider()
st.subheader("⚙️ Manage Repairs")

if not filtered_df.empty:
    repair_id = st.selectbox("Select Repair ID to Edit/Delete", filtered_df['id'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✏️ Edit Selected"):
            st.session_state['edit_id'] = repair_id
    
    with col2:
        if st.button("🗑️ Delete Selected"):
            c.execute("DELETE FROM repairs WHERE id =?", (repair_id,))
            conn.commit()
            st.success("Repair deleted!")
            st.rerun()
    
    # EDIT FORM
    if 'edit_id' in st.session_state:
        repair = filtered_df[filtered_df['id'] == st.session_state['edit_id']].iloc[0]
        with st.form("edit_form"):
            new_price = st.number_input("New Price", value=float(repair['price']))
            new_status = st.selectbox("New Status", ["Pending", "In Progress", "Done"], 
                                      index=["Pending", "In Progress", "Done"].index(repair['status']))
            if st.form_submit_button("Save Changes"):
                c.execute("UPDATE repairs SET price =?, status =? WHERE id =?", 
                          (new_price, new_status, st.session_state['edit_id']))
                conn.commit()
                del st.session_state['edit_id']
                st.success("Repair updated!")
                st.rerun()
conn.close()
