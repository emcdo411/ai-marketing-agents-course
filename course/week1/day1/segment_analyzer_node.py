# segment_analyzer_node.py
"""
Minimal LangGraph demo for Day 1:
START -> segment_analyzer -> END

- Calls Claude (via anthropic_client.ClaudeClient)
- Expects strict JSON back (response, insights, summary_table)
- Returns a clean dict you can render in Streamlit later
"""

import json
import pandas as pd
from typing import Dict, Any
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

# Local Day 1 client wrapper
from anthropic_client import ClaudeClient


# --------- Graph State ---------
class GS(TypedDict):
    """State passed through the graph."""
    segment_id: int
    sample_df_json: str   # JSON preview of rows
    response: str         # narrative
    insights: str         # bullets (string with newlines)
    summary_table: str    # JSON string list[{"metric","value"}]


# --------- Node Implementation ---------
def segment_analyzer(state: GS) -> Dict[str, Any]:
    """
    Ask Claude for an exec-ready summary of a segment.
    Enforce JSON so downstream code is reliable.
    """
    client = ClaudeClient()

    user = f"""
Return ONLY valid JSON matching:
{{
  "response": string,
  "insights": [string],
  "summary_table": [{{"metric": string, "value": string}}]
}}

Context:
- segment_id = {state.get('segment_id')}
- sample_rows = {state.get('sample_df_json', '[]')}

Constraints:
- Keep "response" to 3-5 concise sentences (executive tone).
- "insights": 4-6 bullets, short & specific.
- "summary_table": max 5 rows with ["metric","value"].
- No extra keys, no prose outside JSON.
"""

    raw = client.json_call(
        system="You are a strict JSON generator. Only output valid JSON.",
        user=user,
        max_tokens=700,
    )

    # Parse JSON safely
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {
            "response": raw,
            "insights": ["parse_error"],
            "summary_table": [{"metric": "status", "value": "unparsed"}],
        }

    # Normalize/serialize for UI safety
    response = str(parsed.get("response", ""))
    insights_list = parsed.get("insights", [])
    insights = "\n".join(insights_list) if isinstance(insights_list, list) else str(insights_list)
    table = parsed.get("summary_table", [])
    table_json = json.dumps(table, ensure_ascii=False)

    return {
        "response": response,
        "insights": insights,
        "summary_table": table_json,
    }


# --------- Build & Compile Graph ---------
def build_app():
    g = StateGraph(GS)
    g.add_node("segment_analyzer", segment_analyzer)
    g.add_edge(START, "segment_analyzer")
    g.add_edge("segment_analyzer", END)
    return g.compile()


# --------- CLI Demo ---------
if __name__ == "__main__":
    # Tiny demo dataframe (replace with your real preview later)
    df = pd.DataFrame([
        {"user_email": "a@example.com", "p1": 0.83, "member_rating": 4.7, "purchase_frequency": 5},
        {"user_email": "b@example.com", "p1": 0.35, "member_rating": 3.9, "purchase_frequency": 2},
        {"user_email": "c@example.com", "p1": 0.62, "member_rating": 4.2, "purchase_frequency": 3},
    ])

    app = build_app()
    result = app.invoke({
        "segment_id": 2,
        "sample_df_json": df.head(5).to_json(orient="records"),
        "response": "",
        "insights": "",
        "summary_table": "[]",
    })

    print("\n=== RESPONSE ===\n", result["response"])
    print("\n=== INSIGHTS ===\n", result["insights"])
    print("\n=== SUMMARY TABLE ===\n", result["summary_table"])
