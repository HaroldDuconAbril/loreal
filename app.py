import streamlit as st
import os
from groq import Groq
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from io import BytesIO
from dotenv import load_dotenv

# =============================
# CONFIG
# =============================
load_dotenv()
st.set_page_config(page_title="IPG Strategic Deck - L'Oréal", layout="wide")

# =============================
# SIDEBAR
# =============================
st.sidebar.title("⚙️ Control Panel")

api_key = st.sidebar.text_input("Groq API Key", type="password") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Ingresa API Key")
    st.stop()

client = Groq(api_key=api_key)

modelo = st.sidebar.selectbox(
    "Modelo",
    ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
)

# =============================
# FUNCIÓN IA
# =============================
def generar_contenido(cliente):

    prompt = f"""
Eres consultor senior tipo McKinsey.

Genera una presentación ejecutiva para {cliente}.

FORMATO ESTRICTO:
Cada slide debe venir así:

[TITULO]
- bullet
- bullet
- bullet

SLIDES:

Overview Regional
Marcas por Mercado
Agencias (Medios y Creativas)
Competencia
Inversión en Medios
Data Clave de Marcas
Stakeholders
Conclusiones

Reglas:
- Máximo 5 bullets por slide
- Frases cortas
- Lenguaje ejecutivo
"""

    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# =============================
# PARSER TEXTO → SLIDES
# =============================
def parsear_slides(texto):
    slides = []
    bloques = texto.split("\n\n")

    for bloque in bloques:
        lineas = bloque.strip().split("\n")
        if len(lineas) > 1:
            titulo = lineas[0].strip()
            bullets = [l.replace("- ", "") for l in lineas[1:] if l.startswith("-")]
            slides.append((titulo, bullets))

    return slides

# =============================
# CREAR PPT PRO
# =============================
def crear_ppt_pro(slides, cliente):
    prs = Presentation()

    for titulo, bullets in slides:
        layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(layout)

        # TÍTULO
        title = slide.shapes.title
        title.text = titulo

        title.text_frame.paragraphs[0].font.size = Pt(32)
        title.text_frame.paragraphs[0].font.bold = True
        title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 70, 140)

        # CONTENIDO
        content = slide.placeholders[1].text_frame
        content.clear()

        for bullet in bullets:
            p = content.add_paragraph()
            p.text = bullet
            p.level = 0
            p.font.size = Pt(18)

    buffer = BytesIO()
    prs.save(buffer)
    buffer.seek(0)

    return buffer

# =============================
# UI
# =============================
st.title("💄 L'Oréal Strategic Deck Generator")
st.subheader("Nivel consultora (McKinsey style)")

cliente = st.text_input("Cliente:", "L'Oréal LATAM")

if st.button("🚀 Generar Deck"):

    with st.spinner("Construyendo presentación ejecutiva..."):

        texto = generar_contenido(cliente)

        slides = parsear_slides(texto)

        ppt = crear_ppt_pro(slides, cliente)

        st.success("Deck generado ✅")

        st.download_button(
            "📊 Descargar PowerPoint",
            ppt,
            file_name=f"{cliente}_Deck_Estrategico.pptx"
        )
