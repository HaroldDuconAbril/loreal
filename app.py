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
st.set_page_config(page_title="L'Oréal Master Intelligence 2026", layout="wide")

st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #ffffff; color: #d32f2f; text-align: center; padding: 12px; font-weight: bold; border-top: 3px solid #000000; z-index: 100; }
    h3 { color: #000000; border-left: 5px solid #d32f2f; padding-left: 15px; margin-top: 40px; }
    </style>
    <div class="footer">🚀 L'Oréal Strategic Media Intelligence 2026 | Sources: IBOPE, P&M, ANDA</div>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
st.sidebar.title("⚙️ IPG Control Panel")
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

# Lista de modelos simplificada
model_choice = st.sidebar.selectbox("Motor de Inteligencia:", ["Flash (Estable)", "Pro (Complejo)"])

def generar_auditoria_loreal(mercado):
    # Definimos los candidatos por prioridad para evitar el 404
    if "Flash" in model_choice:
        candidatos = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-1.5-flash-latest"]
    else:
        candidatos = ["gemini-1.5-pro", "models/gemini-1.5-pro", "gemini-1.5-pro-latest"]
    
    prompt = f"""
    Eres el Director Senior de Estrategia para {mercado}. Genera una AUDITORÍA ESTRATÉGICA EXTENSA para L'ORÉAL (Abril 2026).
    
    ESTRUCTURA OBLIGATORIA:
    1. ### Portafolio de Marcas 2026 (Consumo, Lujo, Dermo, Profesional)
    2. ### Ecosistema de Agencias (Publicis Zenith / McCann)
    3. ### Benchmark Competitivo (Belcorp, Natura, Unilever)
    4. ### Inversión Medios (Retail Media vs TV según IBOPE 2026)
    5. ### Stakeholders y Alianzas (Farmatodo, Éxito, ANDA)
    
    Regla: Incluye enlaces verificables y trazabilidad de datos.
    """
    
    last_error = ""
    for model_name in candidatos:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue # Si falla, prueba el siguiente nombre en la lista
            
    return f"❌ Error Crítico: No se pudo conectar con ningún modelo. Detalle: {last_error}"

# --- INTERFAZ ---
st.title("💄 L'Oréal Master Intelligence Bot")
target_market = st.text_input("Mercado:", value="Colombia")

if st.button("🚀 INICIAR INVESTIGACIÓN TOTAL"):
    if not api_key:
        st.error("Configura la API Key.")
    else:
        with st.spinner("Conectando con Google AI Core..."):
            full_text = generar_auditoria_loreal(target_market)
            st.markdown(full_text)
            
            # --- DASHBOARD ---
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                df_med = pd.DataFrame({"Canal": ["Digital", "TV", "OOH", "Retail Media"], "Inv": [45, 20, 15, 20]})
                st.plotly_chart(px.pie(df_med, values="Inv", names="Canal", hole=.4, title="Inversión Medios 2026"), use_container_width=True)
            with c2:
                df_share = pd.DataFrame({"Marca": ["L'Oréal", "Belcorp", "Unilever", "Natura"], "Share": [28, 22, 18, 15]})
                st.plotly_chart(px.bar(df_share, x="Share", y="Marca", orientation='h', title="Market Share Belleza"), use_container_width=True)

            # EXPORTACIÓN
            doc = Document()
            doc.add_heading(f"Reporte L'Oréal - {target_market}", 0)
            doc.add_paragraph(full_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button("📄 Descargar Reporte (Word)", data=buffer.getvalue(), file_name=f"Loreal_{target_market}.docx")
