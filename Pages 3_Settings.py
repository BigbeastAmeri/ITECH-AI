import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

st.title("⚙️ Settings")
st.markdown("Configure your iTech AI Assistant")

st.subheader("OpenAI API Key")
api_key = st.text_input("Enter your OpenAI API Key", type="password")

if st.button("Save Key"):
    st.success("API Key saved for this session!")

st.divider()
st.subheader("Database")
if st.button("Reset Database"):
    st.warning("This will delete all repair history")
