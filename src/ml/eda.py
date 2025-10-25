import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/fase2_sensores_20251025_084829.csv"
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    print("== EDA | fase2_sensores ==")
    
    # Carregar base
    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print(f"[ERRO] Não consegui carregar a base: {e}")
        return

    print(f"[INFO] Linhas: {len(df)} | Colunas: {list(df.columns)}")

    # -------- Gráficos --------
    # 1) Histograma de variáveis contínuas
    cont_vars = ["umidade_pct", "temp_c", "ph_sim", "rain_mm"]
    df[cont_vars].hist(bins=20, figsize=(10,6))
    plt.suptitle("Distribuição - Variáveis Contínuas")
    plt.savefig(f"{OUT_DIR}/eda_histogramas.png")
    plt.close()
    print("[OK] eda_histogramas.png")

    # 2) Boxplots de umidade e temperatura
    plt.figure(figsize=(8,5))
    sns.boxplot(data=df[["umidade_pct","temp_c"]])
    plt.title("Boxplots - Umidade e Temperatura")
    plt.savefig(f"{OUT_DIR}/eda_boxplots.png")
    plt.close()
    print("[OK] eda_boxplots.png")

    # 3) Correlação entre variáveis numéricas
    plt.figure(figsize=(8,6))
    sns.heatmap(df[cont_vars].corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Matriz de Correlação")
    plt.savefig(f"{OUT_DIR}/eda_correlacao.png")
    plt.close()
    print("[OK] eda_correlacao.png")

    # 4) Distribuição de status de irrigação
    plt.figure(figsize=(6,4))
    df["irrigacao"].value_counts().plot(kind="bar")
    plt.title("Distribuição - Status Irrigação")
    plt.ylabel("Frequência")
    plt.savefig(f"{OUT_DIR}/eda_irrigacao.png")
    plt.close()
    print("[OK] eda_irrigacao.png")

    # 5) Dispersão pH x Umidade
    plt.figure(figsize=(7,5))
    sns.scatterplot(x="ph_sim", y="umidade_pct", hue="irrigacao", data=df)
    plt.title("Dispersão pH vs Umidade")
    plt.savefig(f"{OUT_DIR}/eda_ph_umidade.png")
    plt.close()
    print("[OK] eda_ph_umidade.png")

    print("[FINALIZADO] EDA concluída. Imagens salvas em assets/")

if __name__ == "__main__":
    main()
