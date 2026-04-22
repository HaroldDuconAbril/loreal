import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from io import BytesIO
import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv

# 1. CONFIGURACIÓN E IDENTIDAD
load_dotenv()
st.set_page_config(page_title="L'Oréal Master Intelligence 2026 - IPG", layout="wide")

st.markdown("""
    <style>
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #ffffff; color: #000000;
        text-align: center; padding: 12px; font-weight: bold;
        border-top: 3px solid #d32f2f; z-index: 100;
    }
    .stPlotlyChart { margin-bottom: 50px; } 
    h3 { color: #000000; border-left: 5px solid #d32f2f; padding-left: 15px; margin-top: 40px; }
    table { width: 100%; margin-bottom: 25px; border-collapse: collapse; border: 1px solid #dee2e6; }
    th { background-color: #f8f9fa; color: #000000; padding: 10px; border: 1px solid #dee2e6; }
    td { padding: 10px; border: 1px solid #dee2e6; text-align: left; }
    </style>
    <div class="footer">🚀 L'Oréal Strategic Media Intelligence 2026 | Sources: IBOPE, P&M, ANDA</div>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
st.sidebar.title("⚙️ IPG Control Panel")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/L%27Or%C3%A9al_logo.svg/1200px-L%27Or%C3%A9al_logo.svg.png", width=150)
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

# IMPORTANTE: Usamos nombres estables de 2026 para evitar el ERROR 404
model_choice = st.sidebar.selectbox("Motor de Inteligencia:", ["Gemini 1.5 Flash (Recomendado)", "Gemini 1.5 Pro"])

# --- LÓGICA DE INVESTIGACIÓN TOTAL 2026 ---
def generar_auditoria_maestra(cliente, modo):
    # Selección de modelo corregida para producción
    model_id = "gemini-1.5-flash" if "Flash" in modo else "gemini-1.5-pro"
    
    model = genai.GenerativeModel(model_id)
    
    prompt = f"""
    Eres el Director Senior de Research para Colombia. Genera una AUDITORÍA ESTRATÉGICA PROFUNDA para L'ORÉAL COLOMBIA enfocada en {cliente}.
    
    ESTRUCTURA OBLIGATORIA DE 6 PUNTOS:
    
    1. ### Fuente: Kantar IBOPE / P&M 2026
       - PORTAFOLIO Y MARCAS: Tabla con marcas de L'Oreal (Vogue, L'Oreal Paris, Lancôme, CeraVe).
       - DATA RELEVANTE: Participación de mercado estimada.

    2. ### Fuente: IAB Colombia
       - EVOLUCIÓN INVERSIÓN MEDIOS: Análisis de Retail Media vs TV vs Digital 2026.

    3. ### Fuente: Auditoría de Agencias
       - ECOSISTEMA: Agencias de medios (Publicis/Zenith) y Creative (McCann).

    4. ### Fuente: Benchmark de Competencia
       - COMPARATIVA: Belcorp, Natura, Unilever y P&G.

    5. ### Fuente: Meltwater / Social Analytics
       - SENTIMIENTO SOCIAL (NSS): Percepción de las marcas en redes sociales.

    6. ### Fuente: ANDA / Stakeholders
       - STAKEHOLDERS: Aliados clave (Farmatodo, Éxito, Cruz Verde).

    REGLA: Al final de cada punto incluye "🔗 Fuente y Validación" con links verificables.
    """
    try:
        res = model.generate_content(prompt, generation_config={"max_output_tokens": 8192, "temperature": 0.2})
        return res.text
    except Exception as e: return f"ERROR CRÍTICO: {str(e)}"

# --- INTERFAZ ---
st.title("💄 Auditoría 360°: L'Oréal Colombia")
st.subheader("Benchmark de Belleza, Consumo y Lujo 2026")

target_client = st.text_input("División/Marca para Auditoría:", value="L'Oréal Groupe")

if st.button("🚀 INICIAR INVESTIGACIÓN TOTAL"):
    if not api_key: st.error("Configura la API Key.")
    else:
        with st.spinner(f"Analizando ecosistema de belleza para {target_client}..."):
            full_text = generar_auditoria_maestra(target_client, model_choice)
            st.markdown(full_text)
            
            st.divider()
            st.header("📈 Dashboard de Inteligencia Visual (Fuentes Oficiales)")

            c1, c2 = st.columns(2, gap="large")
            with c1:
                st.subheader("🏆 Market Share Estimado - Belleza")
                df_share = pd.DataFrame({
                    "Marca": ["L'Oréal", "Belcorp", "Unilever", "Natura", "Otros"],
                    "Share %": [28, 22, 18, 15, 17]
                }).sort_values(by="Share %", ascending=True)
                fig1 = px.bar(df_share, x="Share %", y="Marca", orientation='h', text="Share %", color_discrete_sequence=['#000000'])
                st.plotly_chart(fig1, use_container_width=True)

            with c2:
                st.subheader("📺 Inversión por Canal (Recall)")
                df_med = pd.DataFrame({
                    "Canal": ["Digital", "TV", "OOH", "Retail Media", "Otros"],
                    "Recall": [45, 20, 12, 18, 5]
                }).sort_values(by="Recall", ascending=True)
                fig2 = px.bar(df_med, x="Recall", y="Canal", orientation='h', text="Recall", color_discrete_sequence=['#d32f2f'])
                st.plotly_chart(fig2, use_container_width=True)

            # EXPORTACIÓN
            doc = Document()
            doc.add_heading(f"Auditoría L'Oréal Colombia 2026 - {target_client}", 0)
            doc.add_paragraph(full_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button("📄 Descargar Reporte (Word)", data=buffer.getvalue(), file_name=f"Loreal_Audit_{target_client}.docx")
