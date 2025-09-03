# product_node.py
"""
Product co-bot:
- Maps likely segment needs to product value props / feature highlights
- Uses Claude to produce concise bullet points
"""
import json
import sys
from typing import Dict, Any

from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course.week1.day1.anthropic_client import ClaudeClient
from router_state import RouterState

SYSTEM = "You are a product marketer. Output only plain text; short bullets."

def product_node(state: RouterState) -> Dict[str, Any]:
    question = state.get("question", "")
    user = f"""
Create 5 concise bullet points with feature/value props to highlight.
Context: {question}
Audience: execs and SDRs. No fluff.
"""
    client = ClaudeClient()
    txt = client.json_call(system=SYSTEM, user=user, max_tokens=250)
    return {"answer": txt.strip()}

