# bi_node.py
"""
Day 4 BI node (compact JSON version):
Uses Day 5's exec_bi() to run safe, parameterized SQL via templates.
Returns structured JSON (rows, metadata, explanation) instead of one big string.
"""

import json
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

    Returns structured dict:
      - intent: "BI"
      - template: str
      - params: dict
      - latency_s: float
      - rows: list of dicts
      - explanation: str
    """
    question = state.get("question", "").strip() or "What's the average p1 by segment for the last 90 days?"

    result = exec_bi(question)

    return {
        "intent": "BI",
        "template": result.get("template"),
        "params": result.get("params"),
        "latency_s": result.get("latency_s"),
        "rows": result.get("rows", []),
        "explanation": result.get("explanation", ""),
    }
