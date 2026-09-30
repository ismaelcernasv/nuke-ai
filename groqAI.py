import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

url_groq = "https://api.groq.com/openai/v1/chat/completions"
api_key = os.getenv("GROQ_API_KEY")
password_secreta = os.getenv("APP_PASSWORD")

st.title("NUKE AI")
st.subheader("Created by NukeSv")
st.sidebar.title("Panel de control")

# PASO 1: Crear el gafete (falso por defecto)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# PASO 2: La puerta de seguridad
if not st.session_state["autenticado"]:
    contrasena = st.text_input("Ingrese la contraseña para continuar: ", type="password")
    
    if contrasena == password_secreta:
        st.session_state["autenticado"] = True
        st.rerun() # Recarga la página al instante
    elif contrasena != "":
        st.error(" 🛑 CONTRASEÑA INCORRECTA!, ACCESO DENEGADO 🛑")

# PASO 3: El interior del sistema (Chat)
if st.session_state["autenticado"]:
    
    if st.sidebar.button("Eliminar Historial"):
        st.session_state["mensajes"] = [{"role": "system", "content": "Eres NukeAI, un sistema de inteligencia artificial avanzado. Respondes de forma fría, analítica y técnica, similar a la computadora de una nave espacial en una película de ciencia ficción. De vez en cuando eres misterioso."}]

    if "mensajes" not in st.session_state:
        st.session_state["mensajes"] = [{"role": "system", "content": "Eres NukeAI, un sistema de inteligencia artificial avanzado. Respondes de forma fría, analítica y técnica, similar a la computadora de una nave espacial en una película de ciencia ficción. De vez en cuando eres misterioso."}]
        
    for mensaje in st.session_state["mensajes"]:
        if mensaje["role"] != "system":
            with st.chat_message(mensaje["role"]):
                st.write(mensaje["content"])

    pregunta_usuario = st.chat_input("Escribe tu mensaje aca:")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    def consultarAI(historial_completo):
        payload = {
            "model" : "qwen/qwen3.8-27b",
            "messages" : historial_completo
        }
        respuesta = requests.post(url_groq, headers=headers, json=payload)
        mensaje_final = respuesta.json()['choices'][0]['message']['content']
        return mensaje_final

    if pregunta_usuario:
        with st.chat_message("user"):
            st.write(pregunta_usuario)
        
        st.session_state["mensajes"].append({"role": "user", "content": pregunta_usuario})
        
        with st.spinner("Pensando..."):
            try:
                respuesta_ai = consultarAI(st.session_state["mensajes"])
                
                with st.chat_message("assistant"):
                    st.write(respuesta_ai)
                
                st.session_state["mensajes"].append({"role" : "assistant", "content": respuesta_ai})
                
            except Exception as e:
                st.error(f"Lo siento, ocurrió un error técnico: {e}")
