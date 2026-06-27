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

# ===== LAYER 2: DATABASE = CHAT HISTORY =====
conn = sqlite3.connect('itech_ai.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (id INTEGER PRIMARY KEY, timestamp, device, country, voltage, problem, answer, rating)''')
conn.commit()

# ===== LAYER 3: GLOBAL DATA = 195 COUNTRIES + 55 APPLIANCES =====

# 1. ALL 195 COUNTRIES + STANDARD VOLTAGE MAP
COUNTRIES_VOLTAGE = {
    "Afghanistan": "220V", "Albania": "230V", "Algeria": "230V", "Andorra": "230V", "Angola": "220V", "Antigua and Barbuda": "230V", "Argentina": "220V", "Armenia": "230V", "Australia": "230V", "Austria": "230V",
    "Azerbaijan": "220V", "Bahamas": "120V", "Bahrain": "230V", "Bangladesh": "220V", "Barbados": "115V", "Belarus": "220V", "Belgium": "230V", "Belize": "120V", "Benin": "220V", "Bhutan": "230V",
    "Bolivia": "220V", "Bosnia and Herzegovina": "230V", "Botswana": "230V", "Brazil": "127V/220V", "Brunei": "230V", "Bulgaria": "230V", "Burkina Faso": "220V", "Burundi": "220V", "Cabo Verde": "220V", "Cambodia": "230V",
    "Cameroon": "220V", "Canada": "120V", "Central African Republic": "220V", "Chad": "220V", "Chile": "220V", "China": "220V", "Colombia": "110V", "Comoros": "220V", "Congo": "220V", "Costa Rica": "120V",
    "Croatia": "230V", "Cuba": "110V", "Cyprus": "230V", "Czech Republic": "230V", "Denmark": "230V", "Djibouti": "220V", "Dominica": "230V", "Dominican Republic": "110V", "Ecuador": "120V", "Egypt": "220V",
    "El Salvador": "115V", "Equatorial Guinea": "220V", "Eritrea": "230V", "Estonia": "230V", "Eswatini": "230V", "Ethiopia": "220V", "Fiji": "240V", "Finland": "230V", "France": "230V", "Gabon": "220V",
    "Gambia": "230V", "Georgia": "220V", "Germany": "230V", "Ghana": "230V", "Greece": "230V", "Grenada": "230V", "Guatemala": "120V", "Guinea": "220V", "Guinea-Bissau": "220V", "Guyana": "240V",
    "Haiti": "110V", "Honduras": "120V", "Hungary": "230V", "Iceland": "230V", "India": "230V", "Indonesia": "230V", "Iran": "220V", "Iraq": "230V", "Ireland": "230V", "Israel": "230V",
    "Italy": "230V", "Jamaica": "110V", "Japan": "100V", "Jordan": "230V", "Kazakhstan": "220V", "Kenya": "240V", "Kiribati": "240V", "Kuwait": "240V", "Kyrgyzstan": "220V", "Laos": "230V",
    "Latvia": "230V", "Lebanon": "220V", "Lesotho": "220V", "Liberia": "120V", "Libya": "230V", "Liechtenstein": "230V", "Lithuania": "230V", "Luxembourg": "230V", "Madagascar": "220V", "Malawi": "230V",
    "Malaysia": "240V", "Maldives": "230V", "Mali": "220V", "Malta": "230V", "Marshall Islands": "120V", "Mauritania": "220V", "Mauritius": "230V", "Mexico": "127V", "Micronesia": "120V", "Moldova": "230V",
    "Monaco": "230V", "Mongolia": "220V", "Montenegro": "230V", "Morocco": "220V", "Mozambique": "220V", "Myanmar": "230V", "Namibia": "220V", "Nauru": "240V", "Nepal": "230V", "Netherlands": "230V",
    "New Zealand": "230V", "Nicaragua": "120V", "Niger": "220V", "Nigeria": "220V", "North Korea": "220V", "North Macedonia": "230V", "Norway": "230V", "Oman": "240V", "Pakistan": "230V", "Palau": "120V",
    "Palestine": "230V", "Panama": "110V", "Papua New Guinea": "240V", "Paraguay": "220V", "Peru": "220V", "Philippines": "220V", "Poland": "230V", "Portugal": "230V", "Qatar": "240V", "Romania": "230V",
    "Russia": "220V", "Rwanda": "230V", "Saint Kitts and Nevis": "230V", "Saint Lucia": "240V", "Saint Vincent and the Grenadines": "230V", "Samoa": "230V", "San Marino": "230V", "Sao Tome and Principe": "220V", "Saudi Arabia": "220V", "Senegal": "230V",
    "Serbia": "230V", "Seychelles": "240V", "Sierra Leone": "230V", "Singapore": "230V", "Slovakia": "230V", "Slovenia": "230V", "Solomon Islands": "240V", "Somalia": "220V", "South Africa": "230V", "South Korea": "220V",
    "South Sudan": "220V", "Spain": "230V", "Sri Lanka": "230V", "Sudan": "230V", "Suriname": "127V", "Sweden": "230V", "Switzerland": "230V", "Syria": "220V", "Taiwan": "110V", "Tajikistan": "220V",
    "Tanzania": "230V", "Thailand": "220V", "Timor-Leste": "220V", "Togo": "220V", "Tonga": "240V", "Trinidad and Tobago": "115V", "Tunisia": "230V", "Turkey": "230V", "Turkmenistan": "220V", "Tuvalu": "240V",
    "Uganda": "240V", "Ukraine": "220V", "United Arab Emirates": "230V", "United Kingdom": "230V", "United States": "120V", "Uruguay": "220V", "Uzbekistan": "220V", "Vanuatu": "240V", "Vatican City": "230V", "Venezuela": "120V",
    "Vietnam": "220V", "Yemen": "220V", "Zambia": "230V", "Zimbabwe": "230V", "Other": "220V"
}

