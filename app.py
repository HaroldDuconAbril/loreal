import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from io import BytesIO
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import numpy as np
from dotenv import load_dotenv

# 1. CONFIGURACIÓN E IDENTIDAD
load_dotenv()
st.set_page_config(page_title="L'Oréal Master Intelligence 2026 - IPG", layout="wide")

# Estilo visual L'Oréal
st.markdown("""
    <style>
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #ffffff; color: #d32f2f;
        text-align: center; padding: 12px; font-weight: bold;
        border-top: 3px solid #000000; z-index: 100;
    }
    h3 { color: #000000; border-left: 5px solid #d32f2f; padding-left: 15px; margin-top: 40px; }
    </style>
    <div class="footer">🚀 L'Oréal Market Intelligence | Sources: IBOPE, P&M, ANDA, Kantar 2026</div>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
st.sidebar.title("⚙️ IPG Control Panel")
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.getenv("GOOGLE_API_KEY")

if api_key:
    # FORZAMOS CONFIGURACIÓN
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

# Seleccionamos modelos con nombres de producción (v1)
model_choice = st.sidebar.selectbox("Motor de Inteligencia:", ["gemini-1.5-flash", "gemini-1.5-pro"])

def generar_auditoria_loreal(mercado):
    try:
        # Inicialización limpia del modelo
        model = genai.GenerativeModel(
            model_name=model_choice,
            generation_config=GenerationConfig(
                temperature=0.1,
                top_p=0.95,
                max_output_tokens=4096
            )
        )
        
        prompt = f"""
        Eres el Director de Estrategia para {mercado}. Genera una AUDITORÍA ESTRATÉGICA PROFUNDA para L'ORÉAL en Abril de 2026.
        Céntrate en: Marcas (Vogue, L'Oreal Paris), Agencias (Publicis, McCann), Competencia (Belcorp, Natura) e Inversión IBOPE.
        Usa encabezados con '###'.
        """
        
        # Intentamos la generación
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Fallback de emergencia si el nombre corto falla
        try:
            retry_model = genai.GenerativeModel(f"models/{model_choice}")
            return retry_model.generate_content(prompt).text
        except Exception as e2:
            return f"❌ Error de Conexión API: {str(e2)}. \n\n**Tip para Harold:** Verifica en Google AI Studio que tu API Key no tenga restricciones de facturación o cuota."

# --- INTERFAZ ---
st.title("💄 L'Oréal Master Intelligence Bot")
target_market = st.text_input("Mercado:", value="Colombia")

if st.button("🚀 INICIAR INVESTIGACIÓN TOTAL"):
    if not api_key:
        st.error("Configura la API Key.")
    else:
        with st.spinner("Conectando con Google Cloud v1..."):
            full_text = generar_auditoria_loreal(target_market)
            st.markdown(full_text)
            
            # --- DASHBOARD ---
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                df_med = pd.DataFrame({"Canal": ["Digital", "TV", "OOH", "Retail Media"], "Inv": [45, 20, 15, 20]})
                st.plotly_chart(px.pie(df_med, values="Inv", names="Canal", hole=.4, title="Inversión Medios"), use_container_width=True)
            with c2:
                df_share = pd.DataFrame({"Marca": ["L'Oréal", "Belcorp", "Unilever", "Natura"], "Share": [28, 22, 18, 15]})
                st.plotly_chart(px.bar(df_share, x="Share", y="Marca", orientation='h', title="Market Share"), use_container_width=True)

            # EXPORTACIÓN
            doc = Document()
            doc.add_heading(f"Reporte L'Oréal - {target_market}", 0)
            doc.add_paragraph(full_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button("📄 Descargar Reporte (Word)", data=buffer.getvalue(), file_name=f"Loreal_{target_market}.docx")
