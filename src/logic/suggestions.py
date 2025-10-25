from __future__ import annotations
import pandas as pd

def _mean_or_none(df: pd.DataFrame, col: str):
    return df[col].dropna().mean() if col in df.columns else None

def basic_recommendations(df: pd.DataFrame) -> list[str]:
    recs: list[str] = []
    if df.empty:
        return ["Sem dados para sugerir ações."]

    umidade = _mean_or_none(df, "umidade")
    ph = _mean_or_none(df, "ph")
    rain = _mean_or_none(df, "rain_mm")
    lim_on = _mean_or_none(df, "limiar_on")
    lim_off = _mean_or_none(df, "limiar_off")

    # 1) Umidade
    if umidade is not None:
        if umidade < 30:
            recs.append("Umidade média baixa (<30%). Avaliar irrigação e cobertura do solo.")
        elif umidade > 70:
            recs.append("Umidade média alta (>70%). Evitar encharcamento; revisar drenagem.")
        else:
            recs.append("Umidade média em faixa adequada (30–70%).")

    # 2) pH
    if ph is not None:
        if ph < 5.5:
            recs.append("pH médio ácido (<5.5). Considerar calagem conforme recomendação técnica.")
        elif ph > 7.0:
            recs.append("pH médio alcalino (>7.0). Avaliar gessagem/enxofre conforme solo/cultura.")
        else:
            recs.append("pH médio adequado (5.5–7.0) para a maioria das culturas.")

    # 3) Nutrientes (flags 0/1): se houver muitos 0, sugerir atenção
    for nutr, label in [("n_ok", "Nitrogênio (N)"), ("p_ok", "Fósforo (P)"), ("k_ok", "Potássio (K)")]:
        if nutr in df.columns:
            frac_ok = df[nutr].mean()  # 0..1
            if frac_ok < 0.8:
                recs.append(f"{label} fora do ideal em várias leituras. Revisar adubação ({label}).")

    # 4) Chuva / Irrigação
    if rain is not None and rain > 0.0 and umidade is not None and umidade > 60:
        recs.append("Chuva registrada e umidade alta. Evitar irrigação para não encharcar o solo.")

    # 5) Limiar on/off — se existirem, contextualize
    if lim_on is not None and lim_off is not None:
        recs.append(f"Limiar de irrigação configurado: ON {lim_on:.1f}% | OFF {lim_off:.1f}%.")

    # 6) Status de irrigação mais recente
    if "irrigacao" in df.columns:
        last = df.sort_values("timestamp").iloc[-1] if "timestamp" in df.columns else df.iloc[-1]
        status = str(last.get("irrigacao", "desconhecido")).lower()
        recs.append(f"Status de irrigação mais recente: {status}.")

    return recs or ["Sem recomendações específicas."]
