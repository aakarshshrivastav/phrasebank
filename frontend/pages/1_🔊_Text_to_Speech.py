import streamlit as st
import requests

BACKEND = "http://localhost:5001"

st.title("🔊 Text → Speech")

text = st.text_input("Enter text")
lang = st.selectbox("Language", ["en","hi","ta","te","bn","mr","gu","pa"])

if st.button("Generate Audio"):
    r = requests.post(f"{BACKEND}/tts", json={"text": text, "language": lang})
    if r.status_code == 200:
        st.audio(r.content, format="audio/mp3")
    else:
        st.error("TTS failed")
