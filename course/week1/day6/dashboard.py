# dashboard.py
"""
Day 6 — Executive Dashboard with Streamlit
- Tabs for Router, BI, Product, Email, Analyst
- Calls Day 4 router (build_router_app)
- Calls Day 5 BI Expert (exec_bi)
"""

import os
import sys
import streamlit as st
import pandas as pd
import json

from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv()

# Import router + BI runner
from course.week1.day4.build_router import build_router_app
from course.week1.day5.bi_templates_runner import exec_bi

# Streamlit config
st.set_page_config(
    page_title="AI Marketing Agents Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open(Path(__file__).parent / "style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# -------------------
# Tabs
# -------------------
tabs = st.tabs(["🔀 Router", "📊 BI Expert", "📦 Product", "✉️ Email", "🧑‍💼 Analyst"])

# Router tab
with tabs[0]:
    st.header("🔀 Router Q&A")
    q = st.text_input("Ask me anything (router will decide intent):")
    if q:
        app = build_router_app()
        state = {"question": q, "intent": "", "confidence": 0.0, "answer": ""}
        result = app.invoke(state)

        st.subheader(f"Intent: {result.get('intent')} (conf: {result.get('confidence')})")

        if result.get("intent") == "BI":
            rows = result.get("rows", [])
            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
            st.markdown(f"**Summary:** {result.get('explanation','')}")
        else:
            answer = result.get("answer")
            if isinstance(answer, dict):
                st.json(answer)
            else:
                st.write(answer)

# BI tab
with tabs[1]:
    st.header("📊 BI Expert")
    q_bi = st.text_input("Ask a BI-specific question:")
    if q_bi:
        result = exec_bi(q_bi)
        df = pd.DataFrame(result.get("rows", []))
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        st.markdown(f"**Summary:** {result.get('explanation','')}")

# Product tab
with tabs[2]:
    st.header("📦 Product Expert")
    q_prod = st.text_input("Ask about product positioning:")
    if q_prod:
        app = build_router_app()
        result = app.invoke({"question": q_prod, "intent": "", "confidence": 0.0, "answer": ""})
        st.write(result.get("answer", ""))

# Email tab
with tabs[3]:
    st.header("✉️ Email Writer")
    q_email = st.text_input("Ask for an outreach email:")
    if q_email:
        app = build_router_app()
        result = app.invoke({"question": q_email, "intent": "", "confidence": 0.0, "answer": ""})
        st.write(result.get("answer", ""))

# Analyst tab
with tabs[4]:
    st.header("🧑‍💼 Analyst")
    q_analyst = st.text_input("Ask for an executive summary:")
    if q_analyst:
        app = build_router_app()
        result = app.invoke({"question": q_analyst, "intent": "", "confidence": 0.0, "answer": ""})
        st.write(result.get("answer", ""))
