# safe_params.py
"""
Parse and validate common BI parameters from a question (or CLI flags).
We keep it conservative and explicit.
"""
from __future__ import annotations
from typing import Dict, Any, Optional
import re

DEFAULT_DAYS: Optional[int] = None  # None means no recency filter
MAX_DAYS = 365 * 3
SEG_MIN, SEG_MAX = -1, 1000

def extract_days(question: str) -> Optional[int]:
    """
    Very simple extractor for 'last N days' or 'last N day' phrases.
    """
    m = re.search(r"last\s+(\d{1,4})\s*day", question.lower())
    if not m:
        m = re.search(r"last\s+(\d{1,4})\s*days", question.lower())
    if m:
        days = int(m.group(1))
        if 1 <= days <= MAX_DAYS:
            return days
    return DEFAULT_DAYS

def extract_segment(question: str) -> Optional[int]:
    """
    Extract 'segment X' (integer). Returns None if not present.
    """
    m = re.search(r"segment\s+(-?\d+)", question.lower())
    if m:
        seg = int(m.group(1))
        if SEG_MIN <= seg <= SEG_MAX:
            return seg
    return None

def validate_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clamp or nullify unexpected values to safe defaults.
    """
    days = params.get("days")
    if days is not None:
        try:
            days = int(days)
            if days < 1 or days > MAX_DAYS:
                days = DEFAULT_DAYS
        except Exception:
            days = DEFAULT_DAYS

    seg = params.get("segment_id")
    if seg is not None:
        try:
            seg = int(seg)
            if seg < SEG_MIN or seg > SEG_MAX:
                seg = None
        except Exception:
            seg = None

    return {"days": days, "segment_id": seg}
