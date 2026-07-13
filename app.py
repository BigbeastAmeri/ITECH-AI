import streamlit as st

st.set_page_config(page_title="iTech AI Assistant", layout="wide")

st.title("🔧 iTech AI Assistant")
st.markdown("Welcome! Use the sidebar to navigate.")

st.sidebar.success("Select a page above")

st.markdown("""
### What you can do:
- **Diagnose**: AI diagnosis for devices
- **History**: View all past repairs  
- **Settings**: Add your API Key

Make sure to add your OpenAI API Key in Settings first.
""")
