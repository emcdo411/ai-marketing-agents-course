# dashboard_charts.py
"""
Day 7 — Streamlit dashboard with charts:
- BI tab renders table + Plotly figure + summary
- Router tab still supported via Day 4 (optional)
"""

import os
import sys
import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv()

# Reuse Day 4 router (optional tab)
from course.week1.day4.build_router import build_router_app

# Day 7 BI chart flow
from .bi_charts import run_bi_with_chart

st.set_page_config(page_title="AI Marketing Agents — Charts", layout="wide")

# Optional: reuse Day 6 CSS if you like
css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

tabs = st.tabs(["📊 BI + Charts", "🔀 Router (optional)"])

with tabs[0]:
    st.header("📊 BI + Charts")
    q = st.text_input("Ask a BI question (e.g., 'What's the average p1 by segment for the last 90 days?')",
                      "What's the average p1 by segment?")
    if q:
        df, fig, summary, meta = run_bi_with_chart(q)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Results Table")
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No rows returned.")
        with col2:
            st.subheader("Visualization")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Executive Summary**")
        st.write(summary)
        st.caption(f"Template: {meta['template']} • Params: {meta['params']} • Latency: {meta['latency_s']}s")

with tabs[1]:
    st.header("🔀 Router (Optional)")
    q = st.text_input("Free-form question (router decides intent):", "Draft a renewal email for Segment 2.")
    if q:
        app = build_router_app()
        result = app.invoke({"question": q, "intent": "", "confidence": 0.0, "answer": ""})
        st.json(result)
