import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt

@st.cache_data
def carregar_dados(url):
    return pd.read_csv(url)

# URL base para os arquivos S3
BASE_URL = "dados/"

# Configurar layout
st.set_page_config(layout="wide", page_title="Dashboard de Vendas")

# Sidebar: Seleção de arquivo e botão
st.sidebar.header("Configuração")
arquivo = st.sidebar.selectbox(
    "Selecione o arquivo da S3:",
    ["base_vendas_ecommerce.csv", "housing.csv"]  # Adicione mais arquivos aqui, se necessário
)
botao_ok = st.sidebar.button("Carregar Dados")

# Variável para armazenar os dados carregados
dados = None

if botao_ok:
    # Carregar dados do arquivo selecionado
    url = BASE_URL + arquivo
    st.write(arquivo)
    dados = carregar_dados(url)
    st.sidebar.success(f"Dados carregados: {arquivo}")

if arquivo != "housing.csv":
    if dados is not None:
        # Normalizar dados
        dados["fabricante"] = dados["fabricante"].str.lower()
        dados["data_compra"] = pd.to_datetime(dados["data_compra"], errors="coerce")

        # Criar container principal
        with st.container():
            st.write("container")
            # Dividir o layout em colunas
            col1, col2 = st.columns(2)

            # Gráfico 1: Quantidade em Estoque por Fabricante
            with col1:
                st.subheader("1) Quantidade em Estoque por Fabricante")
                estoque = (
                    dados.groupby("fabricante")["quantidade_estoque"]
                    .sum()
                    .reset_index()
                    .sort_values("quantidade_estoque", ascending=False)
                )
                chart1 = (
                    alt.Chart(estoque)
                    .mark_bar()
                    .encode(
                        x=alt.X("fabricante:N", title="Fabricante"),
                        y=alt.Y("quantidade_estoque:Q", title="Quantidade em Estoque"),
                        color="fabricante:N",
                    )
                )
                st.altair_chart(chart1, use_container_width=True)

            # Gráfico 2: Linha - Preço total por Data de Compra
            with col2:
                st.subheader("2) Preço Total por Data de Compra")
                soma_precos = (
                    dados.groupby("data_compra")["preco"]
                    .sum()
                    .reset_index()
                    .sort_values("data_compra")
                )
                chart2 = (
                    alt.Chart(soma_precos)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("data_compra:T", title="Data de Compra"),
                        y=alt.Y("preco:Q", title="Soma dos Preços"),
                    )
                )
                st.altair_chart(chart2, use_container_width=True)

            # Dividir os próximos gráficos em colunas
            col3, col4 = st.columns(2)

            # Gráfico 3: Pizza - Quantidade Vendida por Categoria
            with col3:
                st.subheader("3) Quantidade Vendida por Categoria")
                categoria = (
                    dados.groupby("categoria_produto")["quantidade_vendida"]
                    .sum()
                    .reset_index()
                )
                chart3 = (
                    alt.Chart(categoria)
                    .mark_arc()
                    .encode(
                        theta=alt.Theta("quantidade_vendida:Q", title="Quantidade Vendida"),
                        color=alt.Color("categoria_produto:N", title="Categoria"),
                    )
                )
                st.altair_chart(chart3, use_container_width=True)

            # Gráfico 4: Barras - 5 Produtos com Pior Avaliação

                with col4:
                    st.subheader("4) 5 Categorias com Piores Avaliações")

                    # Remover valores nulos e calcular a média das avaliações
                    piores_categorias = (
                        dados.dropna(subset=["avaliacao_produto"])  # Remover nulos
                        .groupby("categoria_produto")
                        .agg({"avaliacao_produto": "mean"})  # Calcular média
                        .reset_index()
                        .sort_values("avaliacao_produto", ascending=True)  # Ordenar da pior para melhor
                        .head(5)  # Selecionar as 5 piores
                    )

                    # Criar gráfico de barras
                    chart4 = (
                        alt.Chart(piores_categorias)
                        .mark_bar()
                        .encode(
                            x=alt.X("avaliacao_produto:Q", title="Média de Avaliação"),
                            y=alt.Y("categoria_produto:N", title="Categoria", sort="-x"),
                            color=alt.Color(
                                "avaliacao_produto:Q",
                                title="Média de Avaliação",
                                scale=alt.Scale(scheme="viridis"),
                            ),
                        )
                    )

                    # Exibir gráfico
                    st.altair_chart(chart4, use_container_width=True)




            # Dividir os últimos gráficos em colunas
            col5, col6 = st.columns(2)

            # Gráfico 5: Barras - Vendas por Faixa Etária
            with col5:
                st.subheader("5) Vendas por Faixa Etária")
                faixa_etaria = (
                    dados.groupby("faixa_etaria_cliente")["quantidade_vendida"]
                    .sum()
                    .reset_index()
                    .sort_values("quantidade_vendida", ascending=False)
                )
                chart5 = (
                    alt.Chart(faixa_etaria)
                    .mark_bar()
                    .encode(
                        x=alt.X("faixa_etaria_cliente:N", title="Faixa Etária"),
                        y=alt.Y("quantidade_vendida:Q", title="Quantidade Vendida"),
                        color="faixa_etaria_cliente:N",
                    )
                )
                st.altair_chart(chart5, use_container_width=True)

            # Gráfico 6: Barras - Quantidade Vendida por Gênero
            with col6:
                st.subheader("6) Quantidade Vendida por Gênero")
                genero = (
                    dados.groupby("genero_cliente")["quantidade_vendida"]
                    .sum()
                    .reset_index()
                    .sort_values("quantidade_vendida", ascending=False)
                )
                chart6 = (
                    alt.Chart(genero)
                    .mark_bar()
                    .encode(
                        x=alt.X("genero_cliente:N", title="Gênero"),
                        y=alt.Y("quantidade_vendida:Q", title="Quantidade Vendida"),
                        color="genero_cliente:N",
                    )
                )
                st.altair_chart(chart6, use_container_width=True)
    else:
        st.warning("Selecione um arquivo e clique em OK para carregar os dados.")

else:
    if dados is not None:
        
        # Exibindo a tabela de dados
        st.dataframe(dados)

        # Exibindo algumas estatísticas descritivas
        st.write("Estatísticas descritivas:")
        st.write(dados.describe())
    else:
        print("Algo Errado com o arquivo...")
