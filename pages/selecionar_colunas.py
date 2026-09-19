import streamlit as st
import pandas as pd

caminho_arquivo = "datasets/compras.csv"

df_compras = pd.read_csv(caminho_arquivo, sep=";", decimal=",")
df_compras = df_compras.sort_values(by=["data_compra", "hora_compra"], ascending=[False, False])

colunas = list(df_compras.columns)
colunas_selecionadas = st.sidebar.multiselect("Selecione as Colunas:", colunas, colunas)

col1, col2 = st.sidebar.columns(2)
col_filtro = col1.selectbox("Selecione a Coluna", [c for c in colunas if c not in ["id_compra"]])

valor_filtro = col2.selectbox("Selecione o Valor", list(df_compras[col_filtro].unique()))

st_filtrar = col1.button("Filtrar")
st_limpar = col2.button("Limpar")

if st_filtrar:
    st.dataframe(df_compras.loc[df_compras[col_filtro] == valor_filtro, colunas_selecionadas])
elif st_limpar:
    st.dataframe(df_compras[colunas_selecionadas])
else:
    st.dataframe(df_compras[colunas_selecionadas])
