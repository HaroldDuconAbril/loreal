import streamlit as st
import os
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO
import numpy as np
from dotenv import load_dotenv
from groq import Groq

# =============================
# CONFIG
# =============================
load_dotenv()
st.set_page_config(page_title="Auditoría 360° L'Oréal", layout="wide")

# =============================
# SIDEBAR
# =============================
st.sidebar.title("⚙️ Control Panel")

api_key = st.sidebar.text_input("Groq API Key", type="password") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Ingresa tu API Key de Groq")
    st.stop()

client = Groq(api_key=api_key)

# =============================
# FUNCIÓN IA
# =============================
@st.cache_data(show_spinner=False)
def generar_auditoria(cliente):

    prompt = f"""
Eres un Director Regional de Estrategia en LATAM.

Haz un informe ejecutivo para {cliente}:

1. Marcas por país
2. Agencias (medios y creativas)
3. Competidores
4. Inversión en medios
5. Data relevante
6. Stakeholders

Formato:
- Tablas
- Claro
- Ejecutivo
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# =============================
# UI
# =============================
st.title("💄 Auditoría 360° L'Oréal LATAM")

cliente = st.text_input("Cliente:", "L'Oréal Groupe")

if st.button("🚀 Generar Auditoría"):

    with st.spinner("Generando análisis..."):

        resultado = generar_auditoria(cliente)
        st.markdown(resultado)

        # DASHBOARD
        df = pd.DataFrame({
            "Marca": ["L'Oréal", "Unilever", "Natura"],
            "Share": [30, 25, 20]
        })

        fig = px.bar(df, x="Marca", y="Share")
        st.plotly_chart(fig)

        # EXPORT
        doc = Document()
        doc.add_paragraph(resultado)

        buffer = BytesIO()
        doc.save(buffer)

        st.download_button(
            "📄 Descargar Word",
            buffer.getvalue(),
            "reporte.docx"
        )
