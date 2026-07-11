import streamlit as st
import openai
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import urllib.parse

# ===== LAYER 1: SETUP + SESSION STATE =====
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="Itech AI Global", page_icon="🔧", layout="wide")

if 'dark_mode' not in st.session_state: st.session_state.dark_mode = False
if st.session_state.dark_mode:
    st.markdown("""<style>.stApp {background-color: #0e1117; color: white;} </style>""", unsafe_allow_html=True)

for key, val in {'language': "English", 'detail_level': "Simple", 'show_prices': True, 'show_panic': True, 'default_country': "Nigeria", 'show_tech_map': True}.items():
    if key not in st.session_state: st.session_state[key] = val

# ===== LAYER 2: DATABASE =====
conn = sqlite3.connect('itech_ai.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, timestamp TEXT, device TEXT, country TEXT, voltage TEXT, problem TEXT, answer TEXT)''')
conn.commit()

# ===== LAYER 3: GLOBAL DATA - 195 COUNTRIES VOLTAGE =====
COUNTRIES_VOLTAGE = {
    "Afghanistan": "220V", "Albania": "230V", "Algeria": "230V", "Andorra": "230V", "Angola": "220V", "Antigua and Barbuda": "230V", "Argentina": "220V", "Armenia": "230V", "Australia": "230V", "Austria": "230V",
    "Azerbaijan": "230V", "Bahamas": "120V", "Bahrain": "230V", "Bangladesh": "220V", "Barbados": "115V", "Belarus": "230V", "Belgium": "230V", "Belize": "110V", "Benin": "220V", "Bhutan": "230V",
    "Bolivia": "220V", "Bosnia and Herzegovina": "230V", "Botswana": "230V", "Brazil": "127V/220V", "Brunei": "230V", "Bulgaria": "230V", "Burkina Faso": "220V", "Burundi": "220V", "Cambodia": "230V", "Cameroon": "220V",
    "Canada": "120V", "Cape Verde": "230V", "Central African Republic": "220V", "Chad": "220V", "Chile": "220V", "China": "220V", "Colombia": "110V", "Comoros": "220V", "Congo": "230V", "Costa Rica": "120V",
    "Croatia": "230V", "Cuba": "110V", "Cyprus": "230V", "Czech Republic": "230V", "Denmark": "230V", "Djibouti": "220V", "Dominica": "230V", "Dominican Republic": "110V", "Ecuador": "120V", "Egypt": "220V",
    "El Salvador": "115V", "Equatorial Guinea": "220V", "Eritrea": "230V", "Estonia": "230V", "Eswatini": "230V", "Ethiopia": "220V", "Fiji": "240V", "Finland": "230V", "France": "230V", "Gabon": "220V",
    "Gambia": "230V", "Georgia": "230V", "Germany": "230V", "Ghana": "230V", "Greece": "230V", "Grenada": "230V", "Guatemala": "120V", "Guinea": "220V", "Guinea-Bissau": "220V", "Guyana": "240V",
    "Haiti": "110V", "Honduras": "110V", "Hungary": "230V", "Iceland": "230V", "India": "230V", "Indonesia": "220V", "Iran": "220V", "Iraq": "230V", "Ireland": "230V", "Israel": "230V",
    "Italy": "230V", "Jamaica": "110V", "Japan": "100V", "Jordan": "230V", "Kazakhstan": "220V", "Kenya": "240V", "Kiribati": "220V", "Kuwait": "240V", "Kyrgyzstan": "220V", "Laos": "230V",
    "Latvia": "230V", "Lebanon": "220V", "Lesotho": "220V", "Liberia": "120V", "Libya": "230V", "Liechtenstein": "230V", "Lithuania": "230V", "Luxembourg": "230V", "Madagascar": "220V", "Malawi": "230V",
    "Malaysia": "240V", "Maldives": "230V", "Mali": "220V", "Malta": "230V", "Marshall Islands": "120V", "Mauritania": "220V", "Mauritius": "230V", "Mexico": "127V", "Micronesia": "120V", "Moldova": "230V",
    "Monaco": "230V", "Mongolia": "220V", "Montenegro": "230V", "Morocco": "220V", "Mozambique": "220V", "Myanmar": "230V", "Namibia": "220V", "Nauru": "240V", "Nepal": "230V", "Netherlands": "230V",
    "New Zealand": "230V", "Nicaragua": "120V", "Niger": "220V", "Nigeria": "220V", "North Korea": "220V", "North Macedonia": "230V", "Norway": "230V", "Oman": "240V", "Pakistan": "230V", "Palau": "120V",
    "Palestine": "230V", "Panama": "120V", "Papua New Guinea": "240V", "Paraguay": "220V", "Peru": "220V", "Philippines": "220V", "Poland": "230V", "Portugal": "230V", "Qatar": "240V", "Romania": "230V",
    "Russia": "220V", "Rwanda": "230V", "Saint Kitts and Nevis": "230V", "Saint Lucia": "240V", "Saint Vincent and the Grenadines": "230V", "Samoa": "220V", "San Marino": "230V", "Sao Tome and Principe": "220V", "Saudi Arabia": "220V", "Senegal": "230V",
    "Serbia": "230V", "Seychelles": "240V", "Sierra Leone": "230V", "Singapore": "230V", "Slovakia": "230V", "Slovenia": "230V", "Solomon Islands": "240V", "Somalia": "220V", "South Africa": "230V", "South Korea": "220V",
    "South Sudan": "220V", "Spain": "230V", "Sri Lanka": "230V", "Sudan": "230V", "Suriname": "127V", "Sweden": "230V", "Switzerland": "230V", "Syria": "220V", "Taiwan": "110V", "Tajikistan": "220V",
    "Tanzania": "230V", "Thailand": "220V", "Timor-Leste": "220V", "Togo": "220V", "Tonga": "240V", "Trinidad and Tobago": "115V", "Tunisia": "230V", "Turkey": "230V", "Turkmenistan": "220V", "Tuvalu": "240V",
    "Uganda": "240V", "Ukraine": "230V", "United Arab Emirates": "230V", "United Kingdom": "230V", "United States": "120V", "Uruguay": "230V", "Uzbekistan": "220V", "Vanuatu": "220V", "Vatican City": "230V", "Venezuela": "120V",
    "Vietnam": "220V", "Yemen": "230V", "Zambia": "230V", "Zimbabwe": "220V", "Other": "220V"
}

