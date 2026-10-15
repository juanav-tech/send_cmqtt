import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Configuración de página con diseño estético
st.set_page_config(
    page_title="Smart Home - Iluminación Inteligente",
    page_icon="💡",
    layout="centered"
)

# Estilos CSS personalizados para mejorar la estética visual sin alterar la comunicación
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid #38BDF8;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
    }
    .card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Versión de Python discreta en la parte superior
st.markdown(f'<p style="text-align: right; color: #94A3B8; font-size: 12px;">Python v{platform.python_version()}</p>', unsafe_allow_html=True)

values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("JuanaCliente")
client1.on_message = on_message

# Encabezado estético enfocado en la función de luz inteligente
st.markdown("""
    <div class="main-header">
        <h1 style="color: #FFFFFF; margin: 0; font-size: 24px;">💡 Control de Iluminación Inteligente</h1>
        <p style="color: #94A3B8; margin: 5px 0 0 0;">Panel domótico conectado con Wokwi vía MQTT</p>
    </div>
""", unsafe_allow_html=True)

# Tarjeta para el control digital (ON / OFF)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔌 Estado del Foco / Relé")

col_on, col_off = st.columns(2)

with col_on:
    if st.button('🟢 Encender (ON)', use_container_width=True):
        act1 = "ON"
        client1 = paho.Client("JuanaCliente")                         
        client1.on_publish = on_publish                         
        client1.connect(broker, port)  
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_juana", message)
    else:
        st.write('')

with col_off:
    if st.button('🔴 Apagar (OFF)', use_container_width=True):
        act1 = "OFF"
        client1 = paho.Client("JuanaCliente")                         
        client1.on_publish = on_publish                         
        client1.connect(broker, port)  
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_juana", message)
    else:
        st.write('')

st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta para el control analógico / dimmer
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🎚️ Regulador de Intensidad (Dimmer)")

values = st.slider('Selecciona el nivel de brillo (%)', 0.0, 100.0)
st.markdown(f'<p style="color: #38BDF8; font-weight: bold;">Valor seleccionado: {values}%</p>', unsafe_allow_html=True)

if st.button('📡 Enviar valor analógico', use_container_width=True):
    client1 = paho.Client("JuanaCliente")                         
    client1.on_publish = on_publish                         
    client1.connect(broker, port)   
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_j", message)
else:
    st.write('')

st.markdown('</div>', unsafe_allow_html=True)
