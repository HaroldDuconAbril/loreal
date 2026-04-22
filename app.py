import streamlit as st
import google.generativeai as genai
import os
from pptx import Presentation
from io import BytesIO
from dotenv import load_dotenv

# 1. Configuración de Entorno y Estilo
load_dotenv()
st.set_page_config(page_title="L'Oréal Strategy Bot | IPG", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #000; color: white; font-weight: bold; }
    .report-box { padding: 25px; border-radius: 10px; background-color: white; border: 1px solid #e6e9ef; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# 2. Barra Lateral - IPG Control Panel
st.sidebar.title("⚙️ IPG Control Panel")
st.sidebar.markdown("---")

# Gestión de API Key (Prioriza Secrets de Streamlit o .env)
api_key = st.sidebar.text_input("Gemini API Key:", type="password")
if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

model_choice = st.sidebar.selectbox(
    "Motor de Inteligencia:", 
    ["Gemini 1.5 Flash (Más estable)", "Gemini 1.5 Pro (Alta complejidad)"]
)

# 3. Lógica de Negocio (Manejo de Errores 404)
def generar_auditoria_maestra(cliente, modo):
    # Intentamos con varios alias conocidos para evitar el 404 de Google
    if "Flash" in modo:
        model_names = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-1.5-flash-latest"]
    else:
        model_names = ["gemini-1.5-pro", "models/gemini-1.5-pro", "gemini-1.5-pro-latest"]
    
    success = False
    response_text = ""
    last_err = ""

    for m_name in model_names:
        try:
            model = genai.GenerativeModel(m_name)
            prompt = f"""
            Actúa como Senior Strategy Director para un pitch de L'Oreal en Colombia, Abril 2026.
            Genera un informe detallado para el cliente: {cliente}.
            
            Usa estos encabezados con '###':
            ### 1. Portafolio de Marcas en Colombia 2026
            ### 2. Ecosistema de Agencias (Publicis, McCann, etc.)
            ### 3. Panorama Competitivo (Belcorp, Natura, Unilever)
            ### 4. Evolución de Inversión 2024-2026 (Datos IBOPE)
            ### 5. Stakeholders Locales (ANDA, Farmatodo, Éxito)
            
            Cita fuentes reales y proyecciones coherentes. Tono profesional.
            """
            response = model.generate_content(prompt)
            response_text = response.text
            success = True
            break # Si funciona, salimos del bucle
        except Exception as e:
            last_err = str(e)
            continue

    if success:
        return response_text
    else:
        return f"❌ Error de conexión (404/Not Found). Google reporta: {last_err}. Sugerencia: Verifica que tu API Key tenga acceso a modelos 1.5 en Google AI Studio."

def crear_pptx(texto_ia):
    prs = Presentation()
    # Slide 1: Portada
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "L'Oréal Colombia 2026"
    slide.placeholders[1].text = "Market Intelligence Report\nPowered by IPG Strategy Bot"

    # Slides por secciones
    secciones = texto_ia.split("###")
    for sec in secciones:
        if len(sec.strip()) > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            lineas = sec.strip().split("\n")
            slide.shapes.title.text = lineas[0].replace("#", "").strip()
            slide.placeholders[1].text = "\n".join(lineas[1:]).strip()[:1000]

    buffer = BytesIO()
    prs.save(buffer)
    return buffer.getvalue()

# 4. Interfaz Principal
st.title("🚀 L'Oréal Market Intelligence")
st.markdown("Auditoría estratégica para el mercado colombiano (Abril 2026).")

cliente_input = st.text_input("Cliente/Proyecto:", "L'Oréal Groupe Colombia")

if st.button("Generar Auditoría 2026"):
    if not api_key:
        st.error("Configura la API Key.")
    else:
        with st.spinner("Conectando con servidores de Google AI..."):
            resultado = generar_auditoria_maestra(cliente_input, model_choice)
            st.session_state['reporte'] = resultado

if 'reporte' in st.session_state:
    st.markdown("---")
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(st.session_state['reporte'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if "❌ Error" not in st.session_state['reporte']:
        ppt_file = crear_pptx(st.session_state['reporte'])
        st.download_button(
            label="📥 Descargar PowerPoint",
            data=ppt_file,
            file_name="Estrategia_Loreal_2026.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
