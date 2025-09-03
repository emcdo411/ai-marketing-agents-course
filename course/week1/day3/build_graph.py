# build_graph.py
"""
Compiles START -> segment_analyzer -> END and provides helpers to
fetch a sample from the DB and invoke the graph.

Usage (from other modules):
    from build_graph import invoke_segment_analysis
    result = invoke_segment_analysis(segment_id=2, limit=50)
"""
import os
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Dict, Any

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from state_types import GraphState
from segment_analyzer_node import segment_analyzer

load_dotenv()
DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/leads_scored_segmentation.db")

def sample_segment_rows(segment_id: int, limit: int = 50) -> pd.DataFrame:
    """
    Pull a small preview of rows for the given segment_id from customer_features.
    If you don't have a 'segment' column yet, sample by heuristics or return head().
    """
    eng = create_engine(DB_URL, future=True)
    with eng.connect() as c:
        # Try to sample by segment column if present, else just take head()
        cols = [r[1] for r in c.execute(text("PRAGMA table_info(customer_features)"))] if DB_URL.startswith("sqlite") \
               else []
        has_segment = "segment" in cols

        if has_segment:
            q = text("SELECT * FROM customer_features WHERE segment = :sid LIMIT :lim")
            df = pd.read_sql(q, c, params={"sid": segment_id, "lim": limit})
        else:
            q = text("SELECT * FROM customer_features LIMIT :lim")
            df = pd.read_sql(q, c, params={"lim": limit})
    return df

def build_app():
    g = StateGraph(GraphState)
    g.add_node("segment_analyzer", segment_analyzer)
    g.add_edge(START, "segment_analyzer")
    g.add_edge("segment_analyzer", END)
    return g.compile()

def invoke_segment_analysis(segment_id: int, limit: int = 50) -> Dict[str, Any]:
    """
    Orchestrates:
      - preview fetch from DB
      - graph build and invoke
      - returns dict with keys in GraphState
    """
    df = sample_segment_rows(segment_id=segment_id, limit=limit)
    sample_json = df.to_json(orient="records")

    app = build_app()
    state: GraphState = {
        "segment_id": segment_id,
        "sample_df_json": sample_json,
        "response": "",
        "insights": "",
        "summary_table": "[]",
        "chart_json": "{}",
    }
    return app.invoke(state)
