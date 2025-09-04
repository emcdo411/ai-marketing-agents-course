# bi_templates_runner.py
"""
BI runner:
1) Ask Claude to select the best template from the registry (enumeration).
2) Extract and validate params from the question (days, segment_id).
3) Bind params safely, execute SQL via SQLAlchemy.
4) Ask Claude for a concise exec explanation of the JSON payload.

No LLM-generated SQL is executed.
"""
from __future__ import annotations
import os, json, time
from typing import Dict, Any, Tuple

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

from course.week1.day1.anthropic_client import ClaudeClient
from sql_templates import TEMPLATES, list_templates
from safe_params import extract_days, extract_segment, validate_params

load_dotenv()
DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/leads_scored_segmentation.db")

SYSTEM_PICK = "You are a strict JSON classifier. Output ONLY valid JSON."
SYSTEM_EXPLAIN = "You are a concise executive analyst. Output plain text only."

def pick_template(question: str) -> str:
    """
    Use Claude to select a template from TEMPLATES (by name).
    """
    names = list(TEMPLATES.keys())
    listing = json.dumps(names)
    user = f"""
Return ONLY valid JSON with key: {{"template": one_of_names}}

where one_of_names ∈ {listing}

Question: {question}

Guidance:
- avg p1 by segment -> "avg_p1_by_segment"
- avg p1 by member rating -> "avg_p1_by_member_rating"
- counts per rating / how many per rating -> "count_by_member_rating"
- top / max purchase_frequency -> "top_purchase_frequency_by_segment"

Return: {{"template": "<name>"}}
"""
    client = ClaudeClient()
    raw = client.json_call(system=SYSTEM_PICK, user=user, max_tokens=200)
    try:
        return json.loads(raw)["template"]
    except Exception:
        # safe default
        return "avg_p1_by_segment"

def bind_and_run(template_name: str, params: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Bind params and execute the approved template. Returns (df, payload_dict)
    """
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    tpl = TEMPLATES[template_name]
    # We only use 'days' in these templates; segment_id can inform narrative later.
    bound = {"days": params.get("days")}
    eng = create_engine(DB_URL, future=True)
    with eng.connect() as c:
        df = pd.read_sql(tpl["sql"], c, params=bound)
    payload = {
        "template": template_name,
        "params": bound,
        "rows": df.to_dict(orient="records"),
    }
    return df, payload

def exec_bi(question: str) -> Dict[str, Any]:
    """
    End-to-end BI: template selection -> execution -> explanation
    """
    t0 = time.time()
    template_name = pick_template(question)
    days = extract_days(question)
    seg = extract_segment(question)
    params = validate_params({"days": days, "segment_id": seg})

    df, payload = bind_and_run(template_name, params)
    elapsed = time.time() - t0

    # Use Claude for a short exec explanation
    client = ClaudeClient()
    explanation = client.json_call(
        system=SYSTEM_EXPLAIN,
        user=(
            "Explain the BI result in <= 4 sentences for executives. "
            f"Question: {question}\n"
            f"Template: {template_name}\n"
            f"Params: {json.dumps(params)}\n"
            f"Data (JSON rows): {json.dumps(payload['rows'])}"
        ),
        max_tokens=300
    )

    return {
        "question": question,
        "template": template_name,
        "params": params,
        "latency_s": round(elapsed, 3),
        "rows": payload["rows"],
        "explanation": explanation.strip(),
    }
