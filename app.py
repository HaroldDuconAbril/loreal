import streamlit as st
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from io import BytesIO
import requests
from pytrends.request import TrendReq
from groq import Groq

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="L'Oréal PRO Intelligence", layout="wide")

GROQ_API_KEY = st.sidebar.text_input("Groq API Key", type="password")

# =============================
# FUNCIONES
# =============================
def cargar_imagen(url):
    try:
        r = requests.get(url)
        return BytesIO(r.content)
    except:
        return None

def agregar_fuente(slide, texto):
    caja = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.3))
    tf = caja.text_frame
    tf.text = texto
    tf.paragraphs[0].font.size = Pt(8)

# =============================
# GOOGLE TRENDS REAL
# =============================
def obtener_trends():
    pytrends = TrendReq()
    kw = ["Loreal", "Maybelline", "CeraVe", "Natura"]
    pytrends.build_payload(kw, geo="CO")
    df = pytrends.interest_over_time()
    return df.tail(12)

# =============================
# IA INSIGHTS
# =============================
def generar_insights(data_text):
    if not GROQ_API_KEY:
        return "Configura API para insights"

    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
    Analiza estos datos y dame 3 insights estratégicos ejecutivos:
    {data_text}
    """

    res = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )

    return res.choices[0].message.content

# =============================
# CREAR DECK
# =============================
def crear_deck():

    prs = Presentation()

    # =============================
    # PORTADA
    # =============================
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "L’Oréal Colombia"
    slide.placeholders[1].text = "Market Intelligence – Data Driven"

    # =============================
    # INVERSIÓN (EXCEL REAL)
    # =============================
    df_inv = pd.read_excel("data/inversion_medios.xlsx")

    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Media Investment"

    table = slide.shapes.add_table(len(df_inv)+1, len(df_inv.columns),
                                   Inches(1), Inches(2), Inches(8), Inches(3)).table

    for j, col in enumerate(df_inv.columns):
        table.cell(0, j).text = col

    for i, row in df_inv.iterrows():
        for j, val in enumerate(row):
            table.cell(i+1, j).text = str(val)

    agregar_fuente(slide, "Fuente: Kantar IBOPE Media / Datos internos")

    # =============================
    # GOOGLE TRENDS
    # =============================
    df_trends = obtener_trends()

    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Search Trends Colombia"

    tf = slide.placeholders[1].text_frame
    tf.text = df_trends.to_string()

    agregar_fuente(slide, "Fuente: Google Trends (Colombia)")

    # =============================
    # INSIGHTS IA
    # =============================
    insights = generar_insights(df_inv.to_string())

    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Key Insights"

    tf = slide.placeholders[1].text_frame
    tf.text = insights

    agregar_fuente(slide, "Fuente: AI Analysis + Data Inputs")

    # =============================
    # EXPORTAR
    # =============================
    buffer = BytesIO()
    prs.save(buffer)
    buffer.seek(0)

    return buffer

# =============================
# UI
# =============================
st.title("💼 L'Oréal Colombia – PRO Intelligence Engine")

if st.button("🚀 Generar Deck PRO REAL"):
    ppt = crear_deck()

    st.download_button(
        "📊 Descargar PPT",
        ppt,
        file_name="Loreal_PRO_REAL.pptx"
    )
