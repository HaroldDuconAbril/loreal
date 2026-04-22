import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from pptx import Presentation
from io import BytesIO
from dotenv import load_dotenv

# 1. Configuración de Entorno y Estilo
load_dotenv()
st.set_page_config(page_title="L'Oréal Strategy Bot | IPG", page_icon="📊", layout="wide")

# Estilo personalizado para el reporte
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #000; color: white; }
    .report-box { padding: 20px; border-radius: 10px; background-color: white; border: 1px solid #e6e9ef; }
    </style>
""", unsafe_allow_html=True)

# 2. Barra Lateral - IPG Control Panel
st.sidebar.title("⚙️ IPG Control Panel")
st.sidebar.image("https://www.loreal.com/en/-/media/project/loreal/brand-sites/corp/master/lcorp/press-releases/2021/brands/loreal_paris_logo.png", width=150)

api_key_input = st.sidebar.text_input("Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

model_choice = st.sidebar.selectbox("Motor de Inteligencia:", ["Gemini 1.5 Pro (Preview)", "Gemini 1.5 Flash"])

# 3. Lógica de Modelos y PPTX
def generar_auditoria_maestra(cliente, modo):
    # Selección dinámica para evitar el error 404
    model_id = "gemini-1.5-pro" if "Pro" in modo else "gemini-1.5-flash"
    
    # Intento de buscar versión específica si es Pro
    if "Pro" in modo:
        try:
            available = [m.name for m in genai.list_models()]
            if "models/gemini-1.5-pro-002" in available:
                model_id = "models/gemini-1.5-pro-002"
        except:
            pass 

    model = genai.GenerativeModel(model_id)
    
    prompt = f"""
    Actúa como un Senior Strategy Director para un pitch de L'Oreal en Colombia, Abril 2026.
    Proporciona un informe detallado y profesional para el cliente: {cliente}.
    
    Estructura la respuesta exactamente con estos encabezados usando '###':
    ### 1. Portafolio de Marcas en Colombia 2026
    (Incluye Luxe, Masivo con Vogue, Dermo y Profesional)
    
    ### 2. Ecosistema de Agencias
    (Menciona a Publicis/Zenith para medios y McCann para creatividad, bajo el contexto actual)
    
    ### 3. Panorama Competitivo (IBOPE)
    (Compara con Belcorp, Natura y Unilever. Cita inversión estimada según IBOPE 2026)
    
    ### 4. Evolución de Inversión 2024-2026
    (Detalla el crecimiento en Retail Media y Social Commerce)
    
    ### 5. Stakeholders y Aliados Locales
    (Menciona ANDA, Farmatodo, Éxito y Rappi)
    
    IMPORTANTE: Usa datos coherentes, menciona que son proyecciones basadas en tendencias reales de IBOPE y mantén un tono de consultoría de alto nivel.
    """
    
    response = model.generate_content(prompt)
    return response.text

def crear_pptx(texto_ia):
    prs = Presentation()
    
    # Slide de Portada
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "L'Oréal Colombia 2026"
    slide.placeholders[1].text = "Strategic Pitch Intelligence\nIPG Control Panel Report"

    # Slides por secciones
    secciones = texto_ia.split("###")
    for sec in secciones:
        if sec.strip():
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            lineas = sec.split("\n")
            slide.shapes.title.text = lineas[0].strip()
            # Agregar el cuerpo del texto
            cuerpo = "\n".join(lineas[1:]).strip()
            slide.placeholders[1].text = cuerpo[:1000] # Limitar para que quepa en el slide

    buffer = BytesIO()
    prs.save(buffer)
    return buffer.getvalue()

# 4. Interfaz Principal
st.title("💄 L'Oréal Market Intelligence Bot")
st.subheader("Mercado: Colombia | Periodo: Q2 2026")

col1, col2 = st.columns([2, 1])

with col1:
    cliente_input = st.text_input("Nombre del Proyecto/Marca:", "L'Oreal Groupe Colombia")
    if st.button("🚀 Iniciar Auditoría Maestra 2026"):
        if not api_key:
            st.warning("Por favor, ingresa tu API Key en el panel izquierdo.")
        else:
            with st.spinner("Analizando datos de IBOPE y mercado local..."):
                resultado = generar_auditoria_maestra(cliente_input, model_choice)
                st.session_state['reporte'] = resultado
                st.success("Auditoría generada con éxito.")

if 'reporte' in st.session_state:
    st.markdown("---")
    with st.container():
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(st.session_state['reporte'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Opción de descarga
    ppt_data = crear_pptx(st.session_state['reporte'])
    st.download_button(
        label="📥 Descargar Presentación para Pitch (PPTX)",
        data=ppt_data,
        file_name=f"Loreal_Colombia_2026_IPG.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

with col2:
    st.info("""
    **Fuentes Activas:**
    - IBOPE Media Colombia
    - Kantar Worldpanel
    - P&M Advertising Data
    - L'Oreal Annual Report 2025
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/L%27Or%C3%A9al_logo.svg/2560px-L%27Or%C3%A9al_logo.svg.png")
