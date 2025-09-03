# analyst_node.py
"""
Analyst co-bot:
- Summary/fallback node for low-confidence routes or generic analysis prompts
"""
import sys
from typing import Dict, Any

from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course.week1.day1.anthropic_client import ClaudeClient
from router_state import RouterState

SYSTEM = "You are an executive analyst. Output plain text only."

def analyst_node(state: RouterState) -> Dict[str, Any]:
    question = state.get("question", "")
    user = f"""
Provide a crisp 3-5 sentence executive summary addressing:
- what the user is likely after
- the minimal data you'd pull next
- likely next best action
Question: {question}
"""
    client = ClaudeClient()
    txt = client.json_call(system=SYSTEM, user=user, max_tokens=300)
    return {"answer": txt.strip()}
