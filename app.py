import streamlit as st
import openai
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# ===== LAYER 1: SETUP =====
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Itech AI Global", page_icon="🔧", layout="wide")

# ===== LAYER 2: DATABASE = CHAT HISTORY #8 =====
conn = sqlite3.connect('itech_ai.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (id INTEGER PRIMARY KEY, timestamp, device, country, voltage, problem, answer, rating)''')
conn.commit()

# ===== LAYER 3: UI HEADER =====
st.title("🔧 Itech AI - Global Electronics Repair Assistant")
st.caption("USA-based AI diagnostics for HVAC, Refrigeration, TVs & Home Appliances")

st.warning("⚠️ Disclaimer: Itech AI provides troubleshooting guidance only. For electrical, gas, or refrigerant work, contact a licensed technician in your state. Use at your own risk.", icon="⚠️")

# ===== #25 PANIC MODE BUTTON =====
col1, col2 = st.columns([3,1])
with col2:
    panic = st.button("🚨 PANIC MODE", type="primary", use_container_width=True, help="AC leaking, sparking, smoking NOW")

# ===== #5 #6 INPUTS: DEVICE + COUNTRY/VOLTAGE =====
col1, col2, col3 = st.columns(3)
with col1:
    device = st.selectbox("1. Select Device", ["AC", "Fridge", "TV", "Washing Machine", "Microwave", "Generator", "Fan", "Laptop", "Phone"])
with col2:
    country = st.selectbox("2. Country", ["Nigeria", "USA", "UK", "India", "Brazil", "Canada", "Other"])
with col3:
    voltage_map = {"Nigeria": "220V", "USA": "110V", "UK": "240V", "India": "230V", "Brazil": "127V/220V", "Canada": "120V", "Other": "220V"}
    voltage = st.selectbox("3. Voltage", [voltage_map[country]])

# ===== #7 AUTO LANGUAGE + PROBLEM INPUT =====
user_input = st.text_area("4. Describe your appliance issue. Any language:", placeholder="e.g. AC not cooling, Fridge making noise...")

# ===== AI BRAIN FUNCTION =====
def get_ai_diagnosis(problem, device, country, voltage, panic=False):
    if panic:
        return "🚨 EMERGENCY 3-STEPS:\n1. UNPLUG DEVICE NOW FROM WALL.\n2. If water/gas/smoke: LEAVE AREA. CALL LICENSED TECH/EMERGENCY.\n3. Do NOT touch wet parts or open panels."

    #27 SAFETY + #26 COST + #7 LANGUAGE
    system_prompt = f"""
    You are a certified USA Appliance Technician.
    RULE 1 #27: First line MUST be: 'SAFETY: UNPLUG DEVICE FIRST. Keep hands dry.'
    RULE 2: If electrical/gas/refrigerant: End with 'Call licensed technician.'
    RULE 3: Give only 3 steps max. Be simple.
    RULE 4 #26: At end add: 'Est. DIY cost: $5-$50 / ₦5k-₦8k. Tech may charge $30-$150.'
    RULE 5 #7: Reply in the SAME LANGUAGE the user wrote. Country: {country}, Voltage: {voltage}, Device: {device}.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{device} issue: {problem}"}
        ],
        temperature=0.3,
        max_tokens=300
    )
    return response.choices[0].message.content

# ===== DIAGNOSE BUTTON =====
if st.button("Diagnose Now", type="primary", use_container_width=True) and user_input:
    with st.spinner("Thinking like a USA tech..."):
        answer = get_ai_diagnosis(user_input, device, country, voltage, panic)

        st.success("Diagnosis Complete:")
        st.write(answer)

        # ===== #9 RATING + #28 SHARE =====
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            st.button("👍 Helpful")
        with col2:
            st.button("👎 Not Helpful")
        with col3:
            share_text = f"AI fixed my {device}: {user_input[:30]}... Try Itech AI: https://itech-ai.streamlit.app"
            st.code(share_text, language=None)

        # ===== SAVE TO DB #8 =====
        c.execute("INSERT INTO logs (timestamp, device, country, voltage, problem, answer) VALUES (?,?,?,?,?,?)",
                  (datetime.now(), device, country, voltage, user_input, answer))
        conn.commit()

# ===== #8 SIDEBAR HISTORY =====
with st.sidebar:
    st.header("📜 Past Repairs")
    rows = c.execute("SELECT timestamp, device, problem FROM logs ORDER BY id DESC LIMIT 10").fetchall()
    if rows:
        for ts, dev, prob in rows:
            st.write(f"**{dev}** - {ts[:16]}")
            st.caption(prob[:50] + "...")
    else:
        st.write("No history yet.")
    st.divider()
    st.metric("Total Diagnoses", len(rows))
