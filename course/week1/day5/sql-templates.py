## `course/week1/day5/sql_templates.py`

```python
# sql_templates.py
"""
Approved BI query templates (no free-form SQL).
All templates MUST:
  - Use bound parameters
  - Return compact, aggregatable results
"""

from __future__ import annotations
from typing import Dict, Any
from sqlalchemy.sql import text

# Template registry
# name -> (description, sqlalchemy.text template, required_params)
TEMPLATES: Dict[str, Dict[str, Any]] = {
    "avg_p1_by_segment": {
        "description": "Average p1 by segment (optionally filter by recency_days <= days)",
        "sql": text("""
            SELECT
                COALESCE(segment, -1) AS segment,
                AVG(p1) AS avg_p1,
                COUNT(*) AS n
            FROM customer_features
            WHERE (:days IS NULL OR recency_days <= :days)
            GROUP BY segment
            ORDER BY avg_p1 DESC
        """),
        "params": ["days"],  # nullable
    },
    "count_by_member_rating": {
        "description": "Row counts grouped by member_rating (optionally filter by days)",
        "sql": text("""
            SELECT
                member_rating,
                COUNT(*) AS n
            FROM customer_features
            WHERE (:days IS NULL OR recency_days <= :days)
            GROUP BY member_rating
            ORDER BY member_rating DESC
        """),
        "params": ["days"],  # nullable
    },
    "top_purchase_frequency_by_segment": {
        "description": "Top purchase_frequency by segment (optionally filter by days)",
        "sql": text("""
            SELECT
                COALESCE(segment, -1) AS segment,
                MAX(purchase_frequency) AS max_purchase_frequency,
                AVG(purchase_frequency) AS avg_purchase_frequency,
                COUNT(*) AS n
            FROM customer_features
            WHERE (:days IS NULL OR recency_days <= :days)
            GROUP BY segment
            ORDER BY max_purchase_frequency DESC
        """),
        "params": ["days"],  # nullable
    },
    "avg_p1_by_member_rating": {
        "description": "Average p1 grouped by member_rating (optionally filter by days)",
        "sql": text("""
            SELECT
                member_rating,
                AVG(p1) AS avg_p1,
                COUNT(*) AS n
            FROM customer_features
            WHERE (:days IS NULL OR recency_days <= :days)
            GROUP BY member_rating
            ORDER BY member_rating DESC
        """),
        "params": ["days"],  # nullable
    },
}

def list_templates() -> Dict[str, str]:
    return {k: v["description"] for k, v in TEMPLATES.items()}
