import streamlit as st

st.title("Detector de Phishing em URLs")

st.subheader("Entrada de URL")

url = st.text_input("URL suspeita")

st.caption("Insira uma URL para análise de possíveis tentativas de phishing.")

st.button("Analisar URL")
