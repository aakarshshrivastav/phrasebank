import streamlit as st
import requests

# ⬅️ Change this if you use ngrok or some other URL
BACKEND = "http://127.0.0.1:5005"

st.title("🌐 Text Translation")

text = st.text_area("Enter text", height=150)

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Source", ["en", "hi", "ta", "te", "bn", "mr", "gu", "pa"], index=0)

with col2:
    target = st.selectbox("Target", ["en", "hi", "ta", "te", "bn", "mr", "gu", "pa"], index=1)

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter some text to translate.")
    elif source == target:
        st.info("Source and target languages are the same.")
    else:
        try:
            with st.spinner("Translating..."):
                r = requests.post(
                    f"{BACKEND}/translate",
                    json={"text": text, "source": source, "target": target},
                    timeout=60,
                )
            if r.status_code == 200:
                data = r.json()
                translated = data.get("translated_text", "")
                st.success(translated if translated else "No translated text returned.")
            else:
                st.error(f"Backend error {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"Could not reach backend: {e}")
