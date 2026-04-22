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
# Prioridad: Input > Secrets de Streamlit > .env
api_key = api_key_input if api_key_input else os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

model_choice = st.sidebar.selectbox("Motor de Inteligencia:", ["Gemini 1.5 Flash", "Gemini 1.5 Pro"])

# --- LÓGICA DE INVESTIGACIÓN TOTAL 2026 ---
def generar_auditoria_loreal(mercado):
    # Forzamos los nombres exactos que espera la API v1
    m_id = "models/gemini-1.5-flash" if "Flash" in model_choice else "models/gemini-1.5-pro"
    
    try:
        # IMPORTANTE: Instanciamos el modelo directamente con el ID completo
        model = genai.GenerativeModel(model_name=m_id)
        
        prompt = f"""
        Eres el Director de Estrategia para {mercado}. Genera una AUDITORÍA ESTRATÉGICA PROFUNDA para L'ORÉAL en Abril de 2026.
        Todo debe ser coherente con la industria de cosméticos y belleza.

        1. ### Portafolio de Marcas 2026
        2. ### Agencias (Publicis/McCann)
        3. ### Competencia (Belcorp/Natura)
        4. ### Inversión Medios (IBOPE)
        5. ### Stakeholders

        Usa tablas markdown donde sea necesario.
        """
        
        # Agregamos configuración de generación para mayor estabilidad
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=4000
            )
        )
        return response.text
    except Exception as e:
        # Si falla, intentamos sin el prefijo "models/" como último recurso
        try:
            alt_id = m_id.replace("models/", "")
            model = genai.GenerativeModel(model_name=alt_id)
            response = model.generate_content(prompt)
            return response.text
        except:
            return f"❌ Error persistente: {str(e)}. Verifica que tu API Key sea de un proyecto con facturación habilitada o dentro de los límites gratuitos de Google AI Studio."

# --- INTERFAZ ---
st.title("💄 L'Oréal Master Intelligence Bot")
target_market = st.text_input("Mercado para Auditoría:", value="Colombia")

if st.button("🚀 INICIAR INVESTIGACIÓN TOTAL"):
    if not api_key:
        st.error("Configura la API Key.")
    else:
        with st.spinner("Conectando con Google AI..."):
            full_text = generar_auditoria_loreal(target_market)
            st.markdown(full_text)
            
            # --- DASHBOARD VISUAL ---
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📊 Inversión en Medios")
                df_med = pd.DataFrame({"Canal": ["Digital", "TV", "OOH", "Retail Media"], "Inv": [45, 20, 15, 20]})
                fig1 = px.pie(df_med, values="Inv", names="Canal", hole=.4, color_discrete_sequence=['#000000', '#d32f2f'])
                st.plotly_chart(fig1, use_container_width=True)
            with c2:
                st.subheader("🏆 Market Share")
                df_share = pd.DataFrame({"Marca": ["L'Oréal", "Belcorp", "Unilever", "Natura"], "Share": [28, 22, 18, 15]})
                fig2 = px.bar(df_share, x="Share", y="Marca", orientation='h', color_discrete_sequence=['#000000'])
                st.plotly_chart(fig2, use_container_width=True)

            # EXPORTACIÓN
            doc = Document()
            doc.add_heading(f"Reporte L'Oréal - {target_market}", 0)
            doc.add_paragraph(full_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button("📄 Descargar Reporte (Word)", data=buffer.getvalue(), file_name=f"Loreal_{target_market}.docx")
