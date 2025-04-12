import streamlit as st
import pandas as pd
import plotly.express as px

# Criando um dataset fictício
st.title("Gráficos Interativos com Plotly")
data = {
    "Produto": ["A", "B", "C", "D"],
    "Vendas": [100, 150, 200, 250],
}
df = pd.DataFrame(data)

# Criando um gráfico interativo
fig = px.bar(df, x="Produto", y="Vendas", title="Vendas por Produto")

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)
