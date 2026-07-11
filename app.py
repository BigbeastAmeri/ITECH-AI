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
             (id INTEGER PRIMARY KEY, timestamp TEXT, device TEXT, country TEXT, voltage TEXT, problem TEXT, answer TEXT, rating TEXT)''')
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

# 2. ALL 195 COUNTRIES LOCAL DATA: CURRENCY + PARTS + COMMON ISSUE
COUNTRY_LOCAL_DATA = {
    "Afghanistan": {"currency": "Af", "parts": "Local bazaars, Kabul Electronics", "common_issue": "Power outages"},
    "Albania": {"currency": "Lek", "parts": "Altex, Nepton", "common_issue": "230V standard"},
    "Algeria": {"currency": "DZD", "parts": "Local markets, Jumia.dz", "common_issue": "Voltage fluctuation"},
    "Angola": {"currency": "Kz", "parts": "Shoprite, Jumia.ao", "common_issue": "Power cuts"},
    "Argentina": {"currency": "$", "parts": "Mercado Libre, Frávega", "common_issue": "220V standard"},
    "Australia": {"currency": "A$", "parts": "JB Hi-Fi, Harvey Norman", "common_issue": "230V standard"},
    "Austria": {"currency": "€", "parts": "MediaMarkt, Amazon.de", "common_issue": "230V EU standard"},
    "Bangladesh": {"currency": "৳", "parts": "Bashundhara City, Daraz.com.bd", "common_issue": "Loadshedding"},
    "Belgium": {"currency": "€", "parts": "Fnac, Coolblue", "common_issue": "230V standard"},
    "Brazil": {"currency": "R$", "parts": "Mercado Livre, Magazine Luiza", "common_issue": "127V/220V confusion"},
    "Canada": {"currency": "$", "parts": "Home Depot, Canadian Tire, Amazon.ca", "common_issue": "110V, Cold weather"},
    "China": {"currency": "¥", "parts": "JD.com, Tmall", "common_issue": "220V standard"},
    "Egypt": {"currency": "E£", "parts": "B.Tech, Jumia.eg", "common_issue": "Power cuts"},
    "France": {"currency": "€", "parts": "Darty, Boulanger", "common_issue": "230V standard"},
    "Germany": {"currency": "€", "parts": "MediaMarkt, Saturn, Amazon.de", "common_issue": "230V EU standards"},
    "Ghana": {"currency": "₵", "parts": "Circle Market Accra, Jumia.com.gh", "common_issue": "Dumsor power cuts"},
    "India": {"currency": "₹", "parts": "Croma, Reliance Digital, Amazon.in", "common_issue": "Power cuts, 230V"},
    "Indonesia": {"currency": "Rp", "parts": "Tokopedia, Bukalapak", "common_issue": "230V standard"},
    "Italy": {"currency": "€", "parts": "Euronics, MediaWorld", "common_issue": "230V standard"},
    "Japan": {"currency": "¥", "parts": "Yodobashi, Bic Camera", "common_issue": "100V low voltage"},
    "Kenya": {"currency": "KSh", "parts": "Jumia.co.ke, Hotpoint", "common_issue": "Power outages"},
    "Malaysia": {"currency": "RM", "parts": "Lazada, Shopee", "common_issue": "240V standard"},
    "Mexico": {"currency": "$", "parts": "Home Depot, Liverpool", "common_issue": "127V standard"},
    "Nigeria": {"currency": "₦", "parts": "Alaba International Market, Jumia.ng, Konga", "common_issue": "NEPA power surge, voltage fluctuation"},
    "Pakistan": {"currency": "₨", "parts": "Daraz.pk, Hall Road Lahore", "common_issue": "Loadshedding"},
    "Philippines": {"currency": "₱", "parts": "Lazada, Shopee, Abenson", "common_issue": "220V standard"},
    "Russia": {"currency": "₽", "parts": "M.Video, DNS", "common_issue": "220V standard"},
    "Saudi Arabia": {"currency": "SAR", "parts": "Extra, Amazon.sa", "common_issue": "Heat and dust"},
    "South Africa": {"currency": "R", "parts": "Takealot, Builders Warehouse", "common_issue": "Loadshedding"},
    "South Korea": {"currency": "₩", "parts": "Coupang, Gmarket", "common_issue": "220V standard"},
    "Spain": {"currency": "€", "parts": "MediaMarkt, El Corte Ingles", "common_issue": "230V standard"},
    "Turkey": {"currency": "₺", "parts": "Trendyol, Vatan", "common_issue": "230V standard"},
    "United Arab Emirates": {"currency": "AED", "parts": "Carrefour, Amazon.ae, Sharaf DG", "common_issue": "Heat and dust"},
    "United Kingdom": {"currency": "£", "parts": "Currys, Screwfix, Amazon.co.uk", "common_issue": "3-pin plug, 230V"},
    "United States": {"currency": "$", "parts": "Home Depot, Lowe's, Amazon.com", "common_issue": "Warranty claims, 110V"},
    "Vietnam": {"currency": "₫", "parts": "Tiki, Dien May Xanh", "common_issue": "220V standard"},
    "default": {"currency": "$", "parts": "Local appliance stores, Amazon", "common_issue": "Standard voltage issues"}
}

# 3. ALL HOME + ELECTRONICS APPLIANCES LIST
ALL_APPLIANCES = [
    "Air Conditioner AC", "Refrigerator", "Freezer", "Washing Machine", "Dryer",
    "Dishwasher", "Microwave Oven", "Electric Oven", "Gas Cooker", "Induction Cooker",
    "Electric Kettle", "Blender", "Mixer", "Juicer", "Toaster", "Rice Cooker",
    "Air Fryer", "Water Dispenser", "Water Heater Geyser", "Vacuum Cleaner",
    "Iron", "Steamer", "Fan Ceiling", "Fan Standing", "Air Purifier", "Humidifier",
    "Deep Freezer", "Chest Freezer", "Wine Cooler", "Ice Maker", "Heater",
    "Television TV LED", "Television TV OLED", "Decoder DSTV", "Decoder GOTV",
    "Sound System", "Amplifier", "Speaker", "Home Theatre", "Projector",
    "PlayStation PS5", "PlayStation PS4", "Xbox", "Nintendo", "DVD Player",
    "Solar Inverter", "Solar Charge Controller", "Solar Battery", "UPS",
    "Generator", "Stabilizer", "Voltage Regulator", "Power Bank",
    "Laptop", "Desktop PC", "Monitor", "Printer", "Router Wifi", "Phone Charger",
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

# ===== AI BRAIN FUNCTION - NOW COUNTRY SMART =====
def get_ai_diagnosis(problem, device, country, voltage, panic=False):
    if panic:
        return "🚨 EMERGENCY 3-STEPS:\n1. UNPLUG DEVICE NOW FROM WALL.\n2. If water/gas/smoke: LEAVE AREA. CALL LICENSED TECH/EMERGENCY.\n3. Do NOT touch wet parts or open panels."

    local = COUNTRY_LOCAL_DATA.get(country, COUNTRY_LOCAL_DATA["default"])

    system_prompt = f"""
    You are ITECH AI, a world-class expert technician for {country}.

    CRITICAL CONTEXT FOR {country}:
    - Voltage: {voltage}
    - Currency: Use {local['currency']} for all prices
    - Where to buy parts: {local['parts']}
    - Most common problem in {country}: {local['common_issue']}
    - Device: {device}

    RULE 1: First line MUST be: 'SAFETY: UNPLUG DEVICE FIRST. Keep hands dry.'
    RULE 2: Give EXACTLY 3 troubleshooting steps that make sense for {country}
    RULE 3: Mention {local['parts']} when suggesting where to buy parts
    RULE 4: Give price estimate in {local['currency']} for {country}
    RULE 5: If electrical/gas/refrigerant: End with 'Call licensed technician in {country}.'
    RULE 6: Reply in the SAME LANGUAGE the user wrote.
    RULE 7: Be practical. Reference {local['common_issue']} if relevant.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{device} issue in {country}: {problem}"}
        ],
        temperature=0.3,
        max_tokens=350
    )
    return response.choices[0].message.content

# ===== DIAGNOSE BUTTON WITH VALIDATION =====
if st.button("Diagnose Now", type="primary", use_container_width=True):
    # VALIDATION: STOP IF EMPTY
    if not device:
        st.error("❌ Please select a Device first")
    elif not user_input.strip():
        st.error("❌ Please describe your appliance issue")
    else:
        with st.spinner("Thinking like a master tech..."):
            answer = get_ai_diagnosis(user_input, device, country, voltage, panic)

            st.success("Diagnosis Complete:")
            st.write(answer)

            # ===== NEW: FIND TECHNICIAN NEAR ME =====
            st.divider()
            st.subheader("👨‍🔧 Need a Professional?")

            st.info(f"**For {device} repair in {country}**")

            # Create Google Maps search link
            search_query = f"appliance+repair+technician+near+me+{country}"
            maps_link = f"https://www.google.com/maps/search/{search_query}"

            # Create Google Search link
            google_link = f"https://www.google.com/search?q=appliance repair technician near me {country}"

            col1, col2 = st.columns(2)
            with col1:
                st.link_button("📍 Find on Google Maps", maps_link, use_container_width=True)
            with col2:
                st.link_button("🔍 Search on Google", google_link, use_container_width=True)

            st.caption("Tip: Click 'Near Me' and Google will show technicians closest to you with ratings + phone")
            # ===== END NEW CODE =====

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
                      (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), device, country, voltage, user_input, answer))
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
