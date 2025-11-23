import streamlit as st
import requests

BACKEND = "https://lonesomely-unbevelled-audriana.ngrok-free.dev"


st.title("📚 Phrase Bank")

keyword = st.text_input("Search keyword")
limit = st.slider("Limit", 1, 20, 5)

if st.button("Search"):
    r = requests.get(f"{BACKEND}/phrases", params={"keyword": keyword, "limit": limit})
    phrases = r.json().get("phrases", [])
    for p in phrases:
        st.markdown(f"**{p['english']}**  →  {p['hindi']}")
