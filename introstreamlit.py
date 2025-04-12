import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def pegar_DADOS():
    URL = "https://aula-unifor.s3.us-east-1.amazonaws.com"
    df = pd.read_csv(URL + "/base_vendas_ecommerce.csv")
    return df

try:
    # Obter os dados
    df = pegar_DADOS()

    # Padronizar fabricantes para letras minúsculas
    df["fabricante"] = df["fabricante"].str.lower()
    
    # Lista de fabricantes disponíveis
    fabricantes_disponiveis = df["fabricante"].unique().tolist()

    # Valores padrão
    valores_padrao = [f for f in ["sony", "apple"] if f in fabricantes_disponiveis]

    # Multiselect para fabricantes
    fabricantes = st.multiselect(
        "Selecione os fabricantes:",
        options=fabricantes_disponiveis,
        default=valores_padrao,
    )

    if not fabricantes:
        st.error("Por favor, selecione ao menos 1 fabricante.")
    else:
        # Filtrar dados pelos fabricantes selecionados
        dados = df[df["fabricante"].isin(fabricantes)]

        # Selecionar apenas as colunas necessárias
        dados = dados[["fabricante", "quantidade_estoque"]]

        # Agrupar dados por fabricante e somar os estoques
        dados = dados.groupby("fabricante").sum().reset_index()

        # Exibir os dados na tela
        st.write("### Quantidade de Estoque por Fabricante", dados)

        # Criar gráfico com Altair
        chart = (
            alt.Chart(dados)
            .mark_bar()
            .encode(
                x=alt.X("fabricante:N", title="Fabricante"),
                y=alt.Y("quantidade_estoque:Q", title="Quantidade em Estoque"),
                color="fabricante:N",
            )
        )

        # Exibir gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(
        f"""
        **Erro:**
        {e}
        """
    )
