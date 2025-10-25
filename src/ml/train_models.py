import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Caminhos
DATA_PATH = "assets/fase2_sensores_rotulado.csv"
REPORT_CSV = "assets/ml_model_report.csv"
REPORT_TXT = "assets/ml_model_comparativo.txt"

def load_and_prepare():
    df = pd.read_csv(DATA_PATH)

    # Mantém apenas as features principais
    FEATURES = ["umidade_pct", "temp_c", "ph_sim", "rain_mm", "n_ok", "p_ok", "k_ok"]
    TARGET = "label"

    # Converte para numérico
    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=FEATURES+[TARGET])

    X = df[FEATURES]
    y = df[TARGET]

    # Normaliza
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Codifica rótulos
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    return X_scaled, y_enc, le, FEATURES

def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    modelos = {
        "LogisticRegression": LogisticRegression(max_iter=500),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "SVM": SVC(kernel="rbf", probability=True),
        "GradientBoosting": GradientBoostingClassifier(random_state=42)
    }

    resultados = []
    melhor_acc = 0
    melhor_modelo = None

    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        resultados.append((nome, acc))

        # Salva relatório detalhado por modelo
        with open(f"assets/ml_{nome}_report.txt", "w", encoding="utf-8") as f:
            f.write(f"== {nome} ==\n")
            f.write(f"Acurácia: {acc:.4f}\n\n")
            f.write("Classification Report:\n")
            f.write(classification_report(y_test, y_pred))
            f.write("\nMatriz de Confusão:\n")
            f.write(str(confusion_matrix(y_test, y_pred)))

        if acc > melhor_acc:
            melhor_acc = acc
            melhor_modelo = (nome, modelo, y_pred, y_test)

    # Relatório consolidado
    df_result = pd.DataFrame(resultados, columns=["Modelo", "Acuracia"])
    df_result.to_csv(REPORT_CSV, index=False)

    with open(REPORT_TXT, "w", encoding="utf-8") as f:
        f.write("== Comparação de Modelos ==\n")
        for nome, acc in resultados:
            f.write(f"{nome}: {acc:.4f}\n")
        f.write(f"\nMelhor modelo: {melhor_modelo[0]} (Acurácia {melhor_acc:.4f})\n")

    print("[FINALIZADO] Modelos treinados e avaliados.")
    print(f"[OK] Resultados em {REPORT_CSV} e {REPORT_TXT}")

def main():
    X, y, le, FEATURES = load_and_prepare()
    train_and_evaluate(X, y)

if __name__ == "__main__":
    main()
