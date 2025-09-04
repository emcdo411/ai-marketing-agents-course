# 📘 Week 1 — Day 6
**Topic:** Executive Dashboard with Streamlit

---

## 🎯 Learning Objectives
- Launch a **Streamlit app** that executives can use interactively.
- Provide **tabs** for each co-bot (BI, Product, Email, Analyst).
- Call:
  - The **router** (`build_router_app`) to handle free-form Q&A.
  - The **BI Expert** (`exec_bi`) for structured analytics.
- Display:
  - BI tables (JSON rows → pandas DataFrame).
  - Summaries (Claude explanations).
- Use a **PowerBI-style dark theme** for professional polish.

---

## 🗂 Files in This Lesson
- `dashboard.py` — Streamlit app with BI/Product/Email/Analyst tabs.
- `style.css` — Dark theme overrides for Streamlit.

> Re-uses:
> - Day 4 router (`build_router_app`)
> - Day 5 BI runner (`exec_bi`)

---

## 🧩 Prereqs
- `.env` with:
  ```ini
  ANTHROPIC_API_KEY=your_key
  CLAUDE_MODEL=claude-3-5-sonnet-latest
  DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
Install:

bash
Copy code
pip install streamlit pandas anthropic langgraph sqlalchemy python-dotenv plotly tabulate
▶️ Run
From repo root:

bash
Copy code
cd course/week1/day6
streamlit run dashboard.py
Open browser → http://localhost:8501

🧠 Design Notes
Router tab → any free-form Q → routes to BI/Product/Email/Analyst.

BI tab → direct BI queries, show table + summary.

Product/Email/Analyst tabs → route-specific Q&A.

Theme → CSS file enforces dark background + modern typography.

✅ Deliverables
A working Streamlit dashboard with 4 tabs.

BI tab shows real data tables and exec summaries.

Router tab demonstrates end-to-end orchestration.
✅ Test Flow

From repo root, install deps if not done:

pip install streamlit pandas anthropic langgraph sqlalchemy python-dotenv plotly tabulate


Run dashboard:

cd course/week1/day6
streamlit run dashboard.py


Try:

Router tab → “What’s the average p1 by segment?”

BI tab → “How many users per member rating?”

Product tab → “Which features should we highlight for Segment 2?”

Email tab → “Write a renewal email for high-value buyers.”

Analyst tab → “Summarize Segment 1 behavior.”
