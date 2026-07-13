import streamlit as st

st.set_page_config(
    page_title="iTech AI Assistant", 
    page_icon="🔧",
    layout="centered"
)

st.title("🔧 iTech AI Assistant")
st.subheader("Your 24/7 AI Repair Expert")

st.write("Got a problem with your phone, TV, fridge, or laptop? 
Just describe it and get instant diagnosis + repair steps.")

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
