import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="Cloudflare Bot Traffic Simulator", layout="wide")
st.title("🤖 Mini Bot Traffic Simulator (Cloudflare Demo)")
st.caption("Simulación ética y controlada de tráfico para demostrar Bot Management. Solo usar con dominios propios.")

st.markdown("---")
st.subheader("1. URL autorizada")

target_url = st.text_input(
    "URL del test (ej: https://lab.tudominio.com/bot-test)",
    ""
)

st.warning("⚠️ Usa solo dominios que controles tú.")

if not target_url:
    st.stop()

st.markdown("---")
st.subheader("2. Tipo de tráfico a simular")

traffic_type = st.selectbox(
    "Tipo de tráfico",
    [
        "Basic Bot (script-like)",
        "Medium Bot (headless-like)",
        "Human Simulated (real browser)",
        "Controlled Burst",
    ]
)

count = st.slider(
    "Número de requests",
    min_value=1,
    max_value=20,
    value=5
)

run = st.button("🚀 Enviar simulación")

# --- User-Agent presets ---
UA_BASIC_BOT = "Python-requests/2.31.0"
UA_HEADLESS = "Mozilla/5.0 (X11; Linux x86_64) HeadlessChrome"
UA_HUMAN = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1)"
]

def send_request(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.status_code
    except:
        return "error"


if run:
    st.markdown("### 🚦 Enviando tráfico…")

    logs = []

    for i in range(count):

        # -----------------------------------------
        # Marca visible para el cliente:
        # CLOUDDEFENDER TEST
        # -----------------------------------------

        base_headers = {
            "X-CloudDefender-Test": "true",
            "X-CD-Demo": "CLOUDDEFENDER TEST",
            "CF-CD-Demo": "CLOUDDEFENDER-TEST"
        }

        if traffic_type == "Basic Bot (script-like)":
            headers = {**base_headers, "User-Agent": UA_BASIC_BOT}

        elif traffic_type == "Medium Bot (headless-like)":
            headers = {
                **base_headers,
                "User-Agent": UA_HEADLESS,
                "X-Headless-Sim": "1"
            }

        elif traffic_type == "Human Simulated (real browser)":
            headers = {
                **base_headers,
                "User-Agent": random.choice(UA_HUMAN)
            }

        elif traffic_type == "Controlled Burst":
            headers = {
                **base_headers,
                "User-Agent": UA_BASIC_BOT,
                "X-Burst-Demo": str(random.randint(1000, 9999))
            }

        status = send_request(target_url, headers)
        logs.append({
            "request": i + 1,
            "headers_sent": headers,
            "status": status
        })

        time.sleep(0.3)

    st.success("Simulación completada.")
    st.json(logs)

    st.info("""
    En Cloudflare (Logs, Security o Bots) podrás ver:
    - Los headers: X-CloudDefender-Test, X-CD-Demo
    - El User-Agent modificado
    - El score de Bot Management
    """)
