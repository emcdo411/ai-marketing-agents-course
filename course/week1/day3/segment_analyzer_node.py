# segment_analyzer_node.py
"""
Claude-powered segment analyzer node.
- Reads a small JSON preview of the segment's rows.
- Returns: response, insights, summary_table (all JSON-safe strings).

Relies on:
  course/week1/day1/anthropic_client.py (ClaudeClient)
"""
import json
from typing import Dict, Any
from state_types import GraphState
from course.week1.day1.anthropic_client import ClaudeClient

SYSTEM = "You are a strict JSON generator. Only output valid JSON."

def segment_analyzer(state: GraphState) -> Dict[str, Any]:
    """
    LLM node that analyzes a segment preview and produces concise exec outputs.
    """
    user = f"""
Return ONLY valid JSON with keys:
{{
  "response": string,
  "insights": [string],
  "summary_table": [{{"metric": string, "value": string}}]
}}

Context:
- segment_id = {state.get('segment_id')}
- sample_rows (JSON list of dicts) = {state.get('sample_df_json', '[]')}

Constraints:
- "response": 3-5 sentences, executive tone.
- "insights": 4-6 bullets, crisp and factual.
- "summary_table": <= 6 rows, keys ["metric","value"] only.
- No extra keys, no prose outside JSON.
"""
    client = ClaudeClient()
    raw = client.json_call(system=SYSTEM, user=user, max_tokens=700)

    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {
            "response": raw,
            "insights": ["parse_error"],
            "summary_table": [{"metric": "status", "value": "unparsed"}],
        }

    response = str(parsed.get("response", ""))
    insights_list = parsed.get("insights", [])
    insights = "\n".join(insights_list) if isinstance(insights_list, list) else str(insights_list)
    table_json = json.dumps(parsed.get("summary_table", []), ensure_ascii=False)

    return {
        "response": response,
        "insights": insights,
        "summary_table": table_json,
        "chart_json": "{}",  # reserved for Day 6 charts
    }
