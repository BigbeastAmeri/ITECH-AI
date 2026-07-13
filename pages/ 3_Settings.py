import streamlit as st

st.title("⚙️ Settings")
st.write("Configure your iTech AI Assistant")

# ===== API KEY SECTION =====
st.header("OpenAI API Key")
api_key = st.text_input("Enter your OpenAI API Key", type="password")
if st.button("Save Key"):
    st.success("Key saved!")

st.divider()

# ===== NEW SETTINGS SECTION =====
st.header("Privacy & Security")
col1, col2 = st.columns(2)
with col1:
    st.toggle("Save chat history", value=True)
with col2:
    st.toggle("Share anonymous data", value=False)

st.header("Appearance")
theme = st.selectbox("Theme", ["Dark", "Light", "System"])
language = st.selectbox("Language", ["English", "Spanish", "French"])

st.header("Notifications")
st.toggle("Email notifications", value=True)
st.toggle("Desktop alerts", value=False)

st.divider()

# ===== DATABASE SECTION =====
st.header("Database")
if st.button("Reset Database", type="secondary"):
    st.warning("This will delete all data!")
