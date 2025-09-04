# bi_node.py
"""
Day 4 BI node (replacement):
Delegates BI questions to the Day 5 template-driven runner (exec_bi),
which selects an approved SQL template, binds params safely, runs it,
and returns rows + a concise executive explanation.

Requires:
  - course/week1/day5/bi_templates_runner.py (exec_bi)
  - DATABASE_URL in .env
  - Anthropic API vars for Claude explanation
"""

import json
import os
import sys
from typing import Dict, Any

# Ensure repo root on path (so Day 5 modules resolve when run from Day 4)
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course.week1.day5.bi_templates_runner import exec_bi
from router_state import RouterState


def bi_node(state: RouterState) -> Dict[str, Any]:
    """
    Expects in state:
      - question: str

    Returns:
      - answer: str (human-readable)
      - rows_json: str (JSON array of result rows)
      - template: str
      - params: dict
      - latency_s: float
    """
    question = state.get("question", "").strip() or "What's the average p1 by segment for the last 90 days?"

    result = exec_bi(question)
    rows_json = json.dumps(result.get("rows", []), ensure_ascii=False)

    answer = (
        "BI — Template-driven result\n"
        f"Template: {result.get('template')}\n"
        f"Params: {json.dumps(result.get('params', {}), ensure_ascii=False)}\n"
        f"Latency (s): {result.get('latency_s')}\n\n"
        f"Rows (preview): {rows_json[:800]}\n\n"
        f"{result.get('explanation','')}"
    )

    return {
        "answer": answer,
        "rows_json": rows_json,
        "template": result.get("template"),
        "params": result.get("params"),
        "latency_s": result.get("latency_s"),
    }
