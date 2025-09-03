# 📘 Week 1 — Day 4
**Topic:** Router Node & Directed Flow (Claude + LangGraph)

---

## 🎯 Learning Objectives
- Build a **Claude-powered router** that classifies user questions by intent.
- Wire a **LangGraph** with **conditional edges** to BI / Product / Email / Analyst nodes.
- Use a **confidence threshold** and safe fallback to Analyst.
- Return **JSON-safe answers** suitable for UI or downstream agents.

---

## 🗂 Files in This Lesson
- `router_state.py` — Typed router state (question, intent, confidence, answer).
- `router_node.py` — Claude router (intent classification, confidence).
- `bi_node.py` — BI co-bot (sample DB query + concise explanation).
- `product_node.py` — Product co-bot (value props for a segment).
- `email_node.py` — Email co-bot (compliant, segment-aware draft).
- `analyst_node.py` — Analyst co-bot (summary/fallback).
- `build_router.py` — START → router → (BI/Product/Email/Analyst) → END.
- `run_router.py` — CLI runner (e.g., `python run_router.py --q "..."`).

> Re-uses **Day 1** Claude client: `course/week1/day1/anthropic_client.py`  
> Re-uses **Day 2** DB schema: `customer_features` in your `DATABASE_URL`.

---

## 🧩 Prereqs
- `.env`:
  ```ini
  ANTHROPIC_API_KEY=your_key
  CLAUDE_MODEL=claude-3-5-sonnet-latest
  DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
Day 2 customer_features table exists.

🧑‍💻 Install (if needed)
bash
Copy code
pip install anthropic langgraph pandas sqlalchemy python-dotenv
▶️ Run Examples
bash
Copy code
cd ai-marketing-agents-course/course/week1/day4

# BI-style question
python run_router.py --q "What is the average p1 by member_rating for the last 60 days?"

# Product-style question
python run_router.py --q "Which features should we highlight for high-frequency buyers?"

# Email-style question
python run_router.py --q "Draft a short outreach email to Segment 2 about renewals."

# Analyst/fallback
python run_router.py --q "Give me a quick summary of Segment 1 behavior."
You’ll see which node handled the question, along with the intent, confidence, and the answer.

🧠 Design Notes
Schema-first prompts and enumerated intents reduce drift.

Confidence threshold (e.g., < 0.6) falls back to Analyst for safety.

BI node demonstrates safe DB querying via SQLAlchemy + concise explanation with Claude (no arbitrary SQL from the model).

🔜 Next (Day 5 Preview)
Expand the BI Expert into a full template-driven SQL runner.

Add unit tests and evaluation harness for the router and co-bots.

python
Copy code

---

## 🧩 `course/week1/day4/router_state.py`

```python
# router_state.py
from typing_extensions import TypedDict

class RouterState(TypedDict):
    """
    Canonical state for routing user questions.
    """
    question: str       # original user question
    intent: str         # one of ["BI","Product","Email","Analyst","Other"]
    confidence: float   # 0..1
    answer: str         # human-readable answer (node-specific)
