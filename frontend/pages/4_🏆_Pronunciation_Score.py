import streamlit as st
import requests

BACKEND = "https://lonesomely-unbevelled-audriana.ngrok-free.dev"


st.title("🏆 Pronunciation Scoring")

reference = st.text_input("Correct Phrase")
attempt = st.text_input("Your Attempt")

if st.button("Score"):
    r = requests.post(f"{BACKEND}/score", json={"reference_text": reference, "user_text": attempt})
    res = r.json()

    st.metric("Score", f"{res['score']}%")
    st.write("Similarity:", res["similarity"])
    st.write("Feedback:", res["feedback"])
