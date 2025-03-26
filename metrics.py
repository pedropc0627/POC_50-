import pandas as pd
import matplotlib.pyplot as plt

def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna as métricas descritivas do DataFrame.
    """
    return df.describe()

def generate_scatter_plot(df: pd.DataFrame, coluna_x: str, coluna_y: str):
    """
    Gera um gráfico de dispersão para as colunas especificadas.
    """
    fig, ax = plt.subplots()
    ax.scatter(df[coluna_x], df[coluna_y])
    ax.set_xlabel(coluna_x)
    ax.set_ylabel(coluna_y)
    ax.set_title(f'Gráfico de Dispersão: {coluna_x} vs. {coluna_y}')
    return fig

def generate_correlation_heatmap(df: pd.DataFrame):
    """
    Gera um heatmap de correlação para as variáveis numéricas do DataFrame.
    """
    numeric_df = df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.matshow(corr, cmap='coolwarm')
    fig.colorbar(cax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticklabels(corr.columns)
    ax.set_title("Heatmap de Correlação", pad=20)
    return fig

def generate_box_plot(df: pd.DataFrame, column: str):
    """
    Gera um boxplot para a coluna especificada.
    """
    fig, ax = plt.subplots()
    ax.boxplot(df[column].dropna())
    ax.set_title(f'Boxplot de {column}')
    ax.set_ylabel(column)
    return fig

def generate_histogram(df: pd.DataFrame, column: str, bins: int = 30):
    """
    Gera um histograma para a coluna especificada.
    """
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=bins, edgecolor='black')
    ax.set_title(f'Histograma de {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Frequência')
    return fig

def generate_time_series_plot(df: pd.DataFrame, date_column: str, value_column: str):
    """
    Gera um gráfico de série temporal agregando os valores da coluna numérica por data.
    Converte a coluna de data para datetime, se necessário.
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df = df.dropna(subset=[date_column])
    
    df_sorted = df.sort_values(date_column)
    aggregated = df_sorted.groupby(date_column)[value_column].sum()
    
    fig, ax = plt.subplots()
    ax.plot(aggregated.index, aggregated.values)
    ax.set_xlabel("Data")
    ax.set_ylabel(value_column)
    ax.set_title(f"Série Temporal de {value_column}")
    return fig

def generate_most_purchased_products_chart(df: pd.DataFrame, produto_col: str):
    """
    Gera um gráfico de barras dos 10 produtos mais comprados,
    utilizando a coluna definida em produto_col.
    """
    if produto_col not in df.columns:
        return None
    counts = df[produto_col].value_counts().head(10)
    fig, ax = plt.subplots()
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Top 10 Produtos Mais Comprados")
    ax.set_xlabel("Produto")
    ax.set_ylabel("Frequência")
    return fig

def generate_most_used_payment_method_chart(df: pd.DataFrame, pagamento_col: str):
    """
    Gera um gráfico de barras dos métodos de pagamento mais utilizados,
    utilizando a coluna definida em pagamento_col.
    """
    if pagamento_col not in df.columns:
        return None
    counts = df[pagamento_col].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Métodos de Pagamento Mais Utilizados")
    ax.set_xlabel("Método de Pagamento")
    ax.set_ylabel("Frequência")
    return fig

def generate_origin_channel_product_types_chart(df: pd.DataFrame, canal_col: str, produto_col: str):
    """
    Gera um gráfico que mostra, para cada canal de origem, a quantidade
    de produtos distintos comprados, utilizando as colunas definidas.
    """
    if canal_col not in df.columns or produto_col not in df.columns:
        return None
    grouped = df.groupby(canal_col)[produto_col].nunique()
    fig, ax = plt.subplots()
    grouped.plot(kind='bar', ax=ax)
    ax.set_title("Tipos de Produtos por Canal de Origem")
    ax.set_xlabel("Canal de Origem")
    ax.set_ylabel("Número de Produtos Únicos")
    return fig

def generate_origin_channel_customer_metrics_chart(df: pd.DataFrame, canal_col: str, valor_col: str, cliente_col: str = None):
    """
    Gera um gráfico que compara canais de origem em relação à soma dos valores de compra
    e, se informado, o número de clientes únicos.
    """
    if canal_col not in df.columns or valor_col not in df.columns:
        return None
    valor_agg = df.groupby(canal_col)[valor_col].sum()
    fig, ax = plt.subplots()
    valor_agg.plot(kind='bar', ax=ax, color='green')
    ax.set_title("Valor Total de Compras por Canal de Origem")
    ax.set_xlabel("Canal de Origem")
    ax.set_ylabel("Valor Total")
    if cliente_col and cliente_col in df.columns:
        clientes = df.groupby(canal_col)[cliente_col].nunique()
        ax2 = ax.twinx()
        clientes.plot(kind='line', marker='o', ax=ax2, color='blue', label="Clientes Únicos")
        ax2.set_ylabel("Número de Clientes Únicos")
        ax2.legend(loc="upper right")
    return fig
