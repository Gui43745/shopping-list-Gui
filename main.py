import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    dados = pd.read_csv("compra.csv")
except:
    dados = pd.DataFrame({"produto": [], "preço": []})
    dados.to_csv("compras.csv", index=False)

st.title("Controle de Compras")

orçamento = st.number_input("Orçamento:", min_value=0.0)
total = dados["preço"].sum() if not dados.empty else 0

with st.form("nova_compra"):
    produto = st.text_input("Adicione aqui o seu produto")
    preco = st.number_input("Indique o preço", min_value=0.0)

    if st.form_submit_button("Adicionar"):
        if preco <= (orçamento - total):
            nova_linha = pd.DataFrame({"produto": [produto], "preço": [preco]})
            dados = pd.concat([dados, nova_linha])
            dados.to_csv("compras.csv", index=False)
            st.success("Produto adicionado")
        else:
            st.error("Não tem orçamento suficiente")

if orçamento > 0:
    # Criar gráfico donut
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["produto"].tolist()
        valores = dados["preço"].tolist()
        restante = orçamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        plt.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        plt.title(f"Orçamento: {orçamento}€")
    
    # Criar gráfico circular
    centro = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(centro)
    st.pyplot(fig)

st.dataframe(dados)
st.write(f"Total gasto: {total}€")
st.write(f"Resta: {orçamento - total}€")