# ===== FULL LOCAL DATA FOR ALL REGIONS =====
COUNTRY_LOCAL_DATA = {
    # AFRICA
    "Nigeria": {"currency": "₦", "parts": "Alaba International Market, Jumia.ng", "issue": "NEPA power surge"},
    "Ghana": {"currency": "GH₵", "parts": "Circle Market, Jumia.com.gh", "issue": "Dumsor power cuts"},
    "Kenya": {"currency": "KSh", "parts": "Luthuli Avenue, Jumia.co.ke", "issue": "Voltage fluctuations"},
    "South Africa": {"currency": "R", "parts": "Builders, Takealot.com, Makro", "issue": "Load shedding surges"},
    "Egypt": {"currency": "E£", "parts": "El-Ataba Market, Jumia.eg", "issue": "Voltage drops"},
    "Morocco": {"currency": "MAD", "parts": "Derb Ghallef Market, Jumia.ma", "issue": "Voltage fluctuations"},
    "Algeria": {"currency": "DZD", "parts": "Local markets, Jumia.dz", "issue": "Power cuts"},
    "Tunisia": {"currency": "TND", "parts": "Tunis Markets, Jumia.tn", "issue": "Voltage instability"},
    "Ethiopia": {"currency": "ETB", "parts": "Merkato, Local stores", "issue": "Power outages"},
    "Uganda": {"currency": "UGX", "parts": "Kampala Markets, Jumia.ug", "issue": "Voltage fluctuations"},
    "Tanzania": {"currency": "TZS", "parts": "Kariakoo Market, Jumia.tz", "issue": "Power cuts"},
    "Zimbabwe": {"currency": "USD", "parts": "Mbare Market, ZOL", "issue": "Load shedding"},
    "Zambia": {"currency": "ZMW", "parts": "Lusaka Markets, Jumia.zm", "issue": "Power cuts"},
    "Rwanda": {"currency": "RWF", "parts": "Kigali Markets, Jumia.rw", "issue": "Voltage issues"},
    "Senegal": {"currency": "XOF", "parts": "Dakar Markets, Jumia.sn", "issue": "Power cuts"},
    # AMERICAS
    "United States": {"currency": "$", "parts": "Home Depot, Amazon, Best Buy", "issue": "120V standard"},
    "USA": {"currency": "$", "parts": "Home Depot, Amazon, Best Buy", "issue": "120V standard"},
    "Canada": {"currency": "C$", "parts": "Canadian Tire, Amazon.ca, Best Buy", "issue": "120V appliances"},
    "Mexico": {"currency": "MXN", "parts": "Home Depot Mexico, Amazon.com.mx", "issue": "127V outlets"},
    "Brazil": {"currency": "R$", "parts": "Magazine Luiza, Mercado Livre", "issue": "127V/220V mixed"},
    "Argentina": {"currency": "ARS", "parts": "Mercado Libre, Frávega", "issue": "220V standard"},
    "Colombia": {"currency": "COP", "parts": "Homecenter, Mercado Libre", "issue": "110V outlets"},
    "Chile": {"currency": "CLP", "parts": "Falabella, Paris", "issue": "220V standard"},
    "Peru": {"currency": "PEN", "parts": "Promart, Mercado Libre", "issue": "220V standard"},
    # EUROPE
    "United Kingdom": {"currency": "£", "parts": "B&Q, Currys, Amazon UK", "issue": "230V ring circuits"},
    "UK": {"currency": "£", "parts": "B&Q, Currys, Amazon UK", "issue": "230V ring circuits"},
    "Germany": {"currency": "€", "parts": "MediaMarkt, Amazon.de, Conrad", "issue": "230V standard"},
    "France": {"currency": "€", "parts": "Darty, Boulanger, Amazon.fr", "issue": "230V standard"},
    "Italy": {"currency": "€", "parts": "MediaWorld, Amazon.it", "issue": "230V standard"},
    "Spain": {"currency": "€", "parts": "El Corte Ingles, Amazon.es", "issue": "230V standard"},
    "Poland": {"currency": "PLN", "parts": "Media Expert, Allegro", "issue": "230V standard"},
    "Netherlands": {"currency": "€", "parts": "Bol.com, MediaMarkt", "issue": "230V standard"},
    # ASIA
    "India": {"currency": "₹", "parts": "Amazon.in, Flipkart, Local markets", "issue": "Voltage stabilizer needed"},
    "Pakistan": {"currency": "PKR", "parts": "Hall Road Lahore, Daraz.pk", "issue": "Load shedding"},
    "China": {"currency": "¥", "parts": "JD.com, Taobao", "issue": "220V standard"},
    "Japan": {"currency": "¥", "parts": "Yodobashi, Amazon.co.jp", "issue": "100V outlets"},
    "South Korea": {"currency": "₩", "parts": "Gmarket, Coupang", "issue": "220V standard"},
    "Indonesia": {"currency": "IDR", "parts": "Tokopedia, Bukalapak", "issue": "220V standard"},
    "Philippines": {"currency": "₱", "parts": "Lazada, Shopee", "issue": "220V standard"},
    "Thailand": {"currency": "THB", "parts": "Lazada, HomePro", "issue": "220V standard"},
    "Vietnam": {"currency": "₫", "parts": "Tiki, Shopee", "issue": "220V standard"},
    "Bangladesh": {"currency": "৳", "parts": "Daraz, Local markets", "issue": "Voltage fluctuations"},
    # MIDDLE EAST
    "Saudi Arabia": {"currency": "SAR", "parts": "Extra, Jarir, Amazon.sa", "issue": "Heat and dust"},
    "UAE": {"currency": "AED", "parts": "Carrefour, ACE Hardware, Amazon.ae", "issue": "Heat damages AC"},
    "United Arab Emirates": {"currency": "AED", "parts": "Carrefour, ACE Hardware, Amazon.ae", "issue": "Heat damages AC"},
    "Qatar": {"currency": "QAR", "parts": "Carrefour, Jarir", "issue": "Heat and humidity"},
    "Kuwait": {"currency": "KWD", "parts": "Xcite, Best", "issue": "Heat damages appliances"},
    "Israel": {"currency": "₪", "parts": "KSP, Amazon", "issue": "230V standard"},
    "Turkey": {"currency": "₺", "parts": "Teknosa, Trendyol", "issue": "230V standard"},
    # OCEANIA
    "Australia": {"currency": "A$", "parts": "JB Hi-Fi, Bunnings, Amazon.au", "issue": "230V standard"},
    "New Zealand": {"currency": "NZ$", "parts": "PB Tech, Mighty Ape", "issue": "230V standard"},
    "default": {"currency": "$", "parts": "Local appliance stores, Amazon", "issue": "Standard voltage issues"}
}

