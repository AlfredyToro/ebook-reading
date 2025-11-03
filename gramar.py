import streamlit as st
import streamlit.components.v1 as components

st.title("🔁 Rephrase con GPT-4o (Puter.js)")

components.html("""
  <textarea id="input" rows="5" cols="60" placeholder="Escribe tu texto aquí..."></textarea><br><br>
  <button onclick="rephrase()">Rephrase</button>
  <h3>Resultado:</h3>
  <div id="output" style="white-space: pre-wrap; font-family: monospace;"></div>

  <script src="https://js.puter.com/v2/"></script>
  <script>
    async function rephrase() {
      const input = document.getElementById("input").value;
      document.getElementById("output").innerText = "⏳ Procesando...";
      const prompt = `Rephrase this sentence in better English:\\n${input}`;
      const response = await puter.ai.chat(prompt);
      document.getElementById("output").innerText = response;
    }
  </script>
""", height=400)
