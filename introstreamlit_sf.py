import streamlit as st
import pandas as pd
import altair as alt
import snowflake.connector


def pegar_DADOS():
    conn = snowflake.connector.connect(
        user="TBLUHM",
        password="@ulaUnifor2025c",
        account="JHOFSPC-NOA08484",
        warehouse="AULAUNIFOR_WH",
        database="DBAULA",
        schema="AIRBYTEDATA",
        role="ACCOUNTADMIN"
    )

    consulta = """
        SELECT FABRICANTE, QUANTIDADE_ESTOQUE
        FROM AWS_ECOMMERCE
    """

    df = pd.read_sql(consulta, conn)
    conn.close()
    return df

try:
    # Obter os dados
    df = pegar_DADOS()

    rename = {"FABRICANTE": "fabricante", "QUANTIDADE_ESTOQUE": "quantidade_estoque"}
    df.rename(columns=rename, inplace=True)

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
