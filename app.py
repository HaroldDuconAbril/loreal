import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from io import BytesIO
import requests

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="L'Oréal Colombia PRO", layout="wide")

st.title("💄 L'Oréal Colombia – Competitive Landscape PRO")

# =============================
# DESCARGAR LOGOS
# =============================
def cargar_imagen(url):
    try:
        r = requests.get(url)
        return BytesIO(r.content)
    except:
        return None

# =============================
# CREAR CAJA CATEGORÍA
# =============================
def crear_categoria(slide, titulo, left, logos):

    # Título categoría
    box = slide.shapes.add_textbox(Inches(left), Inches(1), Inches(3), Inches(0.4))
    tf = box.text_frame
    tf.text = titulo.upper()
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.bold = True

    # Caja contenedora
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left),
        Inches(1.5),
        Inches(3),
        Inches(3)
    )

    shape.fill.background()
    shape.line.color.rgb = RGBColor(180, 180, 180)

    # Logos dentro
    x = left + 0.3
    y = 1.8

    for logo in logos:
        img = cargar_imagen(logo)
        if img:
            slide.shapes.add_picture(img, Inches(x), Inches(y), width=Inches(0.9))
            x += 1

# =============================
# CREAR PPT
# =============================
def crear_ppt():

    prs = Presentation()

    # =============================
    # SLIDE PRINCIPAL
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Título
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.5))
    tf = title.text_frame
    tf.text = "L’Oréal – Competitive Landscape (Colombia)"
    tf.paragraphs[0].font.size = Pt(28)
    tf.paragraphs[0].font.bold = True

    # Subcategorías
    crear_categoria(
        slide,
        "Haircare",
        0.5,
        [
            "https://logo.clearbit.com/pg.com",
            "https://logo.clearbit.com/unilever.com"
        ]
    )

    crear_categoria(
        slide,
        "Skincare",
        3.7,
        [
            "https://logo.clearbit.com/unilever.com",
            "https://logo.clearbit.com/natura.com"
        ]
    )

    crear_categoria(
        slide,
        "Makeup",
        6.9,
        [
            "https://logo.clearbit.com/belcorp.biz",
            "https://logo.clearbit.com/oboticario.com.br"
        ]
    )

    # =============================
    # EXPORTAR
    # =============================
    buffer = BytesIO()
    prs.save(buffer)
    buffer.seek(0)

    return buffer

# =============================
# BOTÓN
# =============================
if st.button("🚀 Generar Slide PRO"):

    ppt = crear_ppt()

    st.download_button(
        "📊 Descargar PPT",
        ppt,
        file_name="competitive_landscape_colombia.pptx"
    )