# ===== ALL 87 HOME + GLOBAL APPLIANCES =====
ALL_APPLIANCES = [
    # HOME
    "Air Conditioner AC", "Air Purifier", "Ceiling Fan", "Standing Fan", "Table Fan", "Heater", "Humidifier", "Dehumidifier",
    "Refrigerator", "Freezer", "Chest Freezer", "Water Dispenser", "Water Purifier", "Water Heater Geyser", "Electric Kettle",
    "Television TV LED", "Television TV OLED", "Sound System", "Home Theater", "Set Top Box Decoder", "Projector",
    "Washing Machine", "Dryer", "Dishwasher", "Vacuum Cleaner", "Robot Vacuum", "Iron", "Sewing Machine",
    # KITCHEN
    "Microwave Oven", "Oven", "Toaster", "Blender", "Food Processor", "Juicer", "Mixer", "Rice Cooker", "Pressure Cooker",
    "Air Fryer", "Induction Cooker", "Electric Stove", "Gas Cooker", "Grill", "Sandwich Maker", "Coffee Maker",
    # OFFICE
    "Laptop", "Desktop Computer", "Monitor", "Printer", "Scanner", "Photocopier", "Router", "Modem", "UPS", "Stabilizer",
    "Camera CCTV", "Fingerprint Machine", "Card Reader POS",
    # POWER & WORKSHOP
    "Generator", "Solar Inverter", "Solar Panel", "Battery", "Drill Machine", "Grinder", "Welding Machine", "Air Compressor",
    "Water Pump", "Submersible Pump", "Pressure Washer",
    # PERSONAL & MEDICAL
    "Hair Dryer", "Hair Clipper", "Shaving Machine", "Massage Gun", "Nebulizer", "Blood Pressure Machine", "Oxygen Concentrator",
    "Car Battery Charger", "Electric Bike", "Electric Scooter", "Other"
]

