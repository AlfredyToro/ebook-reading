import os
from googletrans import Translator
import fitz  # PyMuPDF
from fpdf import FPDF
import time

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
def translate_lines(text):
    translator = Translator()
    lines = text.split("\n")
    translated_pairs = []

    for i, line in enumerate(lines):
        line = line.strip()

        # Saltar líneas vacías
        if not line:
            continue

        # Limitar longitud por si acaso (opcional)
        if len(line) > 1000:
            line = line[:1000] + " [...]"

        try:
            result = translator.translate(line, src='en', dest='es')

            # Manejar posibles respuestas vacías
            if result and result.text:
                translated = result.text
            else:
                translated = "[Sin traducción]"

            translated_pairs.append((line, translated))
            time.sleep(0.5)  # Espera para no saturar
        except Exception as e:
            print(f"[Línea {i+1}] Error al traducir: {e}")
            print(f"Contenido problemático: {repr(line)}")
            translated_pairs.append((line, "[Error de traducción]"))

    return translated_pairs

# Crear PDF con el texto traducido
def create_dual_language_pdf(pairs, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    def safe_line(line):
        return line.encode("latin-1", "replace").decode("latin-1")

    for i, (original, translated) in enumerate(pairs):
        try:
            # Línea en inglés (negro)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, safe_line(original))

            # Línea traducida en español (rojo)
            pdf.set_text_color(255, 0, 0)
            pdf.multi_cell(0, 10, safe_line(translated))

            pdf.ln(2)
        except Exception as e:
            print(f"[PDF] Error en línea {i+1}: {e}")
            continue

    try:
        pdf.output(output_path)
        print(f"✅ PDF bilingüe generado correctamente en: {output_path}")
    except Exception as e:
        print(f"❌ Error al guardar el PDF: {e}")

# Función principal
def main():
    pdf_path = "redwarning2_removed.pdf"
    output_pdf_path = "translated_output.pdf"

    # 📝 Cambia estas páginas según lo que quieras traducir
    start_page = 115  # Página 2 (índice base 0)
    end_page = 130    # Página 4 (índice base 0)

    print(f"Traduciendo páginas {start_page + 1} a {end_page + 1}...")

    # 1. Extraer texto
    extracted_text = extract_text_from_pdf(pdf_path, start_page, end_page)
    print(f"📏 Caracteres a traducir: {len(extracted_text)}")

    # 2. Traducir texto
    translated_pairs = translate_lines(extracted_text)

    # 3. Crear nuevo PDF
    create_dual_language_pdf(translated_pairs, output_pdf_path)
    print(f"✅ Traducción completada. Archivo guardado como: {output_pdf_path}")

if __name__ == "__main__":
    main()
