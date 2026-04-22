import streamlit as st
import os
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO
from dotenv import load_dotenv

from google import genai  # ✅ NUEVA LIBRERÍA

# CONFIG
load_dotenv()
st.set_page_config(page_title="L'Oréal Intelligence", layout="wide")

# API KEY
api_key = st.sidebar.text_input("Gemini API Key", type="password") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Falta API Key")
    st.stop()

client = genai.Client(api_key=api_key)

# MODELOS ACTUALES (estos sí existen)
model_choice = st.sidebar.selectbox(
    "Modelo",
    ["gemini-2.0-flash", "gemini-2.0-flash-lite"]
)

# FUNCIÓN IA
def generar_auditoria(cliente, model_id):
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=f"""
            Eres un experto en marketing en Colombia.

            Haz una auditoría estratégica para {cliente} incluyendo:
            - mercado
            - competencia
            - inversión en medios
            - insights
            """,
        )

        return response.text

    except Exception as e:
        return f"❌ ERROR REAL: {str(e)}"

# UI
st.title("💄 Auditoría L'Oréal Colombia")

cliente = st.text_input("Marca:", "L'Oréal Groupe")

if st.button("Generar"):
    with st.spinner("Analizando..."):
        resultado = generar_auditoria(cliente, model_choice)
        st.write(resultado)

        # gráfico ejemplo
        df = pd.DataFrame({
            "Marca": ["L'Oréal", "Unilever", "Natura"],
            "Share": [30, 25, 20]
        })

        fig = px.bar(df, x="Marca", y="Share")
        st.plotly_chart(fig)

        # export
        doc = Document()
        doc.add_paragraph(resultado)

        buffer = BytesIO()
        doc.save(buffer)

        st.download_button("Descargar Word", buffer.getvalue(), "reporte.docx")