# ===== LAYER 4: SETTINGS PAGE =====
def settings_page():
    st.header("⚙️ Itech AI Settings")
    tab1, tab2, tab3, tab4 = st.tabs(["General", "Diagnosis", "Technicians", "Data & Privacy"])
    with tab1:
        st.session_state.language = st.selectbox("🌍 App Language", ["English", "Hausa", "Yoruba", "Igbo", "French", "Arabic", "Spanish", "Portuguese", "Hindi"])
        st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        st.session_state.default_country = st.selectbox("📍 Default Country", options=sorted(COUNTRIES_VOLTAGE.keys()), index=sorted(COUNTRIES_VOLTAGE.keys()).index(st.session_state.default_country))
    with tab2:
        st.session_state.detail_level = st.radio("📊 Detail Level", ["Simple", "Expert"], horizontal=True)
        st.session_state.show_prices = st.toggle("💰 Show Price Estimates", value=st.session_state.show_prices)
        st.session_state.show_panic = st.toggle("🚨 Show Panic Mode Button", value=st.session_state.show_panic)
    with tab3:
        st.session_state.show_tech_map = st.toggle("🗺️ Show 'Find Technician Near Me' Button", value=st.session_state.show_tech_map)
    with tab4:
        if st.button("🗑️ Clear All History"): c.execute("DELETE FROM logs"); conn.commit(); st.toast("✅ Cleared"); st.rerun()
        st.download_button("💾 Export History", data=str(c.execute("SELECT * FROM logs").fetchall()), file_name="ItechAI_History.txt")
        st.caption("Itech AI v1.5.0 Global")

