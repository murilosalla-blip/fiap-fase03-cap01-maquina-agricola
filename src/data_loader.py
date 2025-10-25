from __future__ import annotations
import os
import glob
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def _autodiscover_csv() -> str | None:
    """
    Procura um CSV em data/ (prioriza nomes com 'sensores'), retornando o mais recente.
    """
    patterns = [
        "data/*sensores*.csv",
        "data/*.csv",
    ]
    candidates: list[str] = []
    for pat in patterns:
        candidates.extend(glob.glob(pat))
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]

def _make_synthetic_timestamp(df: pd.DataFrame) -> pd.Series:
    """
    Cria um timestamp sintético crescente para permitir séries temporais.
    Por padrão, usa row_id (minuto por linha). Se não houver row_id, usa o índice.
    """
    base = pd.Timestamp("2025-01-01 00:00:00")
    if "row_id" in df.columns:
        # normaliza para começar do zero
        start = int(pd.to_numeric(df["row_id"], errors="coerce").min() or 0)
        delta = pd.to_numeric(df["row_id"], errors="coerce") - start
        return base + pd.to_timedelta(delta, unit="m")
    # fallback: 1 minuto por linha
    return base + pd.to_timedelta(range(len(df)), unit="m")

def load_csv(path: str | None = None) -> pd.DataFrame:
    """
    Lê o CSV, normaliza cabeçalhos e mapeia colunas do seu esquema:
      - umidade <- umidade_pct
      - ph <- ph_sim
      - irrigacao <- irrigacao (normaliza LIGADA/DESLIGADA)
      - timestamp (sintético) a partir de row_id
    Mantém colunas auxiliares (n_ok, p_ok, k_ok, rain_mm, limiar_on, limiar_off, temp_c, ldr, etc.)
    """
    csv_path = path or os.getenv("CSV_PATH") or _autodiscover_csv()
    if not csv_path or not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV não encontrado. Verifique data/ ou configure CSV_PATH no .env. Recebido: {csv_path}")

    df = pd.read_csv(csv_path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Conversões básicas/seguras
    for col in ["row_id", "umidade_pct", "temp_c", "ldr", "ph_sim", "rain_mm", "pop_pct", "limiar_on", "limiar_off"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Mapeia para o padrão do dashboard
    if "umidade_pct" in df.columns:
        df["umidade"] = pd.to_numeric(df["umidade_pct"], errors="coerce")

    if "ph_sim" in df.columns:
        df["ph"] = pd.to_numeric(df["ph_sim"], errors="coerce")

    # Normaliza irrigação
    if "irrigacao" in df.columns:
        low = df["irrigacao"].astype(str).str.lower()
        df["irrigacao"] = low.map({
            "ligada": "ligada", "on": "ligada", "1": "ligada", "true": "ligada", "sim": "ligada", "ativo": "ligada", "yes": "ligada",
            "desligada": "desligada", "off": "desligada", "0": "desligada", "false": "desligada", "nao": "desligada", "inativo": "desligada", "no": "desligada"
        }).fillna(low)

    # Cria timestamp sintético se não existir
    if "timestamp" not in df.columns:
        df["timestamp"] = _make_synthetic_timestamp(df)
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Garante tipos numéricos das métricas principais
    for col in ["umidade", "ph"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Flags N/P/K como inteiros (0/1) se existirem
    for col in ["n_ok", "p_ok", "k_ok", "faltando"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    return df
