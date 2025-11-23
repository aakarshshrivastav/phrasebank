import streamlit as st
import base64

st.set_page_config(
    page_title="Voice Translator AI",
    page_icon="🎤",
    layout="wide",
)

# Load CSS animations
import os

css_path = os.path.join(os.path.dirname(__file__), "assets", "wave.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


hero_html = """
<div class="hero">
    <h1 class="title">🎤 Voice Translator AI</h1>
    <p class="subtitle">Real-time translation • Speech synthesis • Pronunciation scoring • Whisper STT</p>
    <div class="buttons">
        <a href="/?page=Text_to_Speech" class="btn">Text → Speech</a>
        <a href="/?page=Speech_to_Text" class="btn">Speech → Text</a>
        <a href="/?page=Translate" class="btn">Translate</a>
        <a href="/?page=Pronunciation_Score" class="btn">Pronunciation</a>
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.info("Use the sidebar to navigate between features.")
