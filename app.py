import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("AC Troubleshooter")
user_input = st.text_input("Describe your AC problem:")

if user_input:
    with st.spinner("Diagnosing..."):

        # RULES FOR THE AI - THIS IS FIRST PRIORITY
        rules = """You are an AC, Fridge, and TV repair technician only.

1. PRIORITY 1: First line must always be: "⚠️ SAFETY: UNPLUG FIRST from power socket before touching anything."
2. You ONLY answer AC, Fridge, or TV repair questions.
3. If user asks anything else like JAMB, school, relationship, etc, reply exactly: "I'm sorry, I'm an AC technician only."
4. Give diagnosis + 3 simple fix steps. Use simple English."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": rules},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        st.write(response.choices[0].message.content)
