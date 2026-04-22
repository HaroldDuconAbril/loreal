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
        background-color: #ffffff; color: #d32f2f;
        text-align: center; padding: 12px; font-weight: bold;
        border-top: 3px solid #000000; z-index: 100;
    }
    .stPlotlyChart { margin-bottom: 50px; } 
    h3 { color: #000000; border-left: 5px solid #d32f2f; padding-left: 15px; margin-top: 40px; }
    table { width: 100%; margin-bottom: 25px; border-collapse: collapse; border: 1px solid #dee2e6; }
    th { background-color: #f8f9fa; color: #000000; padding: 10px; border: 1px solid #dee2e6; }
    td { padding: 10px; border: 1px solid #dee2e6; text-align: left; }
    </style>
    <div class="footer">🚀 L'Oréal Market Intelligence | Sources: IBOPE, P&M, ANDA, Kantar 2026</div>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
st.sidebar.title("⚙️ IPG Control Panel")
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

# Nombres de modelos estables para evitar el 404
model_choice = st.sidebar.selectbox("Motor de Inteligencia:", ["Gemini 1.5 Flash", "Gemini 1.5 Pro"])

# --- LÓGICA DE INVESTIGACIÓN TOTAL 2026 ---
def generar_auditoria_loreal(mercado):
    # Forzamos el nombre del modelo sin sufijos "preview" o fechas para evitar el 404
    m_id = "gemini-1.5-flash" if "Flash" in model_choice else "gemini-1.5-pro"
    
    # IMPORTANTE: No usamos list_models para evitar errores de permisos en algunas regiones
    model = genai.GenerativeModel(model_name=m_id)
    
    prompt = f"""
    Eres el Director de Estrategia Senior para {mercado}. Genera una AUDITORÍA ESTRATÉGICA PROFUNDA para L'ORÉAL en Abril de 2026.
    
    ESTRUCTURA DE RESPUESTA (Usa '###' para encabezados):
    1. ### Portafolio de Marcas en Colombia 2026
       (División Masivo, Lujo, Dermo y Profesional).
    2. ### Ecosistema de Agencias (Medios y Creative)
       (Menciona Publicis/Zenith y McCann).
    3. ### Panorama Competitivo (Kantar/IBOPE)
       (Compara con Belcorp, Natura y Unilever).
    4. ### Evolución de Inversión 2024-2026
       (Retail Media y Digital First).
    5. ### Stakeholders Locales
       (ANDA, Farmatodo, Éxito, Rappi).

    Regla: Incluye una sección de '🔗 Fuente y Validación' al final de cada punto.
    """
    
    try:
        # Forzamos la llamada
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Error crítico al conectar con Gemini: {str(e)}. Tip: Asegúrate de que la API Key sea correcta y tenga acceso al modelo {m_id}."

# --- INTERFAZ ---
st.title("💄 L'Oréal Master Intelligence Bot")
st.subheader("Auditoría 360°: Marcas, Medios y Competencia (Colombia 2026)")

target_market = st.text_input("Mercado para Auditoría:", value="Colombia")

if st.button("🚀 INICIAR INVESTIGACIÓN TOTAL"):
    if not api_key:
        st.error("Configura la API Key.")
    else:
        with st.spinner("Conectando con servidores de Google..."):
            full_text = generar_auditoria_loreal(target_market)
            st.markdown(full_text)
            
            # --- DASHBOARD VISUAL ---
            st.divider()
            st.header("📈 Dashboard de Visualización (Proyecciones 2026)")

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📊 Inversión en Medios")
                df_med = pd.DataFrame({"Canal": ["Digital", "TV", "OOH", "Retail Media"], "Inv": [45, 20, 15, 20]})
                fig1 = px.pie(df_med, values="Inv", names="Canal", hole=.4, color_discrete_sequence=['#000000', '#d32f2f', '#757575', '#bdbdbd'])
                st.plotly_chart(fig1, use_container_width=True)

            with c2:
                st.subheader("🏆 Market Share Estimado")
                df_share = pd.DataFrame({"Marca": ["L'Oréal", "Belcorp", "Unilever", "Natura"], "Share": [28, 22, 18, 15]})
                fig2 = px.bar(df_share, x="Share", y="Marca", orientation='h', color_discrete_sequence=['#000000'])
                st.plotly_chart(fig2, use_container_width=True)

            # --- EXPORTACIÓN ---
            doc = Document()
            doc.add_heading(f"Reporte L'Oréal - {target_market}", 0)
            doc.add_paragraph(full_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button("📄 Descargar Reporte (Word)", data=buffer.getvalue(), file_name=f"Loreal_{target_market}_2026.docx")
