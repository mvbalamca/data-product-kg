import streamlit as st
import requests

st.set_page_config(page_title="Neo4j KG Assistant 💡", layout="centered")
st.title("🧠 Knowledge Graph Assistant")
st.markdown("Ask questions about your data products using natural language.")

question = st.text_input("💬 Ask a question:")

if st.button("Get Answer") and question:
    with st.spinner("🔎 Thinking..."):
        try:
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": question},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            st.code(data.get("cypher", ""), language="cypher")
            if "results" in data:
                st.json(data["results"])
            if "answer" in data:
                st.success(data["answer"])
            if "error" in data:
                st.error(data["error"])
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")