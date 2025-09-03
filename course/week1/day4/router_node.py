# router_node.py
import json
import os
import sys
from typing import Dict, Any

from dotenv import load_dotenv
load_dotenv()

# Make repo root importable so we can use Day 1 Claude client
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]  # repo root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course.week1.day1.anthropic_client import ClaudeClient
from router_state import RouterState

INTENTS = ["BI", "Product", "Email", "Analyst", "Other"]
CONF_THRESHOLD = float(os.getenv("ROUTER_CONF_THRESHOLD", "0.6"))

SYSTEM = "You are a strict JSON router. Output ONLY valid JSON."

def router(state: RouterState) -> Dict[str, Any]:
    """
    Classify question into an intent with a confidence score.
    """
    user = f"""
Return ONLY valid JSON:

{{
  "intent": one of {INTENTS},
  "confidence": number (0..1),
  "rationale": string
}}

Question: {state.get('question')}

Routing Guidance:
- BI: metrics, data, performance, 'average', 'count', 'distribution'
- Product: features, value props, positioning for a segment
- Email: outreach copy, subject lines, CTAs, templates
- Analyst: summaries, segmentation, executive insights
- Other: anything else

Keep rationale very short.
"""
    client = ClaudeClient()
    raw = client.json_call(system=SYSTEM, user=user, max_tokens=350)

    try:
        parsed = json.loads(raw)
        intent = parsed.get("intent", "Analyst")
        confidence = float(parsed.get("confidence", 0.4))
    except Exception:
        intent, confidence = "Analyst", 0.4

    return {"intent": intent, "confidence": confidence, "answer": ""}
