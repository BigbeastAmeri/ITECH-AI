import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Itech AI", page_icon="🔧", layout="wide")

st.title("Itech AI - Electronics Repair Assistant")
st.caption("USA-based AI diagnostics for HVAC, Refrigeration, TVs & Home Appliances")
st.markdown("**⚠️ Disclaimer:** Itech AI provides troubleshooting guidance only. For electrical, gas, or refrigerant work, contact a licensed technician in your state. Use at your own risk.")
st.divider()

user_input = st.text_input("Describe your appliance issue", key="input_box")
zip_code = st.text_input("Enter your US ZIP code for local technician referrals: E.g. 90210", max_chars=5, key="zip_box")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    send_btn = st.button("🔧 Diagnose My Appliance", type="primary", use_container_width=True)

if send_btn and user_input:
    with st.spinner("Itech AI is diagnosing... 🔧"):
        prompt = f"""
You are Itech AI, a USA-based certified appliance technician.
Customer location: ZIP {zip_code if zip_code else 'Not provided'}

RULES:
1. Safety first: Always start with 'UNPLUG the appliance before inspection'
2. Only diagnose electronics: HVAC, Refrigeration, TVs, Washing Machines
3. Give 3 clear troubleshooting steps in plain English
4. End with: 'If this doesn't work, contact a licensed HVAC technician in ZIP {zip_code if zip_code else 'your area'}'

Customer problem: {user_input}
"""

        # TEST MODE - USA Standard
        st.write("**Itech AI Prompt:**")
        st.code(prompt)
        st.success("✅ Prompt built correctly! Add API key next for real diagnosis")

        # TODO: Uncomment below after adding API key
        # response = client.chat.completions.create(
        # model="gpt-4o-mini",
        # messages=[
        # {"role": "system", "content": prompt},
        # {"role": "user", "content": user_input}
        # ],
        # temperature=0.3
        # )
        # st.write(response.choices[0].message.content)
