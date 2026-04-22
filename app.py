import streamlit as st
import os
from groq import Groq

st.sidebar.title("⚙️ Control Panel")

api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.stop()

client = Groq(api_key=api_key)

# MODELOS DISPONIBLES ACTUALIZADOS
MODELOS = [
    "llama-3.3-70b-versatile",
    "llama-3.3-8b-instant",
    "mixtral-8x7b-32768"
]

modelo = st.sidebar.selectbox("Modelo", MODELOS)

def generar_auditoria(prompt):
    for intento in MODELOS:  # intenta con varios modelos automáticamente
        try:
            response = client.chat.completions.create(
                model=intento,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content

        except Exception as e:
            continue  # prueba siguiente modelo

    return "❌ Todos los modelos fallaron. Revisa tu API Key o conexión."

# UI
st.title("💄 Auditoría L'Oréal")

if st.button("Generar"):

    prompt = "Haz auditoría de L'Oréal en LATAM (marcas, agencias, competencia, inversión, stakeholders)"

    resultado = generar_auditoria(prompt)

    st.write(resultado)
