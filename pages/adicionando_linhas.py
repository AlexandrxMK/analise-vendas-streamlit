from datetime import datetime
import pandas as pd
import streamlit as st

caminho_datasets = "datasets"

df_compras = pd.read_csv(f"{caminho_datasets}/compras.csv", decimal=",", sep=";")
df_lojas = pd.read_csv(f"{caminho_datasets}/lojas.csv", decimal=",", sep=";")
df_produtos = pd.read_csv(f"{caminho_datasets}/produtos.csv", decimal=",", sep=";")

df_lojas["cidade/estado"] = df_lojas["cidade"] + "/" + df_lojas["estado"]
lista_lojas = df_lojas["cidade/estado"].to_list()
loja_selecionada = st.sidebar.selectbox("Selecione a Loja:", lista_lojas)

lista_vendedores = df_lojas.loc[df_lojas["cidade/estado"] == loja_selecionada, "vendedor"].iloc[0]
lista_vendedores = lista_vendedores.strip("][").replace("'", "").split(", ")
vendedor_selecionado = st.sidebar.selectbox("Selecione o Vendedor:", lista_vendedores)

lista_produtos = df_produtos["nome"].to_list()
produtos_selecionados = st.sidebar.selectbox("Selecione o Produto:", lista_produtos)

nome_cliente = st.sidebar.text_input("Nome do Cliente:")
genero_selecionado = st.sidebar.selectbox("Gênero do Cliente:", ["Masculino", "Feminino"])

forma_pagamento_selecionada = st.sidebar.selectbox("Forma de Pagamento:", ["Cartão de Crédito", "Boleto", "Pix", "Dinheiro"])

if st.sidebar.button("Adicionar Nova Compra"):
    preco = df_produtos.loc[df_produtos["nome"] == produtos_selecionados, "preco"].iloc[0]
    nova_compra = {
        "data_compra": datetime.now().strftime("%Y-%m-%d"),
        "id_compra": df_compras["id_compra"].max() + 1 if not df_compras.empty else 1,
        "loja": loja_selecionada.split("/")[0],
        "vendedor": vendedor_selecionado,
        "produto": produtos_selecionados,
        "cliente_nome": nome_cliente,
        "cliente_genero": genero_selecionado,
        "hora_compra": datetime.now().strftime("%H:%M:%S"),
        "quantidade": 1,
        "valor_total": preco,
        "forma_pagamento": forma_pagamento_selecionada
    }
    df_compras = pd.concat([df_compras, pd.DataFrame([nova_compra])], ignore_index=True)
    
    df_compras.to_csv(f"{caminho_datasets}/compras.csv", index=False, decimal=",", sep=";")
    st.success("Compra adicionada com sucesso!")

st.dataframe(df_compras)