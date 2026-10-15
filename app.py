import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de la página
st.set_page_config(
    page_title="Smart Home Hub 🏠",
    page_icon="🏠",
    layout="wide"
)

# Estilos CSS personalizados para un panel domótico moderno
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
        font-size: 28px;
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
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado visual del sistema
st.markdown("""
    <div class="home-banner">
        <div class="banner-title">🏠 Smart Home IoT Hub</div>
        <div class="banner-subtitle">Panel de control domótico centralizado para climatización, iluminación y seguridad del hogar mediante MQTT.</div>
    </div>
""", unsafe_allow_html=True)

# Configuración de MQTT en la barra lateral
with st.sidebar:
    st.header("⚙️ Configuración MQTT")
    broker = st.text_input("Broker MQTT", value="broker.mqttdashboard.com")
    port = st.number_input("Puerto", value=1883, step=1)
    topic = st.text_input("Tópico Principal", value="cmqtt_casa_inteligente")
    st.markdown("---")
    st.caption(f"Python v{platform.python_version()}")

def on_publish(client, userdata, result):
    print("El comando ha sido publicado con éxito en el broker MQTT\n")

# Función genérica para enviar los paquetes JSON por MQTT
def publicar_mqtt(payload_dict):
    try:
        client = paho.Client("SmartHomeDashboard")
        client.on_publish = on_publish
        client.connect(broker, int(port))
        message = json.dumps(payload_dict)
        client.publish(topic, message)
        client.disconnect()
        st.toast("¡Comando enviado por MQTT!", icon="📡")
    except Exception as e:
        st.error(f"Error de conexión MQTT: {e}")

# Layout principal dividido en 3 áreas funcionales del hogar
col_luces, col_clima, col_puerta = st.columns(3, gap="medium")

# --- 1. ILUMINACIÓN INTELIGENTE ---
with col_luces:
    st.markdown("### 💡 Iluminación Sala")
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        luz_estado = st.toggle("Encender Luz Principal", value=False)
        brillo_luz = st.slider("Intensidad de Brillo (%)", 0, 100, 50, disabled=not luz_estado)
        
        if st.button("Aplicar Cambios de Luz", use_container_width=True):
            estado_texto = "ON" if luz_estado else "OFF"
            publicar_mqtt({
                "dispositivo": "luz_sala",
                "estado": estado_texto,
                "brillo": brillo_luz if luz_estado else 0
            })
            st.success(f"Luz: {estado_texto} ({brillo_luz}%)")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CLIMATIZACIÓN Y TERMOSTATO ---
with col_clima:
    st.markdown("### 🌡️ Climatización")
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        modo_clima = st.selectbox("Modo del Aire Acondicionado", ["Apagado", "Refrigeración (Cool)", "Calefacción (Heat)", "Automático"])
        temperatura = st.slider("Temperatura Deseada (°C)", 16.0, 30.0, 22.0, 0.5)
        
        if st.button("Actualizar Termostato", use_container_width=True):
            publicar_mqtt({
                "dispositivo": "termostato",
                "modo": modo_clima,
                "temperatura_setpoint": temperatura
            })
            st.success(f"Clima: {modo_clima} a {temperatura}°C")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. SEGURIDAD Y CERRADURA INTELIGENTE ---
with col_puerta:
    st.markdown("### 🚪 Seguridad Puerta")
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        estado_puerta = st.radio("Estado de la Cerradura", ["🔒 Bloqueada (Segura)", "🔓 Desbloqueada (Abierta)"])
        alerta_panico = st.checkbox("🚨 Activar Alarma Silenciosa")
        
        if st.button("Enviar Comando de Seguridad", use_container_width=True):
            lock_status = "LOCKED" if "Bloqueada" in estado_puerta else "UNLOCKED"
            publicar_mqtt({
                "dispositivo": "cerradura_principal",
                "estado_puerta": lock_status,
                "alarma": alerta_panico
            })
            st.warning(f"Seguridad actualizada: {lock_status}")
        st.markdown('</div>', unsafe_allow_html=True)
