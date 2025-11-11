import streamlit as st
import requests

st.set_page_config(page_title="GenAI E-commerce Chat", layout="wide")

api = st.sidebar.text_input("API URL", value="http://localhost:8000")

st.title("🛒 GenAI E-commerce Chat Demo")

q = st.text_input("Ask a question:", "Which category had the highest sales in the last 3 months?")

if st.button("Ask"):
    res = requests.post(f"{api}/ask", json={"question": q}).json()

    st.subheader("SQL Generated")
    st.code(res["sql"])

    st.subheader("Result")
    st.dataframe(res["data"]["rows"])
