import streamlit as st
import google.generativeai as genai

st.title("AC Troubleshooter")
st.write("Ask me anything about your AC problem 👇")

# Get key from Secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Text box for user
user_input = st.text_input("What's wrong with your AC?")

if st.button("Get Answer"):
    if user_input:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"You are an AC repair expert. User says: {user_input}. Give 3 simple troubleshooting steps.")
        st.write(response.text)
    else:
        st.warning("Please type your AC problem first")
