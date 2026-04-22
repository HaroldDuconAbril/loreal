import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from io import BytesIO
import pandas as pd

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="L'Oréal Colombia Deck", layout="wide")

st.title("💄 L'Oréal Colombia – Strategic Deck Generator")

# =============================
# FUNCIÓN CREAR PPT
# =============================
def crear_ppt_colombia():

    prs = Presentation()

    # =============================
    # SLIDE 1 - PORTADA
    # =============================
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = "L'Oréal Colombia"
    slide.placeholders[1].text = "Strategic Competitive Landscape"

    # =============================
    # SLIDE 2 - COMPETIDORES (CON LOGOS)
    # =============================
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.5))
    title_tf = title_box.text_frame
    title_tf.text = "MAIN COMPETITORS"

    logos = [
        ("logos/pg.png", 1),
        ("logos/unilever.png", 2),
        ("logos/natura.png", 3),
        ("logos/belcorp.png", 4),
        ("logos/quala.png", 5),
    ]

    left = 1
    for path, i in logos:
        slide.shapes.add_picture(path, Inches(left), Inches(1.2), height=Inches(1))
        left += 1.5

    # =============================
    # SLIDE 3 - MARCAS LOREAL
    # =============================
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

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
    p.text = "Lancôme, Kiehl’s, Yves Saint Laurent Beauty"
    p.level = 1

    # =============================
    # SLIDE 4 - INVERSIÓN (TABLA)
    # =============================
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)

    title = slide.shapes.title
    title.text = "Media Investment Colombia (Estimated)"

    rows, cols = 5, 4
    table = slide.shapes.add_table(rows, cols, Inches(1), Inches(2), Inches(8), Inches(3)).table

    headers = ["Empresa", "2022", "2023", "2024"]
    data = [
        ["L'Oréal", "120", "140", "160"],
        ["Unilever", "110", "130", "150"],
        ["P&G", "100", "120", "140"],
        ["Natura", "60", "70", "80"]
    ]

    for col in range(cols):
        table.cell(0, col).text = headers[col]

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
    slide.shapes.title.text = "Agencies & Ecosystem"

    tf = slide.placeholders[1].text_frame
    tf.text = "Media Agencies:"
    p = tf.add_paragraph()
    p.text = "Publicis Groupe (Zenith, Starcom)"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Creative Agencies:"
    p.level = 0

    p = tf.add_paragraph()
    p.text = "McCann, Wunderman Thompson"
    p.level = 1

    # =============================
    # SLIDE 7 - STAKEHOLDERS
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Key Stakeholders"

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
    p.text = "Caracol, RCN, Meta, Google"
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
if st.button("🚀 Generar Deck Colombia PRO"):
    ppt = crear_ppt_colombia()

    st.download_button(
        "📊 Descargar PowerPoint",
        ppt,
        file_name="Loreal_Colombia_Deck.pptx"
    )
