import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("AC Troubleshooter")
user_input = st.text_input("Describe your AC problem:")

if user_input:
    with st.spinner("Diagnosing..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"You are an AC repair expert. User says: {user_input}. Give diagnosis and fix."}]
        )
        st.write(response.choices[0].message.content)
