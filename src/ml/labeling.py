from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Dict, Tuple

# Perfis ideais (faixas) — valores sintetizados a partir de referências agronômicas comuns
# Ajustados para a sua base: umidade_pct, temp_c, ph_sim, rain_mm
PERFIS = {
    "milho": {
        "umidade_pct": (45, 65),
        "temp_c": (24, 30),
        "ph_sim": (5.5, 7.0),
        "rain_mm": (2, 20),
    },
    "soja": {
        "umidade_pct": (50, 70),
        "temp_c": (22, 28),
        "ph_sim": (6.0, 7.5),
        "rain_mm": (2, 25),
    },
    "cafe": {
        "umidade_pct": (60, 80),
        "temp_c": (18, 24),
        "ph_sim": (5.0, 6.5),
        "rain_mm": (5, 30),
    },
}

FEATURES = ["umidade_pct", "temp_c", "ph_sim", "rain_mm"]

def _range_distance(val: float, low: float, high: float) -> float:
    """
    Distância 0 se dentro do intervalo [low, high].
    Fora da faixa: distância proporcional à borda mais próxima.
    """
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return 1.0  # penalização máxima
    if val < low:
        return (low - val) / (high - low if high > low else 1.0)
    if val > high:
        return (val - high) / (high - low if high > low else 1.0)
    return 0.0

def score_row_to_profile(row: dict, perfil: Dict[str, Tuple[float, float]]) -> float:
    """
    Score médio de distâncias normalizadas às faixas ideais.
    Quanto MENOR, melhor (0 = perfeito).
    """
    dists = []
    for col in FEATURES:
        low, high = perfil[col]
        d = _range_distance(float(row.get(col, float("nan"))), low, high)
        dists.append(d)
    # bônus leve se N/P/K estiverem OK (reduz a distância)
    bonus = 0.0
    for f in ["n_ok", "p_ok", "k_ok"]:
        v = row.get(f, None)
        if v in (1, "1", True, "SIM", "Sim", "sim"):
            bonus -= 0.03  # pequeno bônus por nutriente ok
    return max(0.0, sum(dists) / len(dists) + bonus)

def assign_label(row: dict) -> str:
    """
    Atribui a cultura com menor score (melhor aderência ao perfil).
    """
    scores = {cult: score_row_to_profile(row, PERFIS[cult]) for cult in PERFIS}
    return min(scores.items(), key=lambda kv: kv[1])[0]