# 2. ALL HOME + ELECTRONICS APPLIANCES LIST
ALL_APPLIANCES = [
    # HOME APPLIANCES
    "Air Conditioner AC", "Refrigerator", "Freezer", "Washing Machine", "Dryer", 
    "Dishwasher", "Microwave Oven", "Electric Oven", "Gas Cooker", "Induction Cooker",
    "Electric Kettle", "Blender", "Mixer", "Juicer", "Toaster", "Rice Cooker", 
    "Air Fryer", "Water Dispenser", "Water Heater Geyser", "Vacuum Cleaner", 
    "Iron", "Steamer", "Fan Ceiling", "Fan Standing", "Air Purifier", "Humidifier",
    # COOLING/HEATING
    "Deep Freezer", "Chest Freezer", "Wine Cooler", "Ice Maker", "Heater",
    # ELECTRONICS + ENTERTAINMENT 
    "Television TV LED", "Television TV OLED", "Decoder DSTV", "Decoder GOTV", 
    "Sound System", "Amplifier", "Speaker", "Home Theatre", "Projector",
    "PlayStation PS5", "PlayStation PS4", "Xbox", "Nintendo", "DVD Player",
    # POWER + SOLAR
    "Solar Inverter", "Solar Charge Controller", "Solar Battery", "UPS", 
    "Generator", "Stabilizer", "Voltage Regulator", "Power Bank",
    # PHONES + COMPUTERS
    "Laptop", "Desktop PC", "Monitor", "Printer", "Router Wifi", "Phone Charger",
    # OTHER ELECTRONICS
    "Electric Drill", "Welding Machine", "Pressure Cooker", "Sewing Machine",
    "Hair Dryer", "Clippers", "Electric Fence", "CCTV Camera", "Other"
]

# ===== LAYER 4: UI HEADER =====
st.title("🔧 Itech AI - Global Electronics Repair Assistant")
st.caption("World-class AI diagnostics for ALL Electronics & Home Appliances")

st.warning("⚠️ Disclaimer: Itech AI provides troubleshooting guidance only. For electrical, gas, or refrigerant work, contact a licensed technician. Use at your own risk.", icon="⚠️")

# ===== #25 PANIC MODE BUTTON =====
col1, col2 = st.columns([3,1])
with col2:
    panic = st.button("🚨 PANIC MODE", type="primary", use_container_width=True, help="Device sparking, smoking, leaking NOW")

# ===== INPUTS: DEVICE + COUNTRY/VOLTAGE [ALL SEARCHABLE] =====
col1, col2, col3 = st.columns(3)
with col1:
    device = st.selectbox("1. Select Device 🔧", options=ALL_APPLIANCES, index=None, placeholder="Type to search: TV, Microwave...")
with col2:
    country = st.selectbox("2. Select Country 🌍", options=list(COUNTRIES_VOLTAGE.keys()), index=list(COUNTRIES_VOLTAGE.keys()).index("Nigeria"), placeholder="Type country name...")
with col3:
    voltage = st.selectbox("3. Voltage", options=[COUNTRIES_VOLTAGE[country]], disabled=True, help=f"Auto-set to {COUNTRIES_VOLTAGE[country]} for {country}")

# ===== PROBLEM INPUT =====
user_input = st.text_area("4. Describe your appliance issue. Any language:", placeholder="e.g. AC not cooling, Fridge making noise...")

# ===== AI BRAIN FUNCTION =====
def get_ai_diagnosis(problem, device, country, voltage, panic=False):
    if panic:
        return "🚨 EMERGENCY 3-STEPS:\n1. UNPLUG DEVICE NOW FROM WALL.\n2. If water/gas/smoke: LEAVE AREA. CALL LICENSED TECH/EMERGENCY.\n3. Do NOT touch wet parts or open panels."

    system_prompt = f"""
    You are ITECH AI, a world-class expert technician for ALL electronics and home appliances.
    Country: {country}. Voltage: {voltage}. Device: {device}.
    RULE 1: First line MUST be: 'SAFETY: UNPLUG DEVICE FIRST. Keep hands dry.'
    RULE 2: If electrical/gas/refrigerant: End with 'Call licensed technician.'
    RULE 3: Give only 3 steps max. Be simple, practical.
    RULE 4: At end add local cost estimate for {country} using {voltage}.
    RULE 5: Reply in the SAME LANGUAGE the user wrote.
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
if st.button("Diagnose Now", type="primary", use_container_width=True) and user_input and device:
    with st.spinner("Thinking like a master tech..."):
        answer = get_ai_diagnosis(user_input, device, country, voltage, panic)

        st.success("Diagnosis Complete:")
        st.write(answer)

        # ===== RATING + SHARE =====
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            st.button("👍 Helpful")
        with col2:
            st.button("👎 Not Helpful")
        with col3:
            share_text = f"AI fixed my {device}: {user_input[:30]}... Try Itech AI: https://itech-ai.streamlit.app"
            st.code(share_text, language=None)

        # ===== SAVE TO DB =====
        c.execute("INSERT INTO logs (timestamp, device, country, voltage, problem, answer) VALUES (?,?,?,?,?,?)",
                  (datetime.now(), device, country, voltage, user_input, answer))
        conn.commit()

# ===== SIDEBAR HISTORY =====
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
  total_count = c.execute('SELECT COUNT(*) FROM logs').fetchone()[0]
st.metric("Total Diagnoses", total_count)
