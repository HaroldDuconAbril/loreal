import streamlit as st
import google.generativeai as genai
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from io import BytesIO
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Gemini
# Nota: En Streamlit Cloud, usa st.secrets["GOOGLE_API_KEY"]
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-pro-preview-0409')

# --- FUNCIONES DE APOYO ---
def create_pptx(data_dict):
    prs = Presentation()
    
    # Slide de Portada
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = f"Análisis Estratégico: L'Oréal Colombia 2026"
    slide.placeholders[1].text = "Market Intelligence & Media Landscape"

    # Slide de Datos
    for key, value in data_dict.items():
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = key
        content = slide.placeholders[1]
        content.text = value

    binary_output = BytesIO()
    prs.save(binary_output)
    return binary_output.getvalue()

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="L'Oréal AI Intelligence", page_icon="✨", layout="wide")

st.title("🤖 L'Oréal Strategy Bot - Colombia 2026")
st.markdown("---")

with st.sidebar:
    st.header("Configuración")
    target_market = st.selectbox("Mercado", ["Colombia", "México", "Chile"])
    st.info("Fuente principal de pauta: IBOPE / Kantar Media 2026")

# Prompt Principal
prompt_base = f"""
Actúa como un experto en Media Planning y Business Intelligence para el mercado de {target_market}. 
Estamos en abril de 2026. Necesito datos reales y verificables para un pitch de L'Oreal.
Responde con detalle sobre:
1. Marcas presentes (Luxe, Mass, Active, Professional).
2. Agencias actuales (Media & Creative).
3. Competidores top (enfocado en Belcorp, Natura, Unilever).
4. Evolución inversión medios 2024-2026 (datos tipo IBOPE).
5. Stakeholders locales clave.

IMPORTANTE: Cita las fuentes como IBOPE, P&M, o la ANDA.
"""

if st.button("Generar Reporte de Inteligencia"):
    with st.spinner("Consultando fuentes de mercado 2026..."):
        try:
            response = model.generate_content(prompt_base)
            content = response.text
            
            # Mostrar en Pantalla
            st.markdown(content)
            
            # Preparar descarga de PPTX (Simulación de parseo simple)
            sections = content.split("###")
            data_for_ppt = { f"Sección {i}": s for i, s in enumerate(sections) if s.strip() }
            
            pptx_data = create_pptx(data_for_ppt)
            
            st.download_button(
                label="⬇️ Descargar Presentación PPTX",
                data=pptx_data,
                file_name=f"Loreal_Colombia_2026.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")

st.markdown("---")
st.caption("Harold Ducon v1.0 | Datos proyectados a 2026 basados en tendencias de mercado.")
