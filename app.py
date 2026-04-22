import streamlit as st
import google.generativeai as genai
import os
from pptx import Presentation
from io import BytesIO
from dotenv import load_dotenv

# 1. Configuración de Entorno y Estilo
load_dotenv()
st.set_page_config(page_title="L'Oréal Strategy Bot | IPG", page_icon="📊", layout="wide")

# Estilo profesional para la interfaz
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

# Gestión de API Key
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password", help="Pega tu API Key de Google AI Studio")
api_key = api_key_input if api_key_input else os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida para funcionar.")

# Selección de Modelo (Nombres estables para evitar 404)
model_choice = st.sidebar.selectbox(
    "Motor de Inteligencia:", 
    ["Gemini 1.5 Pro (Recomendado)", "Gemini 1.5 Flash (Más rápido)"]
)

# 3. Lógica de Negocio
def generar_auditoria_maestra(cliente, modo):
    # Usar alias estables de producción
    model_id = "gemini-1.5-pro" if "Pro" in modo else "gemini-1.5-flash"
    
    try:
        model = genai.GenerativeModel(model_id)
        
        prompt = f"""
        Actúa como un Senior Strategy Director para un pitch de L'Oreal en Colombia, Abril 2026.
        Genera un informe estratégico de alto nivel para el cliente: {cliente}.
        
        Responde detalladamente usando estos encabezados con '###':
        ### 1. Portafolio de Marcas en Colombia 2026
        (Analiza Luxe, Masivo con Vogue, Dermo y Profesional)
        
        ### 2. Ecosistema de Agencias (Medios y Creatividad)
        (Menciona el rol de Publicis/Zenith y McCann en el mercado colombiano actual)
        
        ### 3. Competidores y Participación de Mercado
        (Compara con Belcorp, Natura y Unilever. Cita proyecciones de IBOPE 2026)
        
        ### 4. Evolución de la Inversión en Medios
        (Tendencias de Retail Media, TikTok Shop y pauta tradicional en Colombia)
        
        ### 5. Stakeholders Locales y Alianzas
        (Relación con ANDA, Farmatodo, Éxito y Rappi)
        
        IMPORTANTE: Cita fuentes verificables como IBOPE, Kantar y P&M. Tono profesional y ejecutivo.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error al conectar con la IA: {str(e)}"

def crear_pptx(texto_ia):
    prs = Presentation()
    
    # Slide 1: Portada
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "L'Oréal Colombia 2026"
    slide.placeholders[1].text = "Análisis de Inteligencia de Mercado\nIPG Strategic Support Tool"

    # Dividir texto por secciones para los slides
    secciones = texto_ia.split("###")
    for sec in secciones:
        if len(sec.strip()) > 10:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            lineas = sec.strip().split("\n")
            slide.shapes.title.text = lineas[0].replace("#", "").strip()
            
            cuerpo = "\n".join(lineas[1:]).strip()
            body_shape = slide.placeholders[1]
            body_shape.text = cuerpo[:1200] # Evitar que el texto se salga del slide

    buffer = BytesIO()
    prs.save(buffer)
    return buffer.getvalue()

# 4. Interfaz Principal (Main UI)
st.title("🚀 L'Oréal Market Intelligence")
st.markdown("Generador de insights estratégicos para el mercado colombiano (Proyección 2026).")

col1, col2 = st.columns([3, 1])

with col1:
    cliente_input = st.text_input("Nombre de la marca o proyecto:", "L'Oréal Groupe Colombia")
    
    if st.button("Generar Reporte y Diapositivas"):
        if not api_key:
            st.error("Debes configurar la API Key en la barra lateral.")
        else:
            with st.spinner("Consultando tendencias 2026 y datos de IBOPE..."):
                resultado = generar_auditoria_maestra(cliente_input, model_choice)
                st.session_state['reporte_final'] = resultado

    if 'reporte_final' in st.session_state:
        st.markdown("---")
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(st.session_state['reporte_final'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generación de descarga de PPTX
        with st.sidebar:
            st.success("✅ Reporte Generado")
            ppt_file = crear_pptx(st.session_state['reporte_final'])
            st.download_button(
                label="📥 Descargar PowerPoint",
                data=ppt_file,
                file_name=f"Estrategia_Loreal_2026.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

with col2:
    st.info("**Contexto de Mercado:**")
    st.write("- **Líder Local:** Vogue Cosméticos")
    st.write("- **Canal Clave:** Farmatodo / Éxito")
    st.write("- **Medición:** IBOPE / Kantar")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/L%27Or%C3%A9al_logo.svg/1200px-L%27Or%C3%A9al_logo.svg.png")

st.divider()
st.caption("Harold Ducon v2.0 | IA Engine: Google Gemini 1.5 Series")
