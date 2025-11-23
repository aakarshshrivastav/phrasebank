import streamlit as st
import requests

BACKEND = "https://lonesomely-unbevelled-audriana.ngrok-free.dev"


st.title("📝 Save Practice Logs")

pid = st.text_input("Phrase ID")
ref = st.text_input("Reference Text")
user = st.text_input("Your Attempt")
score = st.number_input("Score", 0, 100)
duration = st.number_input("Duration", 0.0)
lang = st.selectbox("Language", ["en","hi","ta","bn","mr","gu","pa","te"])

if st.button("Save Log"):
    payload = {
        "phrase_id": pid,
        "reference_text": ref,
        "user_text": user,
        "score": score,
        "duration": duration,
        "language": lang
    }

    requests.post(f"{BACKEND}/log", json=payload)
    st.success("Log saved successfully!")


