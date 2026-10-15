import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de la página
st.set_page_config(
    page_title="Control de Iluminación Inteligente 💡",
    page_icon="💡",
    layout="centered"
)

# Estilos CSS personalizados para un panel domótico limpio
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .home-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #38BDF8;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .banner-title {
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
    }
    .banner-subtitle {
        font-size: 14px;
        color: #94A3B8;
    }
    .control-card {
        background-color: #1E293B;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado visual del sistema
st.markdown("""
    <div class="home-banner">
        <div class="banner-title">💡 Control de Iluminación Inteligente</div>
        <div class="banner-subtitle">Gestiona el encendido, apagado y la intensidad lumínica de la sala mediante MQTT.</div>
    </div>
""", unsafe_allow_html=True)

# Configuración de MQTT en la barra lateral
with st.sidebar:
    st.header("⚙️ Configuración MQTT")
    broker = st.text_input("Broker MQTT", value="broker.mqttdashboard.com")
    port = st.number_input("Puerto", value=1883, step=1)
    topic = st.text_input("Tópico Principal", value="cmqtt_iluminacion_sala")
    st.markdown("---")
    st.caption(f"Python v{platform.python_version()}")

def on_publish(client, userdata, result):
    print("El comando de iluminación ha sido publicado con éxito\n")

# Función para enviar el paquete JSON por MQTT
def publicar_mqtt(payload_dict):
    try:
        client = paho.Client("SmartLightDashboard")
        client.on_publish = on_publish
        client.connect(broker, int(port))
        message = json.dumps(payload_dict)
        client.publish(topic, message)
        client.disconnect()
        st.toast("¡Comando de luz enviado por MQTT!", icon="📡")
    except Exception as e:
        st.error(f"Error de conexión MQTT: {e}")

# Panel único de control de iluminación
st.markdown("### 🛋️ Panel de la Sala")
with st.container():
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    
    luz_estado = st.toggle("Encender Luz Principal", value=False)
    brillo_luz = st.slider("Intensidad de Brillo (%)", 0, 100, 50, disabled=not luz_estado)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Enviar Configuración de Luz", use_container_width=True):
        estado_texto = "ON" if luz_estado else "OFF"
        nivel_brillo = brillo_luz if luz_estado else 0
        
        publicar_mqtt({
            "dispositivo": "luz_sala",
            "estado": estado_texto,
            "brillo": nivel_brillo
        })
        
        if luz_estado:
            st.success(f"Luz encendida al {nivel_brillo}% de intensidad.")
        else:
            st.info("Luz apagada.")
            
    st.markdown('</div>', unsafe_allow_html=True)
