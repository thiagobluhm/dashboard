# Importando a biblioteca Streamlit
import streamlit as st

setor = "TECH"
nome = "Thiago Bluhm"
titulo = f"Hello {nome} do setor {setor}, World com Streamlit"
# Exibindo um título no aplicativo
st.title(titulo)

# Exibindo um texto no aplicativo
st.write("Este é o meu primeiro aplicativo com Streamlit!")

# Criando um botão
if st.button("Clique aqui"):
    st.write("Você clicou no botão!")
