# 📘 Week 1 — Day 5
**Topic:** BI Expert — Template-Driven SQL, Safe Params, and Evaluation Harness

---

## 🎯 Learning Objectives
- Map natural-language BI questions → **approved SQL templates** (no free-form SQL).
- Validate and **bind parameters** (segment, date window) safely.
- Execute with **SQLAlchemy** and return clean JSON.
- Summarize results with **Claude (plain text)**.
- Measure **latency** & **template selection accuracy** with a small **eval harness**.

---

## 🗂 Files in This Lesson
- `sql_templates.py` — Approved query templates (Python dict + builder functions).
- `safe_params.py` — Parse/validate user parameters (segment, days).
- `bi_templates_runner.py` — Classify → pick template → bind → run → explain via Claude.
- `run_bi.py` — CLI entry to ask BI questions (e.g., average p1 by segment last 60 days).
- `eval_harness.py` — Golden cases to measure template selection accuracy & latency.

> Re-uses:
> - Day 1 Claude client: `course/week1/day1/anthropic_client.py`
> - Day 2 DB: `customer_features` in `DATABASE_URL`

---

## 🧩 Prereqs
`.env`:
```ini
ANTHROPIC_API_KEY=your_key
CLAUDE_MODEL=claude-3-5-sonnet-latest
DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
Tables needed:

customer_features(user_email, p1, member_rating, purchase_frequency, recency_days, [segment])

🧑‍💻 Install (if needed)
bash
Copy code
pip install anthropic pandas sqlalchemy python-dotenv
▶️ Run Examples
bash
Copy code
cd ai-marketing-agents-course/course/week1/day5

# Average p1 by segment for the last 90 days
python run_bi.py --q "What's the average p1 by segment for the last 90 days?"

# Segment size (row count) by member_rating
python run_bi.py --q "How many users per member rating?"

# Top purchase_frequency per segment (last 60 days)
python run_bi.py --q "Show top purchase frequency by segment in the last 60 days"
🧠 Design Notes
Template selector uses Claude to pick from a small set (enumeration) and to keep answers concise.

Parameters allowed: segment_id (int), days (int window). Both are range-checked.

Safety: We only run SQL we own; no LLM-generated SQL is executed.

✅ Deliverables
A robust BI co-bot that converts NL questions to safe SQL templates with bound params.

A tiny eval harness to track which template was chosen and latency.

🔜 Next (Day 6)
Executive Streamlit dashboard + Plotly charts using these BI endpoints.

Wire chart JSON into the outputs from Day 3 (chart_json).
