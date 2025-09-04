## 🧩 `course/week1/day7/chart_utils.py`

```python
# chart_utils.py
"""
Utilities to convert BI JSON rows (list[dict]) into Plotly figures.

Rules:
- Prefer "plotly_dark" template for a cohesive exec look.
- Do not hardcode colors; let Plotly pick sensible defaults.
- Provide safe fallbacks when expected columns are missing.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Tuple
import pandas as pd
import plotly.express as px


def _as_df(rows: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(rows or [])


def _pick_numeric(df: pd.DataFrame) -> Optional[str]:
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            return c
    return None


def bar_from_rows(
    rows: List[Dict],
    x: str,
    y: str,
    title: str,
    category_order: Optional[Tuple[str, List]] = None,
):
    df = _as_df(rows)
    if df.empty:
        return px.scatter(title="No data")

    # Safeguards
    if x not in df.columns:
        x = df.columns[0]
    if y not in df.columns:
        y = _pick_numeric(df) or df.columns[-1]

    fig = px.bar(df, x=x, y=y, title=title, template="plotly_dark")
    if category_order and category_order[0] in df.columns:
        fig.update_layout(xaxis={"categoryorder": "array", "categoryarray": category_order[1]})
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig


def line_from_rows(
    rows: List[Dict],
    x: str,
    y: str,
    title: str,
):
    df = _as_df(rows)
    if df.empty:
        return px.scatter(title="No data")
    if x not in df.columns:
        x = df.columns[0]
    if y not in df.columns:
        y = _pick_numeric(df) or df.columns[-1]
    fig = px.line(df, x=x, y=y, markers=True, title=title, template="plotly_dark")
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig


def scatter_from_rows(
    rows: List[Dict],
    x: str,
    y: str,
    title: str,
):
    df = _as_df(rows)
    if df.empty:
        return px.scatter(title="No data")
    if x not in df.columns:
        x = df.columns[0]
    if y not in df.columns:
        y = _pick_numeric(df) or df.columns[-1]
    fig = px.scatter(df, x=x, y=y, title=title, template="plotly_dark")
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig
