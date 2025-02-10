import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Sistema Financeiro", layout="wide")

# Estilos customizados
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
        }
        .stSelectbox>div>div>select {
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Título do aplicativo
st.title('💰 Sistema Financeiro Pessoal')

# Inicializar dados
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor', 'Tipo'])

# Função para adicionar transação
def adicionar_transacao(data, descricao, categoria, valor, tipo):
    nova_transacao = pd.DataFrame({
        'Data': [data],
        'Descrição': [descricao],
        'Categoria': [categoria],
        'Valor': [valor],
        'Tipo': [tipo]
    })
    st.session_state.dados = pd.concat([st.session_state.dados, nova_transacao], ignore_index=True)

# Barra lateral
st.sidebar.header("📌 Adicionar Transação")
data = st.sidebar.date_input("Data", datetime.now())
descricao = st.sidebar.text_input("Descrição")
categorias = st.session_state.dados['Categoria'].unique().tolist() if not st.session_state.dados.empty else ["Alimentação", "Transporte", "Lazer", "Saúde", "Outros"]
nova_categoria = st.sidebar.text_input("Nova Categoria (Opcional)")
if nova_categoria:
    categorias.append(nova_categoria)
categoria = st.sidebar.selectbox("Categoria", categorias)
valor = st.sidebar.number_input("Valor", min_value=0.0, format="%.2f")
tipo = st.sidebar.selectbox("Tipo", ["Receita", "Despesa"])

if st.sidebar.button("Adicionar"):
    adicionar_transacao(data, descricao, categoria, valor, tipo)
    st.sidebar.success("Transação adicionada com sucesso!")

# Filtros
st.sidebar.header("🔍 Filtrar Transações")
tipo_filtro = st.sidebar.selectbox("Filtrar por Tipo", ["Todos", "Receita", "Despesa"])
data_inicial = st.sidebar.date_input("Data Inicial", datetime.now())
data_final = st.sidebar.date_input("Data Final", datetime.now())

# Aplicar filtros
df_filtrado = st.session_state.dados
if tipo_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_filtro]
df_filtrado = df_filtrado[(df_filtrado['Data'] >= data_inicial) & (df_filtrado['Data'] <= data_final)]

# Exibição de transações
st.subheader("📋 Transações")
st.dataframe(df_filtrado, use_container_width=True)

# Análise financeira
if not df_filtrado.empty:
    total_receitas = df_filtrado[df_filtrado['Tipo'] == 'Receita']['Valor'].sum()
    total_despesas = df_filtrado[df_filtrado['Tipo'] == 'Despesa']['Valor'].sum()
    saldo = total_receitas - total_despesas

    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas", f"R$ {total_receitas:.2f}", "+")
    col2.metric("Despesas", f"R$ {total_despesas:.2f}", "-")
    col3.metric("Saldo", f"R$ {saldo:.2f}")

    # Gráfico
    st.subheader("📊 Gráfico de Receita vs Despesa")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Receitas', 'Despesas'], [total_receitas, total_despesas], color=['green', 'red'])
    ax.set_ylabel('Valor (R$)')
    st.pyplot(fig)
else:
    st.info("Nenhuma transação registrada no período selecionado.")

# Exportação
st.subheader("📤 Exportar Dados")
if st.button("Exportar para CSV"):
    df_filtrado.to_csv("transacoes_financeiras.csv", index=False)
    st.success("Dados exportados para 'transacoes_financeiras.csv'!")
