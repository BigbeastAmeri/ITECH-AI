import streamlit as st

st.set_page_config(
    page_title="iTECH AI",
    page_icon="logo.png",
    layout="wide"
)

# HEADER WITH LOGO
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=70)
with col2:
    st.title("iTECH AI")
    st.caption("Smart Repair Management System")
st.divider()

# YOUR OLD CODE CONTINUES BELOW
col1, col2 = st.columns(2)

st.write("Got a problem with any electronic device? Just describe it and get instant diagnosis + repair steps.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Instant Diagnosis")
    st.write("Tell us your device problem in plain English")

with col2:
    st.markdown("### 📋 Repair History") 
    st.write("Track all your past repairs in one place")

st.divider()

st.info("👈 **Get Started**: Click 'Diagnose' in the sidebar to describe your problem")

st.caption("Powered by AI • Built for iTech Repairs")
