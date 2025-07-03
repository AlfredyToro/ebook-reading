import streamlit as st
import fitz
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide")
st.title("📖 eBook")

pdf_path = "redwarning2_removed.pdf"

if os.path.exists(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        for b in blocks:
            text += b[4] + " "

    words = text.split()
    html_words = " ".join(f"<span class='word'>{word}</span>" for word in words)

    RAPIDAPI_KEY = "7366b97a9emshcadc1ea093c5332p1cc432jsn03b514aa1fab"  # ⬅️ reemplaza con tu clave de WordsAPI

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
        background-color: #111;
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        font-size: 14px;
        max-width: 320px;
        z-index: 9999;
        pointer-events: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        white-space: normal;
    }}
    button.audio {{
        margin-top: 8px;
        background-color: #2563eb;
        border: none;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 13px;
        cursor: pointer;
        pointer-events: auto;
        z-index: 10000;
    }}
    </style>

    <div id="text-container" style="line-height: 1.8; font-size: 18px;">
        {html_words}
        <div id="tooltip"></div>
    </div>

    <script>
    const tooltip = window.parent.document.getElementById("tooltip") || document.getElementById("tooltip");

    function speakWord(word) {{
        const utterance = new SpeechSynthesisUtterance(word);
        utterance.lang = "en-US";
        window.speechSynthesis.speak(utterance);
    }}

    function hideTooltip() {{
        tooltip.style.display = "none";
    }}

    document.addEventListener("click", (e) => {{
        if (!e.target.classList.contains("word")) {{
            hideTooltip();
        }}
    }});

    window.addEventListener("scroll", hideTooltip);

    document.querySelectorAll(".word").forEach(wordEl => {{
        wordEl.addEventListener("click", async () => {{
            const word = wordEl.innerText;
            const rect = wordEl.getBoundingClientRect();
            tooltip.innerHTML = "⏳ Buscando...";
            tooltip.style.left = (rect.left + window.scrollX + rect.width / 2) + "px";
            tooltip.style.top = (rect.top + window.scrollY - 60) + "px";
            tooltip.style.display = "block";

            try {{
                const transRes = await fetch("https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + encodeURIComponent(word));
                const transData = await transRes.json();
                const translated = transData[0][0][0];

                const wordsapiRes = await fetch("https://wordsapiv1.p.rapidapi.com/words/" + encodeURIComponent(word), {{
                    method: "GET",
                    headers: {{
                        "X-RapidAPI-Key": "{RAPIDAPI_KEY}",
                        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
                    }}
                }});
                const wordData = await wordsapiRes.json();

                let examples = [];
                let synonyms = [];
                if (Array.isArray(wordData.results) && wordData.results.length > 0) {{
                    examples = wordData.results[0].examples?.slice(0, 3) || [];
                    synonyms = wordData.results[0].synonyms?.slice(0, 3) || [];
                }}

                let html = `<strong>📌 ${{word}}</strong><br>`;
                html += `🔁 <strong>Traducción:</strong> ${{translated}}<br>`;
                if (examples.length > 0) {{
                    html += `<br><strong>✍️ Ejemplos:</strong><br>` + examples.map(e => `– ${{e}}`).join("<br>");
                }}
                if (synonyms.length > 0) {{
                    html += `<br><br><strong>🔄 Sinónimos:</strong> ` + synonyms.join(", ");
                }}
                html += `<br><button class='audio' onclick="event.stopPropagation(); speakWord('${{word}}')">🔊 Escuchar</button>`;
                tooltip.innerHTML = html;
            }} catch (err) {{
                tooltip.innerHTML = "⚠️ Error al obtener datos.";
            }}
        }});
    }});
    </script>
    """

    components.html(html_code, height=600, scrolling=True)
