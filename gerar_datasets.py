import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import names

pasta_datasets = Path(__file__).parent / "datasets"
pasta_datasets.mkdir(parents=True, exist_ok=True)

LOJAS = [
    {"estado": "SP", "cidade": "São Paulo", "vendedor": ["Aline Maria", "Lucas Silva"]},
    {"estado": "RJ", "cidade": "Rio de Janeiro", "vendedor": ["Carla Souza", "Bruno Costa"]},
    {"estado": "MG", "cidade": "Belo Horizonte", "vendedor": ["Ana Paula", "Fernando Alves"]},
    {"estado": "RS", "cidade": "Porto Alegre", "vendedor": ["Mariana Lima", "Rafael Oliveira"]},
    {"estado": "BA", "cidade": "Salvador", "vendedor": ["Juliana Santos", "Thiago Pereira"]},
]

PRODUTOS = [
    {"nome": "Smartphone", "id": 0, "preco": 1500.00},
    {"nome": "Notebook", "id": 1, "preco": 3500.00},
    {"nome": "Smartwatch", "id": 2, "preco": 800.00},
    {"nome": "Tablet", "id": 3, "preco": 1200.00},
    {"nome": "Fone de Ouvido", "id": 4, "preco": 250.00},
]

FORMA_PAGAMENTO = ["Cartão de Crédito", "Boleto", "Pix", "Dinheiro"]
GENERO_CLIENTES = ["Masculino", "Feminino"]

compras = []

for i in range(2000):
    loja = random.choice(LOJAS)
    vendedor = random.choice(loja["vendedor"])
    produto = random.choice(PRODUTOS)
    hora_compra = datetime.now() - timedelta(days=random.randint(1, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    data_compra = datetime.now() - timedelta(days=random.randint(1, 365))
    quantidade = random.randint(1, 5)
    valor_total = produto["preco"] * quantidade
    forma_pagamento = random.choice(FORMA_PAGAMENTO)
    genero_cliente = random.choice(GENERO_CLIENTES)
    nome_cliente = names.get_full_name(gender=genero_cliente.lower())
    
    compras.append({
        "data_compra": data_compra.strftime("%Y-%m-%d"),
        "id_compra": i + 1,
        "loja": loja["cidade"],
        "vendedor": vendedor,
        "produto": produto["nome"],
        "cliente_nome": nome_cliente,
        "cliente_genero": genero_cliente,
        "hora_compra": hora_compra.strftime("%H:%M:%S"),
        "quantidade": quantidade,
        "valor_total": valor_total,
        "forma_pagamento": forma_pagamento
    })

df_compras = pd.DataFrame(compras).set_index("data_compra").sort_index()
df_lojas = pd.DataFrame(LOJAS)
df_produtos = pd.DataFrame(PRODUTOS)

df_compras.to_csv(pasta_datasets / "compras.csv", decimal=",", sep=";")
df_produtos.to_csv(pasta_datasets / "produtos.csv", decimal=",", sep=";")
df_lojas.to_csv(pasta_datasets / "lojas.csv", decimal=",", sep=";")

df_compras.to_excel(pasta_datasets / "compras.xlsx")
df_produtos.to_excel(pasta_datasets / "produtos.xlsx")
df_lojas.to_excel(pasta_datasets / "lojas.xlsx")
