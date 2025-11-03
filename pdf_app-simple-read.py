import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(layout="wide")

st.title("📖 Lector de PDF Interactivo")

uploaded_file = st.file_uploader("Carga tu PDF en inglés", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    st.markdown("### Contenido del libro:")
    st.markdown(
        f"<div style='white-space: pre-wrap; font-size: 18px;'>{full_text}</div>",
        unsafe_allow_html=True
    )
