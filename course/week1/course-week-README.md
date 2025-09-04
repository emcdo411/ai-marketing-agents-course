# 🚀 Week 1 — Foundations of Generative AI Systems

Welcome to Week 1 of your **AI Marketing Agents Course**.  
This week establishes your foundation: connecting to data, building features, orchestrating nodes with LangGraph, routing intents, and creating safe BI workflows.

---

## 🗂 Structure

```

course/
week1/
day1/   Claude client setup
day2/   Data foundations & feature store
day3/   Segment analyzer node
day4/   Router with BI/Product/Email/Analyst
day5/   BI Expert with template-driven SQL

````

---

## 📅 Daily Breakdown

### **Day 1 — Claude Client Setup**
- ✅ Build `ClaudeClient` wrapper in `anthropic_client.py`.
- ✅ Test JSON-only output with system prompts.
- 🎯 Goal: You can call Claude safely with strict JSON or text responses.

---

### **Day 2 — Data Foundations**
- ✅ Build and seed `customer_features` table in SQLite:
  - `purchase_frequency`
  - `recency_days`
  - `member_rating`
  - `p1` (probability score)
- ✅ Scripts:
  - `seed_sample_data.py` (mock data)
  - `build_features.py` (engineered features)
- 🎯 Goal: You now have a **feature store** backing your AI nodes.

---

### **Day 3 — Segment Analyzer Node**
- ✅ Define `GraphState` (typed dict).
- ✅ Build `segment_analyzer_node.py` that reads a DB preview and outputs:
  - `response` (summary)
  - `insights` (bullets)
  - `summary_table` (metric/value JSON)
- ✅ Compile a simple graph: START → segment_analyzer → END.
- 🎯 Goal: First working LangGraph node → exec-ready insights.

---

### **Day 4 — Router & Co-Bots**
- ✅ Add `router_node.py` with intents: BI, Product, Email, Analyst.
- ✅ Add co-bots:
  - `bi_node.py` (replaced with Day 5 version)
  - `product_node.py`
  - `email_node.py`
  - `analyst_node.py`
- ✅ Conditional routing edges with a confidence threshold.
- ✅ Upgraded CLI `run_router.py` with:
  - Pretty-print (default)
  - `--json` flag (structured output for dashboards)
- 🎯 Goal: Route user questions to the right node automatically.

---

### **Day 5 — BI Expert with Safe SQL**
- ✅ Create template-driven BI queries (`sql_templates.py`).
- ✅ Safe param parsing (`safe_params.py`).
- ✅ `bi_templates_runner.py` to run queries → JSON rows + Claude summary.
- ✅ `run_bi.py` CLI for BI-only testing.
- ✅ `eval_harness.py` for template selection accuracy & latency.
- ✅ Replace Day 4 `bi_node.py` to use `exec_bi()` → returns structured JSON.
- 🎯 Goal: Executives get reliable BI insights without risking arbitrary SQL.

---

## 🔧 Install Checklist

Run once from repo root:
```bash
pip install anthropic langgraph pandas sqlalchemy python-dotenv tabulate
````

Ensure `.env` has:

```ini
ANTHROPIC_API_KEY=your_key
CLAUDE_MODEL=claude-3-5-sonnet-latest
DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
```

---

## ▶️ Test Checklist

### Day 2 — Seed + Features

```bash
cd course/week1/day2
python seed_sample_data.py
python build_features.py
```

### Day 3 — Segment Analyzer

```bash
cd course/week1/day3
python run_graph.py --segment 2 --limit 50
```

### Day 4 — Router

```bash
cd course/week1/day4
python run_router.py --q "What's the average p1 by segment for the last 90 days?"
python run_router.py --q "Draft a short outreach email to Segment 2 about renewals."
python run_router.py --q "Summarize Segment 1 behavior." --json
```

### Day 5 — BI Expert

```bash
cd course/week1/day5
python run_bi.py --q "What's the average p1 by member rating?"
python eval_harness.py
```

---

## 📊 Deliverables by End of Week 1

* A working **Claude client** with JSON-safe prompts.
* A **feature store** in SQLite (`customer_features`).
* A **segment analyzer node** (LLM-powered insights).
* A **router** with BI/Product/Email/Analyst co-bots.
* A **BI Expert** that executes safe SQL templates with Claude explanations.
* CLI tools (`run_graph.py`, `run_router.py`, `run_bi.py`) to test each step.

---

## 🔜 Next Steps (Week 2 Preview)

* **Day 6**: Build an exec-facing Streamlit dashboard (BI charts + router outputs).
* **Day 7**: Add visualization: Plotly/Altair charts, JSON → chart\_json → UI.
* **Day 8**: Evaluation harness for routing accuracy, latency, and data drift.

```

---

👉 Do you want me to also prepare a **Week 2 README skeleton** now (so you have a roadmap for Days 6–8), or keep building day-by-day?
```
