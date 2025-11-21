import streamlit as st
import requests
import time

st.title("🛡️ CloudDefender – Bot Traffic Simulator")
st.write("Envía tráfico controlado hacia Cloudflare para mostrar detecciones de bots.")

url = st.text_input("URL objetivo (ruta especial recomendada: /__clouddefender_test__):")

traffic_type = st.selectbox("Tipo de tráfico", [
    "Basic Bot",
    "Burst Bot",
    "JA3 Randomizer",
    "Suspicious Header Bot"
])

count = st.slider("Número de requests", 1, 50, 5)

start_btn = st.button("Enviar tráfico")

def send_request(i):
    headers = {
        "X-CloudDefender-Test": "true",
        "X-CD-Demo": "CLOUDDEFENDER TEST",
        "CF-CD-Demo": "CLOUDDEFENDER-TEST",
        "User-Agent": "Python-requests/2.31.0",
    }

    # Variante JA3 falsa
    if traffic_type == "JA3 Randomizer":
        headers["User-Agent"] = f"Bot/{i}.0"
        headers["X-JA3-Fake"] = f"ja3-{i}"

    # Variante encabezados sospechosos
    if traffic_type == "Suspicious Header Bot":
        headers["X-Forwarded-For"] = f"185.66.75.{50+i}"
        headers["X-Origin"] = "botnet"

    try:
        r = requests.get(url, headers=headers, timeout=3)
        return {"req": i, "status": r.status_code}
    except Exception as e:
        return {"req": i, "status": "error", "detail": str(e)}

if start_btn:
    if not url:
        st.error("Ingresa una URL válida.")
        st.stop()

    st.write("📡 Enviando tráfico…")

    out = []
    for i in range(1, count + 1):
        out.append(send_request(i))
        time.sleep(0.25)

    st.success("Simulación completada.")
    st.json(out)
