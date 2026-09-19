import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(
    page_title="Visão Geral",
    page_icon="📊",
    layout="wide"
)

caminho_datasets = "datasets"

df_compras = pd.read_csv(f"{caminho_datasets}/compras.csv", decimal=",", sep=";", index_col=0, parse_dates=True)
df_lojas = pd.read_csv(f"{caminho_datasets}/lojas.csv", decimal=",", sep=";", index_col=0)
df_produtos = pd.read_csv(f"{caminho_datasets}/produtos.csv", decimal=",", sep=";", index_col=0)

df_produtos = df_produtos.rename(columns={"nome": "produto"})

df_compras = df_compras.reset_index()
df_compras = pd.merge(
    left=df_compras,
    right=df_produtos[["preco", "produto"]],
    on="produto",
    how="left"
)
df_compras = df_compras.set_index("data_compra")

st.sidebar.header("Filtros Globais")

data_default = df_compras.index.date.max()
data_min = df_compras.index.date.min()

data_inicio = st.sidebar.date_input("Data Inicial", data_default - timedelta(days=30), min_value=data_min, max_value=data_default)
data_final = st.sidebar.date_input("Data Final", data_default, min_value=data_min, max_value=data_default)

lista_lojas = sorted(df_compras["loja"].unique().tolist())
lojas_selecionadas = st.sidebar.multiselect("Selecione as Lojas", lista_lojas, default=lista_lojas)

df_filtrado = df_compras[
    (df_compras.index.date >= data_inicio) &
    (df_compras.index.date <= data_final) &
    (df_compras["loja"].isin(lojas_selecionadas))
]

st.title("📊 Visão Geral e Gráficos")
st.markdown("Análise consolidada dos principais indicadores e desempenho de vendas.")

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    col1, col2, col3, col4 = st.columns(4)
    
    valor_total = df_filtrado["valor_total"].sum()
    qtd_compras = df_filtrado["id_compra"].count()
    ticket_medio = valor_total / qtd_compras if qtd_compras > 0 else 0
    total_clientes = df_filtrado["cliente_nome"].nunique()
    
    col1.metric("Valor Total", f"R$ {valor_total:.2f}")
    col2.metric("Total de Compras", f"{qtd_compras}")
    col3.metric("Ticket Médio", f"R$ {ticket_medio:.2f}")
    col4.metric("Clientes Únicos", f"{total_clientes}")
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Vendas por Loja")
        vendas_loja = df_filtrado.groupby("loja")["valor_total"].sum()
        st.bar_chart(vendas_loja)
        
    with col_b:
        st.subheader("Vendas por Forma de Pagamento")
        vendas_pagamento = df_filtrado.groupby("forma_pagamento")["valor_total"].sum()
        st.bar_chart(vendas_pagamento)
        
    st.divider()
    
    st.subheader("Evolução Diária de Vendas")
    vendas_diarias = df_filtrado.groupby(df_filtrado.index)["valor_total"].sum()
    st.line_chart(vendas_diarias)
