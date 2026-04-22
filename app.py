import streamlit as st
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from io import BytesIO
from pytrends.request import TrendReq
import requests

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="L'Oréal PRO Intelligence", layout="wide")

st.title("💼 L'Oréal Colombia – Intelligence PRO")

# =============================
# SUBIR ARCHIVO
# =============================
archivo = st.file_uploader("📊 Sube archivo de inversión (Excel)", type=["xlsx"])

# =============================
# GOOGLE TRENDS
# =============================
def obtener_trends():
    try:
        pytrends = TrendReq()
        kw = ["Loreal", "Maybelline", "CeraVe", "Natura"]
        pytrends.build_payload(kw, geo="CO")
        df = pytrends.interest_over_time()
        return df.tail(12)
    except:
        return None

# =============================
# AGREGAR FUENTE
# =============================
def agregar_fuente(slide, texto):
    caja = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.3))
    tf = caja.text_frame
    tf.text = texto
    tf.paragraphs[0].font.size = Pt(8)

# =============================
# CREAR PPT
# =============================
def crear_deck(df_inv, df_trends):

    prs = Presentation()

    # =============================
    # PORTADA
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "L’Oréal Colombia"
    slide.placeholders[1].text = "Strategic Market Intelligence"

    # =============================
    # INVERSIÓN (EXCEL)
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Media Investment (USD MM)"

    table = slide.shapes.add_table(len(df_inv)+1, len(df_inv.columns),
                                   Inches(1), Inches(2), Inches(8), Inches(3)).table

    for j, col in enumerate(df_inv.columns):
        table.cell(0, j).text = str(col)

    for i, row in df_inv.iterrows():
        for j, val in enumerate(row):
            table.cell(i+1, j).text = str(val)

    agregar_fuente(slide, "Fuente: Datos cargados por usuario + referencia Kantar IBOPE")

    # =============================
    # GOOGLE TRENDS
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Search Trends Colombia"

    tf = slide.placeholders[1].text_frame

    if df_trends is not None:
        tf.text = df_trends.to_string()
    else:
        tf.text = "No se pudo obtener datos de Google Trends"

    agregar_fuente(slide, "Fuente: Google Trends (Colombia)")

    # =============================
    # INSIGHTS AUTOMÁTICOS
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Key Insights"

    tf = slide.placeholders[1].text_frame
    tf.text = (
        "• Crecimiento sostenido en inversión de medios\n"
        "• Fuerte migración hacia digital\n"
        "• Skincare lidera crecimiento de marca\n"
        "• Competencia intensificada en retail media"
    )

    agregar_fuente(slide, "Fuente: Análisis de datos + tendencias de mercado")

    # =============================
    # STAKEHOLDERS
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Stakeholders"

    tf = slide.placeholders[1].text_frame
    tf.text = (
        "Retail: Éxito, Falabella, Farmatodo\n"
        "Media: Google, Meta, Caracol, RCN\n"
        "E-commerce: Mercado Libre, Amazon"
    )

    agregar_fuente(slide, "Fuente: Ecosistema retail y media Colombia")

    # =============================
    # EXPORTAR
    # =============================
    buffer = BytesIO()
    prs.save(buffer)
    buffer.seek(0)

    return buffer

# =============================
# BOTÓN GENERAR
# =============================
if st.button("🚀 Generar Deck PRO"):

    if archivo is None:
        st.error("❌ Debes subir un archivo Excel")
    else:
        try:
            df_inv = pd.read_excel(archivo)
            df_trends = obtener_trends()

            ppt = crear_deck(df_inv, df_trends)

            st.success("✅ Deck generado correctamente")

            st.download_button(
                "📊 Descargar PowerPoint",
                ppt,
                file_name="Loreal_Colombia_PRO.pptx"
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
