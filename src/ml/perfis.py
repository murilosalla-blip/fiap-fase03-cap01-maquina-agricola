from __future__ import annotations
import os
import pandas as pd
from src.ml.labeling import PERFIS, FEATURES, assign_label

DATA_PATH = "data/fase2_sensores_20251025_084829.csv"
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH)
    # Estatística descritiva das features da sua base
    desc_path = os.path.join(OUT_DIR, "ml_perfis_estatisticas_base.txt")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("=== Estatísticas descritivas — base Fase 2 ===\n\n")
        f.write(df[FEATURES].describe().to_string())
    print(f"[OK] {desc_path}")

    # Relatório dos perfis ideais
    perfis_path = os.path.join(OUT_DIR, "ml_perfis_ideais.txt")
    with open(perfis_path, "w", encoding="utf-8") as f:
        f.write("=== Perfis ideais (faixas) — milho, soja, café ===\n\n")
        for cult, ranges in PERFIS.items():
            f.write(f"[{cult.upper()}]\n")
            for k, (lo, hi) in ranges.items():
                f.write(f" - {k}: {lo} a {hi}\n")
            f.write("\n")
    print(f"[OK] {perfis_path}")

    # Rotulagem sintética e contagem resultante
    df["label"] = df.apply(lambda r: assign_label(r), axis=1)
    counts = df["label"].value_counts()
    dist_path = os.path.join(OUT_DIR, "ml_perfis_rotulos_sinteticos.txt")
    with open(dist_path, "w", encoding="utf-8") as f:
        f.write("=== Distribuição de rótulos sintéticos gerados a partir dos perfis ===\n\n")
        f.write(counts.to_string())
        f.write("\n")
    print(f"[OK] {dist_path}")

    # Salva um CSV auxiliar com a coluna label (não altera seu arquivo original)
    out_csv = os.path.join(OUT_DIR, "fase2_sensores_rotulado.csv")
    df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"[OK] Base rotulada (auxiliar): {out_csv}")

if __name__ == "__main__":
    main()
