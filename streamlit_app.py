from __future__ import annotations
import streamlit as st
import pandas as pd
from src.data_loader import load_csv
from src.logic.suggestions import basic_recommendations
from src.ui.components import kpi_row, timeseries, distributions

st.set_page_config(page_title="Máquina Agrícola — Dashboard", layout="wide")
st.title("🌱 Dashboard — Etapas de uma Máquina Agrícola")

# === Carregamento de dados (período completo) ===
try:
    df = load_csv()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar CSV: {e}")
    st.stop()

# Ordena por tempo, se existir
if "timestamp" in df.columns:
    df = df.sort_values("timestamp")

# === UI Principal ===
st.subheader("Indicadores")
kpi_row(df)

st.subheader("Séries temporais")
timeseries(df)

st.subheader("Distribuições")
distributions(df)

st.subheader("Sugestões")
for rec in basic_recommendations(df):
    st.write("• ", rec)

st.caption("FIAP — Fase 3, Capítulo 1 — Ir Além (MVP)")
