import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from io import BytesIO
import numpy as np
from dotenv import load_dotenv
from groq import Groq

# =============================
# CONFIGURACIÓN
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
<div class="footer">🚀 IPG Strategic Intelligence 2026 | Powered by Groq</div>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR
# =============================
st.sidebar.title("⚙️ Control Panel")

api_key = st.sidebar.text_input("Groq API Key", type="password") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Ingresa tu API Key de Groq")
    st.stop()

client = Groq(api_key=api_key)

modelo = st.sidebar.selectbox(
    "Modelo IA",
    [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]
)

# =============================
# FUNCIÓN IA
# =============================
@st.cache_data(show_spinner=False)
def generar_auditoria(cliente, modelo):

    prompt = f"""
Eres el Director Regional de Estrategia en LATAM (IPG).

Construye un INFORME EJECUTIVO estilo consultora para {cliente} (L'Oréal).

OBJETIVO:
1. Marcas por mercado
2. Agencias (medios y creativas)
3. Competidores
4. Evolución inversión medios
5. Data relevante
6. Stakeholders

ESTRUCTURA:

## 1. 🌍 PRESENCIA POR MERCADO
Tabla: País | Marcas | Segmento

## 2. 🎯 AGENCIAS
Tabla: Marca | Medios | Creativa | Modelo

## 3. 🥊 COMPETENCIA
Tabla: Marca | Competidores | Grupo

## 4. 📊 INVERSIÓN MEDIOS
Análisis últimos años (Digital vs TV vs Retail Media)

## 5. 📈 DATA CLAVE
Tabla: Marca | Posicionamiento | Target | Insight | Canal

## 6. 🤝 STAKEHOLDERS
Tabla: Tipo | Nombre | Rol

## 7. 🧠 CONCLUSIONES
- Oportunidades
- Riesgos
- Recomendaciones

FORMATO:
- Tablas claras
- Lenguaje ejecutivo
- Máximo 5 bullets por sección
"""

    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# =============================
# UI
# =============================
st.title("💄 Auditoría 360° L'Oréal LATAM")
st.subheader("Benchmark de marcas, agencias y competencia")

cliente = st.text_input("Cliente:", "L'Oréal Groupe")

if st.button("🚀 Generar Auditoría"):

    with st.spinner("Generando análisis estratégico..."):

        resultado = generar_auditoria(cliente, modelo)

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

        st.divider()

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
        # EXPORTACIÓN WORD
        # =============================
        doc = Document()
        doc.add_heading(f"Auditoría {cliente}", 0)
        doc.add_paragraph(resultado)

        buffer = BytesIO()
        doc.save(buffer)

        st.download_button(
            "📄 Descargar Reporte (Word)",
            data=buffer.getvalue(),
            file_name="auditoria_loreal.docx"
        )
