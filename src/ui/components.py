from __future__ import annotations
import pandas as pd
import streamlit as st
import plotly.express as px

def _fmt_num(x):
    return "—" if x is None else f"{x:.2f}"

def _fmt_pct(x):
    return "—" if x is None else f"{x:.0f}%"

def kpi_row(df: pd.DataFrame):
    """
    KPIs:
      - Umidade média (%)
      - Fósforo: se houver df['p'], usa média; senão, % a partir de p_ok
      - Potássio: se houver df['k'], usa média; senão, % a partir de k_ok
      - pH médio
    """
    c1, c2, c3, c4 = st.columns(4)

    # Umidade
    umid = df["umidade"].mean() if "umidade" in df.columns else None
    c1.metric("Umidade média (%)", _fmt_num(umid))

    # Fósforo
    p_mean = df["p"].mean() if "p" in df.columns else None
    if p_mean is None and "p_ok" in df.columns:
        p_ok_pct = float(df["p_ok"].mean() * 100.0)
        c2.metric("Fósforo (%)", _fmt_pct(p_ok_pct))
    else:
        c2.metric("Fósforo médio (P)", _fmt_num(p_mean))

    # Potássio
    k_mean = df["k"].mean() if "k" in df.columns else None
    if k_mean is None and "k_ok" in df.columns:
        k_ok_pct = float(df["k_ok"].mean() * 100.0)
        c3.metric("Potássio (%)", _fmt_pct(k_ok_pct))
    else:
        c3.metric("Potássio médio (K)", _fmt_num(k_mean))

    # pH
    ph = df["ph"].mean() if "ph" in df.columns else None
    c4.metric("pH médio", _fmt_num(ph))

def timeseries(df: pd.DataFrame):
    if "timestamp" not in df.columns:
        st.info("Sem coluna de tempo para séries temporais.")
        return
    cols = [c for c in ["umidade", "ph"] if c in df.columns]
    if not cols:
        st.info("Sem colunas numéricas esperadas (umidade, ph).")
        return
    long_df = (
        df.dropna(subset=["timestamp"])
          .sort_values("timestamp")
          .melt(id_vars=["timestamp"], value_vars=cols, var_name="variavel", value_name="valor")
    )
    if long_df.empty:
        st.info("Sem dados válidos para série temporal.")
        return
    fig = px.line(long_df, x="timestamp", y="valor", color="variavel", markers=True)
    st.plotly_chart(fig, use_container_width=True)

def distributions(df: pd.DataFrame):
    cols = [c for c in ["umidade", "ph", "temp_c"] if c in df.columns]
    if not cols:
        return
    for c in cols:
        st.subheader(f"Distribuição — {c.upper()}")
        fig = px.histogram(df, x=c, nbins=30)
        st.plotly_chart(fig, use_container_width=True)