# ===== LAYER 5: MENU =====
page = st.sidebar.radio("Menu", ["Diagnose", "Settings", "History"])
if page == "Settings": settings_page(); st.stop()
if page == "History":
    st.header("📜 Past Repairs")
    rows = c.execute("SELECT timestamp, device, problem, answer FROM logs ORDER BY id DESC").fetchall()
    st.metric("Total", len(rows))
    for ts, dev, prob, ans in rows:
        with st.expander(f"**{dev}** - {ts[:16]}"): st.write(f"**Problem:** {prob}"); st.code(ans)
    st.stop()

# ===== LAYER 6: DIAGNOSE PAGE =====
st.title("🔧 Itech AI - Global Electronics Repair Assistant")
st.warning("⚠️ Troubleshooting guidance only. For electrical/gas work, contact a licensed technician.", icon="⚠️")

panic = st.button("🚨 PANIC MODE", type="primary", use_container_width=True) if st.session_state.show_panic else False
col1, col2, col3 = st.columns(3)
with col1: device = st.selectbox("1. Select Device 🔧", ALL_APPLIANCES, index=None)
with col2: country = st.selectbox("2. Select Country 🌍", sorted(COUNTRIES_VOLTAGE.keys()), index=sorted(COUNTRIES_VOLTAGE.keys()).index(st.session_state.default_country))
with col3: voltage = st.selectbox("3. Voltage", [COUNTRIES_VOLTAGE[country]], disabled=True)
user_input = st.text_area("4. Describe your appliance issue. Any language:")

def get_ai_diagnosis(problem, device, country, voltage, panic):
    if panic: return "🚨 UNPLUG NOW. CALL LICENSED ELECTRICIAN IMMEDIATELY."
    local = COUNTRY_LOCAL_DATA.get(country, COUNTRY_LOCAL_DATA["default"])
    price_rule = f"Give 'DIY Cost:' and 'Technician Cost:' in {local['currency']}" if st.session_state.show_prices else "Do NOT mention prices"
    prompt = f"You are ITECH AI for {country}. Lang:{st.session_state.language}. Detail:{st.session_state.detail_level}. Voltage:{voltage}. Currency:{local['currency']}. Parts:{local['parts']}. Issue:{local['issue']}. RULES: 1.SAFETY UNPLUG 2.3 Steps 3.{price_rule} 4.Reply in {st.session_state.language}"
    res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":prompt},{"role":"user","content":f"{device}: {problem}"}])
    return res.choices[0].message.content

if st.button("Diagnose Now", type="primary", use_container_width=True):
    if not device or not user_input: st.error("❌ Fill Device and Problem")
    else:
        with st.spinner("🔍 Thinking..."):
            answer = get_ai_diagnosis(user_input, device, country, voltage, panic)
            st.success("✅ Done")
            st.markdown(answer); st.code(answer)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: st.button("📋 Copy")
            with col2: st.link_button("📱 Share", f"https://wa.me/?text={urllib.parse.quote(answer)}")
            with col3: st.download_button("💾 Download", data=answer, file_name=f"ItechAI_{device}.txt")
            with col4: st.link_button("🌍 Translate", f"https://translate.google.com/?text={urllib.parse.quote(answer[:500])}")
            if st.session_state.show_tech_map:
                with col5: st.link_button("🗺️ Find Tech", f"https://www.google.com/maps/search/{urllib.parse.quote(f'{device} repair technician near me in {country}')}")
            c.execute("INSERT INTO logs VALUES (NULL,?,?,?,?,?,?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), device, country, voltage, user_input, answer)); conn.commit()
