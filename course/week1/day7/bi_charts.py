# bi_charts.py
"""
Thin wrapper that calls Day 5's exec_bi(question) and returns:
- df (pandas)
- fig (plotly figure suited for the chosen template)
- explanation (Claude's exec summary)

If the template is unknown, we fall back to a generic bar chart.
"""

from __future__ import annotations
from typing import Tuple
import pandas as pd
import plotly.express as px

# Import the BI runner from Day 5
from course.week1.day5.bi_templates_runner import exec_bi
from .chart_utils import bar_from_rows


def _figure_for_template(template: str, rows: list[dict]):
    t = template or ""
    if t == "avg_p1_by_segment":
        return bar_from_rows(rows, x="segment", y="avg_p1", title="Average p1 by Segment")
    if t == "avg_p1_by_member_rating":
        return bar_from_rows(rows, x="member_rating", y="avg_p1", title="Average p1 by Member Rating")
    if t == "count_by_member_rating":
        return bar_from_rows(rows, x="member_rating", y="n", title="Users per Member Rating")
    if t == "top_purchase_frequency_by_segment":
        return bar_from_rows(rows, x="segment", y="max_purchase_frequency", title="Top Purchase Frequency by Segment")

    # fallback: pick first numeric for y
    df = pd.DataFrame(rows)
    if df.empty:
        return px.scatter(title="No data", template="plotly_dark")
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    y = numeric_cols[0] if numeric_cols else df.columns[-1]
    x = [c for c in df.columns if c != y][0]
    return bar_from_rows(rows, x=x, y=y, title=f"{template or 'Metric'} by {x}")


def run_bi_with_chart(question: str) -> Tuple[pd.DataFrame, "plotly.graph_objs.Figure", str, dict]:
    """
    Returns: df, fig, explanation, meta
    meta = {"template": str, "params": dict, "latency_s": float}
    """
    result = exec_bi(question)
    rows = result.get("rows", [])
    df = pd.DataFrame(rows)
    fig = _figure_for_template(result.get("template"), rows)
    return df, fig, result.get("explanation", ""), {
        "template": result.get("template"),
        "params": result.get("params"),
        "latency_s": result.get("latency_s"),
    }
