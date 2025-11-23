import streamlit as st
import requests

BACKEND = "https://lonesomely-unbevelled-audriana.ngrok-free.dev"


st.title("🌐 Text Translation")

text = st.text_area("Enter text")
col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Source", ["en","hi","ta","te","bn","mr","gu","pa"])
with col2:
    target = st.selectbox("Target", ["en","hi","ta","te","bn","mr","gu","pa"])

if st.button("Translate"):
    r = requests.post(f"{BACKEND}/translate", json={"text": text, "source": source, "target": target})
    st.success(r.json().get("translated_text"))
