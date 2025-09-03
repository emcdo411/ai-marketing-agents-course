# bi_node.py
"""
BI co-bot:
- Runs a SAFE, predefined aggregation on customer_features
- Asks Claude to explain results in 3-4 concise sentences
"""
import json
import os
import sys
from typing import Dict, Any

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/leads_scored_segmentation.db")

from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from course.week1.day1.anthropic_client import ClaudeClient
from router_state import RouterState

def bi_node(state: RouterState) -> Dict[str, Any]:
    """
    Example BI: average p1 by member_rating over the entire table (safe).
    Extend with date filters in Day 5.
    """
    eng = create_engine(DB_URL, future=True)
    with eng.connect() as c:
        df = pd.read_sql(text("""
            SELECT member_rating, AVG(p1) AS avg_p1, COUNT(*) AS n
            FROM customer_features
            GROUP BY member_rating
            ORDER BY member_rating DESC
        """), c)

    payload = df.to_dict(orient="records")
    client = ClaudeClient()
    explain = client.json_call(
        system="You are a concise executive analyst. Output plain text (no JSON).",
        user=f"Explain these BI results in <= 4 sentences:\n{json.dumps(payload)}",
        max_tokens=300
    )

    answer = (
        "BI — Average p1 by member_rating\n"
        f"Data: {json.dumps(payload, ensure_ascii=False)}\n\n"
        f"{explain}"
    )
    return {"answer": answer}
