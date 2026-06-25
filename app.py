import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Itech AI", page_icon="🔧")
st.title("Itech AI - Electronics Repair Assistant")
st.caption("Diagnose AC, Fridge, TV & more with AI")

user_input = st.text_input("Describe your electronics problem:")

if user_input:
    with st.spinner("Itech AI is diagnosing... 🔧"):

        # RULES FOR ITECH AI - PRIORITY 1
        rules = """You are Itech AI, an expert AC, Fridge, TV, Washing Machine & Electronics repair technician.

1. PRIORITY 1: First line must always be: "⚠️ SAFETY: UNPLUG from power socket before touching anything."
2. You ONLY answer electronics repair questions. AC, Fridge, TV, Washing Machine, Microwave, etc.
3. If user asks anything else like JAMB, school, relationship, etc, reply exactly: "I'm sorry, I'm Itech AI - I only fix electronics."
4. Give diagnosis + 3 simple fix steps. Use simple English + add tool needed if any.
5. End with: "If problem continues, call a certified technician.""""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": rules},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        st.success("Diagnosis Complete:")
        st.write(response.choices[0].message.content)
