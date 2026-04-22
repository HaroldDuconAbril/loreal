import streamlit as st
import os
import pandas as pd
import plotly.express as px
from docx import Document
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

# CONFIG
load_dotenv()
st.set_page_config(page_title="L'Oréal Master Intelligence 2026 - IPG", layout="wide")

# UI STYLE
st.markdown("""
<style>
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #ffffff; color: #000000;
    text-align: center; padding: 12px; font-weight: bold;
    border-top: 3px solid #d32f2f; z-index: 100;
}
</style>
<div class="footer">🚀 L'Oréal Strategic Media Intelligence 2026</div>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("⚙️ IPG Control Panel")

api_key_input = st.sidebar.text_input("Gemini API Key:", type="password")
api_key = api_key_input if api_key_input else os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key requerida.")

# MODELOS ACTUALIZADOS
model_choice = st.sidebar.selectbox(
    "Motor de Inteligencia:",
    ["Gemini Flash (rápido)", "Gemini Pro (potente)"]
)

def get_model_id(choice):
    if "Flash" in choice:
        return "gemini-1.5-flash"  # estable
    else:
        return "gemini-2.0-flash"  # reemplazo moderno de Pro

# FUNCIÓN PRINCIPAL
def generar_auditoria_maestra(cliente, modo):
    try:
        model_id = get_model_id(modo)
        model = genai.GenerativeModel(model_id)

        prompt = f"""
Eres un Director Senior de Research en Colombia.

Genera una AUDITORÍA ESTRATÉGICA PROFUNDA para {cliente}:

1. PORTAFOLIO Y MARCAS
2. INVERSIÓN EN MEDIOS
3. ECOSISTEMA DE AGENCIAS
4. COMPETENCIA
5. SENTIMIENTO SOCIAL
6. STAKEHOLDERS

Incluye tablas, análisis y conclusiones claras.
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 4096
            }
        )

        return response.text

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# UI
st.title("💄 Auditoría 360°: L'Oréal Colombia")

cliente = st.text_input("Marca o división:", "L'Oréal Groupe")

if st.button("🚀 Generar Auditoría"):
    if not api_key:
        st.error("Falta API Key")
    else:
        with st.spinner("Analizando..."):
            resultado = generar_auditoria_maestra(cliente, model_choice)
            st.markdown(resultado)

            # DASHBOARD
            st.subheader("📊 Market Share")

            df = pd.DataFrame({
                "Marca": ["L'Oréal", "Belcorp", "Unilever", "Natura"],
                "Share": [28, 22, 18, 15]
            })

            fig = px.bar(df, x="Marca", y="Share")
            st.plotly_chart(fig, use_container_width=True)

            # EXPORT WORD
            doc = Document()
            doc.add_heading(f"Auditoría {cliente}", 0)
            doc.add_paragraph(resultado)

            buffer = BytesIO()
            doc.save(buffer)

            st.download_button(
                "📄 Descargar Word",
                data=buffer.getvalue(),
                file_name="reporte.docx"
            )
