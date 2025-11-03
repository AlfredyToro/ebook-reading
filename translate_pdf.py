import os
from googletrans import Translator
import fitz  # PyMuPDF
from fpdf import FPDF

# Extraer texto de un rango de páginas
def extract_text_from_pdf(pdf_path, start_page, end_page):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(start_page, end_page + 1):
        if page_num < doc.page_count:
            page = doc.load_page(page_num)
            text += page.get_text()
    return text

# Traducir texto con Google Translate
def translate_text(text, target_language="es"):
    translator = Translator()
    
    # Dividir el texto si es muy largo (límite de seguridad: 4000 caracteres)
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    translated_chunks = []
    for chunk in chunks:
        translated = translator.translate(chunk, dest=target_language)
        translated_chunks.append(translated.text)
    
    return "\n".join(translated_chunks)

# Crear PDF con el texto traducido
def create_pdf_from_text(text, output_path):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Reemplaza caracteres no compatibles con latin-1
    def safe_line(line):
        return line.encode("latin-1", "replace").decode("latin-1")

    lines = text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, safe_line(line))

    try:
        pdf.output(output_path)
        print(f"✅ PDF generado correctamente en: {output_path}")
    except Exception as e:
            print(f"[Línea {i+1}] Error al traducir: {e}")
            print(f"Contenido problemático: {repr(line)}")
            translated_pairs.append((line, "[Error de traducción]"))

# Función principal
def main():
    pdf_path = "redwarn.pdf"
    output_pdf_path = "translated_output.pdf"

    # 📝 Cambia estas páginas según lo que quieras traducir
    start_page = 92  # Página 2 (índice base 0)
    end_page = 432    # Página 4 (índice base 0)

    print(f"Traduciendo páginas {start_page + 1} a {end_page + 1}...")

    # 1. Extraer texto
    extracted_text = extract_text_from_pdf(pdf_path, start_page, end_page)

    # 2. Traducir texto
    translated_text = translate_text(extracted_text)

    # 3. Crear nuevo PDF
    create_pdf_from_text(translated_text, output_pdf_path)

    print(f"✅ Traducción completada. Archivo guardado como: {output_pdf_path}")

if __name__ == "__main__":
    main()
