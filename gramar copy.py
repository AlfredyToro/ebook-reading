import streamlit as st
from googletrans import Translator
import difflib

translator = Translator()

st.title("🔤 Corrector con Google Translate")
input_text = st.text_area("Escribe tu texto en inglés:")

if st.button("🔍 Validar texto"):
    if input_text.strip():
        # Traducción a español y de vuelta a inglés
        translated = translator.translate(input_text, dest='es').text
        back_translated = translator.translate(translated, dest='en').text

        st.subheader("Texto corregido:")
        st.write(back_translated)

        st.subheader("Diferencias:")
        diff = difflib.ndiff(input_text.split(), back_translated.split())
        st.markdown(" ".join([
            f"~~{word[2:]}~~" if word.startswith("- ") else
            f"**{word[2:]}**" if word.startswith("+ ") else word[2:]
            for word in diff if not word.startswith("? ")
        ]))
    else:
        st.warning("⚠️ Por favor, escribe algo antes de validar.")
