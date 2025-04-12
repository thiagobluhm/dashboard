import streamlit as st
import pandas as pd
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
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="none")
                ax.bar(
                    estoque["fabricante"],
                    estoque["quantidade_estoque"],
                    color="tomato"
                )
                ax.set_xlabel("Fabricante", fontsize=12, labelpad=10, color="white")
                ax.set_ylabel("Quantidade em Estoque", fontsize=12, labelpad=10, color="white")
                ax.set_title("Quantidade em Estoque por Fabricante", fontsize=14, pad=15, color="white")
                ax.tick_params(axis="x", colors="white", rotation=45)
                ax.tick_params(axis="y", colors="white")
                ax.set_facecolor("none")
                fig.patch.set_alpha(0.0)
                plt.tight_layout()
                st.pyplot(fig)

            # Gráfico 2: Linha - Preço total por Data de Compra
            with col2:
                st.subheader("2) Preço Total por Data de Compra")
                soma_precos = (
                    dados.groupby("data_compra")["preco"]
                    .sum()
                    .reset_index()
                    .sort_values("data_compra")
                )
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="none")
                ax.plot(
                    soma_precos["data_compra"],
                    soma_precos["preco"],
                    color="cyan",
                    marker="o",
                    linestyle="-"
                )
                ax.set_xlabel("Data de Compra", fontsize=12, labelpad=10, color="white")
                ax.set_ylabel("Soma dos Preços", fontsize=12, labelpad=10, color="white")
                ax.set_title("Preço Total por Data de Compra", fontsize=14, pad=15, color="white")
                ax.tick_params(axis="x", colors="white", rotation=45)
                ax.tick_params(axis="y", colors="white")
                ax.set_facecolor("none")
                fig.patch.set_alpha(0.0)
                plt.tight_layout()
                st.pyplot(fig)

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
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="none")
                ax.pie(
                    categoria["quantidade_vendida"],
                    labels=categoria["categoria_produto"],
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=plt.cm.viridis(np.linspace(0, 1, len(categoria)))
                )
                ax.set_title("Quantidade Vendida por Categoria", fontsize=14, pad=15, color="white")
                fig.patch.set_alpha(0.0)
                st.pyplot(fig)

            # Gráfico 4: Barras - 5 Categorias com Piores Avaliações
            with col4:
                st.subheader("4) 5 Categorias com Piores Avaliações")
                piores_categorias = (
                    dados.dropna(subset=["avaliacao_produto"])
                    .groupby("categoria_produto")
                    .agg({"avaliacao_produto": "mean"})
                    .reset_index()
                    .sort_values("avaliacao_produto", ascending=True)
                    .head(5)
                )
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="none")
                bars = ax.barh(
                    piores_categorias["categoria_produto"],
                    piores_categorias["avaliacao_produto"],
                    color=plt.cm.viridis(np.linspace(0, 1, len(piores_categorias))),
                )
                ax.set_xlabel("Média de Avaliação", fontsize=12, labelpad=10, color="white")
                ax.set_ylabel("Categoria", fontsize=12, labelpad=10, color="white")
                ax.set_title("5 Categorias com Piores Avaliações", fontsize=14, pad=15, color="white")
                ax.tick_params(axis="x", colors="white")
                ax.tick_params(axis="y", colors="white")
                ax.set_facecolor("none")
                fig.patch.set_alpha(0.0)
                plt.tight_layout()
                st.pyplot(fig)

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
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="none")
                ax.bar(
                    faixa_etaria["faixa_etaria_cliente"],
                    faixa_etaria["quantidade_vendida"],
                    color="orange",
                )
                ax.set_xlabel("Faixa Etária", fontsize=12, labelpad=10, color="white")
                ax.set_ylabel("Quantidade Vendida", fontsize=12, labelpad=10, color="white")
                ax.set_title("Vendas por Faixa Etária", fontsize=14, pad=15, color="white")
                ax.tick_params(axis="x", colors="white", rotation=45)
                ax.tick_params(axis="y", colors="white")
                ax.set_facecolor("none")
                fig.patch.set_alpha(0.0)
                plt.tight_layout()
                st.pyplot(fig)

            # Gráfico 6: Barras - Quantidade Vendida por Gênero
            with col6:
                st.subheader("6) Quantidade Vendida por Gênero")
                genero = (
                    dados.groupby("genero_cliente")["quantidade_vendida"]
                    .sum()
                    .reset_index()
                    .sort_values("quantidade_vendida", ascending=False)
                )
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="none")
                ax.bar(
                    genero["genero_cliente"],
                    genero["quantidade_vendida"],
                    color="skyblue",
                )
                ax.set_xlabel("Gênero", fontsize=12, labelpad=10, color="white")
                ax.set_ylabel("Quantidade Vendida", fontsize=12, labelpad=10, color="white")
                ax.set_title("Quantidade Vendida por Gênero", fontsize=14, pad=15, color="white")
                ax.tick_params(axis="x", colors="white", rotation=45)
                ax.tick_params(axis="y", colors="white")
                ax.set_facecolor("none")
                fig.patch.set_alpha(0.0)
                plt.tight_layout()
                st.pyplot(fig)
    else:
        st.warning("Selecione um arquivo e clique em OK para carregar os dados.")

else:
    if dados is not None:
        st.dataframe(dados)
        st.write("Estatísticas descritivas:")
        st.write(dados.describe())
    else:
        print("Algo Errado com o arquivo...")
