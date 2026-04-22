import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from io import BytesIO
import requests

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="L'Oréal Colombia Deck", layout="wide")

st.title("💄 L'Oréal Colombia – Strategic Deck Generator")

# =============================
# FUNCIÓN DESCARGAR IMAGEN URL
# =============================
def cargar_imagen(url):
    response = requests.get(url)
    return BytesIO(response.content)

# =============================
# CREAR PPT
# =============================
def crear_ppt_colombia():

    prs = Presentation()

    # =============================
    # SLIDE 1 - PORTADA
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "L'Oréal Colombia"
    slide.placeholders[1].text = "Strategic Competitive Landscape"

    # =============================
    # SLIDE 2 - COMPETIDORES (LOGOS)
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.5))
    title_tf = title_box.text_frame
    title_tf.text = "MAIN COMPETITORS"

    logos = [
        "https://logo.clearbit.com/pg.com",
        "https://logo.clearbit.com/unilever.com",
        "https://logo.clearbit.com/natura.com",
        "https://logo.clearbit.com/belcorp.biz",
        "https://logo.clearbit.com/quala.com.co"
    ]

    left = 1
    for url in logos:
        try:
            img = cargar_imagen(url)
            slide.shapes.add_picture(img, Inches(left), Inches(1.2), width=Inches(1.2))
            left += 1.5
        except:
            continue

    # =============================
    # SLIDE 3 - MARCAS LOREAL
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "L'Oréal Brands in Colombia"

    tf = slide.placeholders[1].text_frame
    tf.text = "Mass Market:"
    p = tf.add_paragraph()
    p.text = "L'Oréal Paris, Garnier, Maybelline"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Dermocosmetics:"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "La Roche-Posay, Vichy, CeraVe"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Luxury:"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "Lancôme, Kiehl’s, YSL Beauty"
    p.level = 1

    # =============================
    # SLIDE 4 - INVERSIÓN
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Media Investment Colombia (USD MM)"

    table = slide.shapes.add_table(5, 4, Inches(1), Inches(2), Inches(8), Inches(3)).table

    headers = ["Empresa", "2022", "2023", "2024"]
    data = [
        ["L'Oréal", "120", "140", "160"],
        ["Unilever", "110", "130", "150"],
        ["P&G", "100", "120", "140"],
        ["Natura", "60", "70", "80"]
    ]

    for i, h in enumerate(headers):
        table.cell(0, i).text = h

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            table.cell(i+1, j).text = val

    # =============================
    # SLIDE 5 - MEDIA MIX
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Media Mix Colombia"

    table = slide.shapes.add_table(6, 3, Inches(1), Inches(2), Inches(8), Inches(3)).table

    headers = ["Canal", "2023", "2024"]
    data = [
        ["Digital", "45%", "55%"],
        ["TV", "30%", "25%"],
        ["OOH", "10%", "8%"],
        ["Retail Media", "10%", "12%"],
        ["Radio", "5%", "5%"]
    ]

    for i, h in enumerate(headers):
        table.cell(0, i).text = h

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            table.cell(i+1, j).text = val

    # =============================
    # SLIDE 6 - AGENCIAS
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Agencies"

    tf = slide.placeholders[1].text_frame
    tf.text = "Media:"
    p = tf.add_paragraph()
    p.text = "Publicis Groupe (Zenith, Starcom)"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Creative:"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "McCann, WPP"
    p.level = 1

    # =============================
    # SLIDE 7 - STAKEHOLDERS
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Stakeholders"

    tf = slide.placeholders[1].text_frame
    tf.text = "Retail:"
    p = tf.add_paragraph()
    p.text = "Éxito, Falabella, Farmatodo"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "E-commerce:"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "Mercado Libre, Amazon"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Media:"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "Caracol, RCN, Google, Meta"
    p.level = 1

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
if st.button("🚀 Generar Deck PRO Colombia"):
    ppt = crear_ppt_colombia()

    st.download_button(
        "📊 Descargar PowerPoint",
        ppt,
        file_name="Loreal_Colombia_Deck.pptx"
    )
