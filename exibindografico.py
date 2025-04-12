# Importando bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Criando um dataset fictício
st.title("Visualização de Gráficos")
data = {
    "Ano": [2018, 2019, 2020, 2021],
    "Vendas": [150, 200, 300, 400],
}
df = pd.DataFrame(data)

# Exibindo os dados
st.write("Tabela de dados:", df)

# Criando um gráfico de barras
fig, ax = plt.subplots()
ax.bar(df["Ano"], df["Vendas"])
ax.set_title("Vendas por Ano")
ax.set_xlabel("Ano")
ax.set_ylabel("Vendas")

# Exibindo o gráfico no Streamlit
st.pyplot(fig)
