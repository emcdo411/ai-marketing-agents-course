# 📘 Week 1 — Day 3
**Topic:** LangGraph Deep Dive — State, Nodes, and Executable Graphs (Claude-powered)

---

## 🎯 Learning Objectives
- Define a **typed graph state** that your nodes read/write.
- Build a production-ready **`segment_analyzer`** node (Claude + strict JSON).
- Wire a runnable **START → segment_analyzer → END** graph.
- Pull a **sample preview** from your SQLite feature store (`customer_features`).
- Expose a clean **CLI** to invoke the graph for any `segment_id`.

---

## 🗂 Files in This Lesson
- `state_types.py` — Strongly typed LangGraph state for reliability.
- `segment_analyzer_node.py` — Claude-powered node that creates exec insights.
- `build_graph.py` — Compiles START → node → END; helper to invoke from code.
- `run_graph.py` — Command-line runner (`python run_graph.py --segment 2 --limit 50`).

> Re-uses `course/week1/day1/anthropic_client.py` for Claude calls.

---

## 🧩 Prereqs
- Day 2 created `customer_features` in your DB:
  - Columns: `user_email, p1, member_rating, purchase_frequency, recency_days`
- `.env` has:
  ```ini
  ANTHROPIC_API_KEY=your_key
  CLAUDE_MODEL=claude-3-5-sonnet-latest
  DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
🧑‍💻 Install (if needed)
bash
Copy code
pip install langgraph pandas sqlalchemy python-dotenv
▶️ Run
bash
Copy code
cd ai-marketing-agents-course/course/week1/day3

# Analyze segment 2 with a 50-row preview
python run_graph.py --segment 2 --limit 50

# Try a different segment
python run_graph.py --segment 0 --limit 25
Expected console output:

RESPONSE — 3–5 sentence exec summary

INSIGHTS — 4–6 bullets

SUMMARY TABLE — compact JSON (metric/value)

🧠 Why This Matters
Typed state makes your graphs predictable and easier to test.

A single node can become a reusable building block for routers and multi-agent flows.

Using DB previews keeps your prompts grounded without shipping full tables to the model.

✅ Deliverables
A runnable graph that turns DB features into exec-ready insights.

A CLI pattern you can reuse for unit tests and automation.

🔜 Next (Day 4 Preview)
Build a Router Node that classifies user intent → BI / Product / Email / Analyst / Other.

Add conditional edges to route questions automatically.

python
Copy code

---

## 🧩 `course/week1/day3/state_types.py`

```python
# state_types.py
from typing_extensions import TypedDict

class GraphState(TypedDict):
    """
    Canonical state for segment analysis.
    """
    segment_id: int
    sample_df_json: str   # JSON (records) preview sent to the LLM
    response: str         # narrative for execs (3-5 sentences)
    insights: str         # bullet points (\n- delimited string)
    summary_table: str    # JSON (list of {"metric","value"})
    chart_json: str       # optional plot spec as JSON (unused today)
