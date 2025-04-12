# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd

# Lendo um arquivo CSV
st.title("Carregamento e Exibição de Dados")
uploaded_file = st.file_uploader("Faça o upload do arquivo CSV")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # Exibindo a tabela de dados
    st.dataframe(data)

    # Exibindo algumas estatísticas descritivas
    st.write("Estatísticas descritivas:")
    st.write(data.describe())

