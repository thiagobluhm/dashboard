import streamlit as st

# Configurando o layout com colunas
st.title("Layout Personalizado com Colunas")

col1, col2 = st.columns(2)

with col1:
    st.write("Esta é a Coluna 1")

st.write("aqui aqui aqui aqui aqui...")

with col2:
    st.write("Esta é a Coluna 2")

st.write("aqui aqui aqui aqui aqui...")

col1, col2 = st.columns(2)

with col1:
    st.write("Esta é a Coluna 1")


with col2:
    st.write("Esta é a Coluna 2")



st.write("aqui aqui aqui aqui....")



