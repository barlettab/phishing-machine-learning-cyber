import streamlit as st

st.title("Resultado da análise")

st.error("⚠ URL SUSPEITA DE PHISHING")

st.metric("Score de risco", "87%")

st.write("### Principais sinais detectados:")
st.write("- Estrutura de domínio suspeita")
st.write("- Possível uso de subdomínios enganosos")
st.write("- Similaridade com padrões de phishing conhecidos")
