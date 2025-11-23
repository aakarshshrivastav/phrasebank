import streamlit as st
import requests

BACKEND = "https://lonesomely-unbevelled-audriana.ngrok-free.dev"


st.title("🎙️ Speech → Text")

audio = st.file_uploader("Upload audio (wav/mp3)")

if st.button("Transcribe"):
    if audio:
        r = requests.post(f"{BACKEND}/stt", files={"audio": audio})
        st.success(r.json().get("text"))
    else:
        st.warning("Upload an audio file first.")
