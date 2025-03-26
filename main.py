import sys
import pandas as pd
import metrics

def main():
    # Se o argumento "metrics" for passado, executa a geração de métricas a partir do CSV de exemplo
    if len(sys.argv) > 1 and sys.argv[1] == "metrics":
        csv_file = "base_compras_5000.csv"
        try:
            df = pd.read_csv(csv_file)
            print("Métricas Descritivas:")
            print(metrics.compute_metrics(df))
            
            # Utiliza as duas primeiras colunas para gerar o gráfico de dispersão, se possível
            colunas = df.columns.tolist()
            if len(colunas) >= 2:
                fig = metrics.generate_scatter_plot(df, colunas[0], colunas[1])
                # Exibe o gráfico (o método .show() abre uma janela com o gráfico, útil fora do Streamlit)
                fig.show()
            else:
                print("O CSV precisa de pelo menos duas colunas para gerar o gráfico de dispersão.")
        except Exception as e:
            print(f"Erro ao ler o CSV: {e}")
    else:
        print("Para rodar o dashboard interativo, utilize o comando:")
        print("   streamlit run app.py")
        print("Para gerar métricas via linha de comando, utilize:")
        print("   python main.py metrics")

if __name__ == "__main__":
    main()
