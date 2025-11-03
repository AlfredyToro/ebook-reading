import streamlit as st
import fitz
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("📖 Lector PDF con Traducción Instantánea por Clic")

uploaded_file = st.file_uploader("Carga tu PDF en inglés", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        for b in blocks:
            text += b[4] + " "

    words = text.split()
    html_words = ""
    for word in words:
        html_words += f"<span class='word'>{word}</span> "

    html_code = f"""
    <style>
    .word {{
        cursor: pointer;
        padding: 2px 4px;
        display: inline-block;
    }}
    .word:hover {{
        background-color: #dbeafe;
    }}
    #tooltip {{
        position: absolute;
        display: none;
        background-color: #333;
        color: #fff;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 14px;
        max-width: 250px;
        z-index: 9999;
        pointer-events: none;
    }}
    </style>
    <div id="text-container" style="line-height: 1.8; font-size: 18px;">
        {html_words}
        <div id="tooltip"></div>
    </div>
    <script>
    const tooltip = window.parent.document.getElementById('tooltip') || document.getElementById('tooltip');
    document.querySelectorAll('.word').forEach(wordEl => {{
        wordEl.addEventListener('click', async () => {{
            const word = wordEl.innerText;
            const rect = wordEl.getBoundingClientRect();
            try {{
                const res = await fetch("https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + encodeURIComponent(word));
                const data = await res.json();
                const translated = data[0][0][0];
                tooltip.innerText = translated;
                tooltip.style.left = (rect.left + window.scrollX + rect.width / 2) + 'px';
                tooltip.style.top = (rect.top + window.scrollY - 40) + 'px';
                tooltip.style.display = 'block';
            }} catch (err) {{
                tooltip.innerText = "Error al traducir";
                tooltip.style.display = 'block';
            }}
        }});
    }});
    </script>
    """

    components.html(html_code, height=600, scrolling=True)
