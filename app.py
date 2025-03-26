import streamlit as st
import pandas as pd
import metrics

def login():
    # Inicializa o estado se não existir
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username", key="username")
        password = st.sidebar.text_input("Password", type="password", key="password")
        if st.sidebar.button("Entrar"):
            if username == "admin" and password == "senha":
                st.session_state["logged_in"] = True
                st.sidebar.success("Login realizado com sucesso!")
            else:
                st.sidebar.error("Credenciais incorretas!")
        st.write("Por favor, faça login para continuar.")
        return False
    else:
        # Botão de logout para testar novamente
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()
        return True

def run_app():
    if not login():
        return

    st.title("Dashboard Interativo de Dados - Análise Completa")
    st.write("Faça o upload do arquivo CSV para gerar uma análise completa dos dados.")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Visualização dos Dados")
        st.write(df.head())
        
        st.subheader("Métricas Descritivas")
        st.write(metrics.compute_metrics(df))
        
        # Análises padrão
        num_cols = df.select_dtypes(include='number')
        if not num_cols.empty:
            st.subheader("Heatmap de Correlação")
            fig_corr = metrics.generate_correlation_heatmap(df)
            st.pyplot(fig_corr)
        
        if "idade" in df.columns and "salario" in df.columns:
            st.subheader("Gráfico de Dispersão: Idade vs. Salário")
            fig_scatter = metrics.generate_scatter_plot(df, "idade", "salario")
            st.pyplot(fig_scatter)
        
        if "salario" in df.columns:
            st.subheader("Boxplot de Salário")
            fig_box = metrics.generate_box_plot(df, "salario")
            st.pyplot(fig_box)
        
        if "idade" in df.columns:
            st.subheader("Histograma de Idade")
            fig_hist = metrics.generate_histogram(df, "idade", bins=30)
            st.pyplot(fig_hist)
        
        # Série Temporal: procura por coluna de data (ex.: 'data' ou 'date')
        date_cols = [col for col in df.columns if "data" in col.lower() or "date" in col.lower()]
        if date_cols:
            date_column = date_cols[0]
            if "valor_compra" in df.columns:
                value_column = "valor_compra"
            elif "salario" in df.columns:
                value_column = "salario"
            elif not num_cols.empty:
                value_column = num_cols.columns[0]
            else:
                value_column = None
            if value_column:
                st.subheader(f"Série Temporal: {date_column} vs. {value_column}")
                fig_ts = metrics.generate_time_series_plot(df, date_column, value_column)
                st.pyplot(fig_ts)
            else:
                st.info("Não há coluna numérica disponível para gerar a série temporal.")
        
        # --- Mapeamento de Variáveis Avançadas ---
        st.sidebar.header("Mapeamento de Variáveis Avançadas")
        produto_col = st.sidebar.selectbox("Coluna para Produto:", df.columns)
        pagamento_col = st.sidebar.selectbox("Coluna para Método de Pagamento:", df.columns)
        canal_col = st.sidebar.selectbox("Coluna para Canal de Origem:", df.columns)
        valor_col = st.sidebar.selectbox("Coluna para Valor da Compra:", df.columns)
        cliente_options = ["Nenhuma"] + list(df.columns)
        cliente_col = st.sidebar.selectbox("Coluna para Cliente ID (opcional):", cliente_options)
        if cliente_col == "Nenhuma":
            cliente_col = None
        
        # Análises Avançadas
        st.subheader("Produtos Mais Comprados")
        fig_produtos = metrics.generate_most_purchased_products_chart(df, produto_col)
        if fig_produtos:
            st.pyplot(fig_produtos)
        else:
            st.info("Não foi possível gerar o gráfico de produtos.")
        
        st.subheader("Método de Pagamento Mais Utilizado")
        fig_pagamento = metrics.generate_most_used_payment_method_chart(df, pagamento_col)
        if fig_pagamento:
            st.pyplot(fig_pagamento)
        else:
            st.info("Não foi possível gerar o gráfico de métodos de pagamento.")
        
        st.subheader("Tipos de Produtos por Canal de Origem")
        fig_canal_prod = metrics.generate_origin_channel_product_types_chart(df, canal_col, produto_col)
        if fig_canal_prod:
            st.pyplot(fig_canal_prod)
        else:
            st.info("Não foi possível gerar o gráfico de tipos de produtos por canal de origem.")
        
        st.subheader("Valor Total de Compras e Clientes por Canal de Origem")
        fig_canal_clientes = metrics.generate_origin_channel_customer_metrics_chart(df, canal_col, valor_col, cliente_col)
        if fig_canal_clientes:
            st.pyplot(fig_canal_clientes)
        else:
            st.info("Não foi possível gerar o gráfico de valor total de compras e clientes por canal de origem.")

if __name__ == "__main__":
    run_app()
