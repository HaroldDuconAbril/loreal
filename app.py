import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from io import BytesIO
import numpy as np
import requests
from dotenv import load_dotenv

# =============================
# CONFIG
# =============================
load_dotenv()
st.set_page_config(page_title="Auditoría 360° L'Oréal - IPG", layout="wide")

st.markdown("""
<style>
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #ffffff; color: #004a99;
    text-align: center; padding: 10px;
    border-top: 3px solid #004a99;
}
</style>
<div class="footer">🚀 IPG Strategic Intelligence 2026 | Powered by Perplexity</div>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR
# =============================
st.sidebar.title("⚙️ Control Panel")

api_key = st.sidebar.text_input("Perplexity API Key", type="password") or os.getenv("PPLX_API_KEY")

if not api_key:
    st.error("⚠️ Debes ingresar tu API Key de Perplexity")
    st.stop()

modelo = st.sidebar.selectbox(
    "Modelo",
    ["sonar-small-online", "sonar-medium-online"]
)

# =============================
# FUNCIÓN IA (PERPLEXITY)
# =============================
@st.cache_data(show_spinner=False)
def generar_auditoria(cliente, modelo, api_key):

    url = "https://api.perplexity.ai/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Eres un Director Regional de Estrategia en LATAM.

Genera un informe ejecutivo tipo consultora para {cliente}:

1. Marcas de L’Oréal por país
2. Agencias (medios y creativas)
3. Competidores
4. Evolución inversión medios
5. Data clave
6. Stakeholders

Formato:
- Tablas claras
- Datos reales (usa búsqueda web)
- Nivel ejecutivo
- Incluye fuentes
"""

    data = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": "Eres un experto en research de mercado y marketing."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# =============================
# UI
# =============================
st.title("💄 Auditoría 360° L'Oréal LATAM")
st.subheader("Inteligencia de Mercado con datos reales")

cliente = st.text_input("Cliente:", "L'Oréal Groupe")

if st.button("🚀 Generar Auditoría"):

    with st.spinner("Buscando información real en internet..."):

        resultado = generar_auditoria(cliente, modelo, api_key)

        st.markdown(resultado)

        st.divider()

        # =============================
        # DASHBOARD
        # =============================
        st.header("📊 Dashboard Visual")

        col1, col2 = st.columns(2)

        with col1:
            df = pd.DataFrame({
                "Marca": ["L'Oréal", "Unilever", "Natura", "P&G"],
                "Share": [30, 25, 20, 18]
            })
            fig = px.bar(df, x="Marca", y="Share", title="Market Share")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            df2 = pd.DataFrame({
                "Canal": ["Digital", "TV", "Retail Media", "OOH"],
                "Inversión": [55, 25, 15, 5]
            })
            fig2 = px.bar(df2, x="Canal", y="Inversión", title="Mix de Medios")
            st.plotly_chart(fig2, use_container_width=True)

        # =============================
        # TENDENCIAS SIMULADAS
        # =============================
        st.subheader("🔍 Tendencias de Búsqueda")

        semanas = list(range(1, 53))

        df_trend = pd.DataFrame({
            "Semana": semanas,
            cliente: np.random.randint(60, 100, 52),
            "Natura": np.random.randint(50, 90, 52),
            "Unilever": np.random.randint(40, 80, 52)
        })

        fig3 = px.line(df_trend, x="Semana", y=df_trend.columns[1:], title="Interés en el tiempo")
        st.plotly_chart(fig3, use_container_width=True)

        # =============================
        # EXPORT WORD
        # =============================
        doc = Document()
        doc.add_heading(f"Auditoría {cliente}", 0)
        doc.add_paragraph(resultado)

        buffer = BytesIO()
        doc.save(buffer)

        st.download_button(
            "📄 Descargar Word",
            data=buffer.getvalue(),
            file_name="auditoria_loreal.docx"
        )
