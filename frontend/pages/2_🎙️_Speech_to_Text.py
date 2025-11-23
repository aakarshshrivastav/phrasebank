import streamlit as st
import requests

BACKEND = "http://localhost:5001"

st.title("🎙️ Speech → Text")

audio = st.file_uploader("Upload audio (wav/mp3)")

if st.button("Transcribe"):
    if audio:
        r = requests.post(f"{BACKEND}/stt", files={"audio": audio})
        st.success(r.json().get("text"))
    else:
        st.warning("Upload an audio file first.")
