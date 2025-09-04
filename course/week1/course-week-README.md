# 🚀 Week 1 — Foundations of Generative AI Systems

Welcome to Week 1 of your **AI Marketing Agents Course**.  
This week you’ll go from raw data → features → LLM nodes → intent routing → safe BI queries → dashboards and visualizations.

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
day6/   Streamlit dashboard (exec BI + router outputs)
day7/   Visualizations (Plotly charts + JSON integration)

````

---

## 📅 Daily Breakdown

### **Day 1 — Claude Client Setup**
- Build `ClaudeClient` wrapper in `anthropic_client.py`.
- Test JSON-only output with system prompts.
- 🎯 Goal: Safely call Claude with schema-first prompts.

---

### **Day 2 — Data Foundations**
- Seed and build `customer_features` with:
  - `purchase_frequency`, `recency_days`, `member_rating`, `p1`.
- Scripts: `seed_sample_data.py`, `build_features.py`.
- 🎯 Goal: Have a **feature store** backing your nodes.

---

### **Day 3 — Segment Analyzer Node**
- Define `GraphState`.
- Build `segment_analyzer_node.py` (Claude JSON → insights).
- Graph: START → segment_analyzer → END.
- 🎯 Goal: Exec-ready insights from your feature store.

---

### **Day 4 — Router & Co-Bots**
- Router node classifies into: BI, Product, Email, Analyst.
- Add co-bots for each.
- Conditional routing with confidence threshold.
- CLI `run_router.py` upgraded with:
  - Pretty-print tables (default).
  - `--json` structured output for dashboards.
- 🎯 Goal: Route user questions automatically.

---

### **Day 5 — BI Expert**
- Create safe, parameterized templates in `sql_templates.py`.
- Parse and validate params (`safe_params.py`).
- `bi_templates_runner.py`: run → JSON rows + Claude summary.
- CLI tools: `run_bi.py`, `eval_harness.py`.
- Replace Day 4 `bi_node.py` with structured JSON version.
- 🎯 Goal: Reliable BI results without arbitrary SQL.

---

### **Day 6 — Streamlit Dashboard**
- Build `dashboard.py` (Streamlit app):
  - Tabs: **BI**, **Product**, **Email**, **Analyst**.
  - Calls router (`run_router`) for free-form Q&A.
  - Calls BI Expert (`exec_bi`) for metrics & tables.
  - Dark theme, PowerBI-style layout.
- 🎯 Goal: Executives can click → see answers + tables.

---

### **Day 7 — Visualizations**
- Use Plotly/Altair to render charts from JSON rows.
- Extend GraphState to include `chart_json`.
- BI outputs feed into charts (bar/line/scatter).
- Update dashboard to show **tables + charts**.
- 🎯 Goal: End-to-end pipeline → **data → features → LLM nodes → dashboards with visuals**.

---

## 🔧 Install Checklist

```bash
pip install anthropic langgraph pandas sqlalchemy python-dotenv tabulate streamlit plotly
````

Ensure `.env` has:

```ini
ANTHROPIC_API_KEY=your_key
CLAUDE_MODEL=claude-3-5-sonnet-latest
DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
```

---

## ▶️ Test Checklist

### Day 2

```bash
cd course/week1/day2
python seed_sample_data.py
python build_features.py
```

### Day 3

```bash
cd course/week1/day3
python run_graph.py --segment 2 --limit 50
```

### Day 4

```bash
cd course/week1/day4
python run_router.py --q "What's the average p1 by segment for the last 90 days?"
python run_router.py --q "Summarize Segment 1 behavior." --json
```

### Day 5

```bash
cd course/week1/day5
python run_bi.py --q "What's the average p1 by member rating?"
python eval_harness.py
```

### Day 6

```bash
cd course/week1/day6
streamlit run dashboard.py
```

### Day 7

* Ask BI questions in the dashboard and confirm charts render from JSON rows.

---

## 📊 Deliverables by End of Week 1

* Claude client with JSON-safe prompts.
* Feature store (`customer_features`).
* Segment analyzer node.
* Router with BI/Product/Email/Analyst.
* BI Expert with safe SQL templates.
* Streamlit dashboard that routes and displays results.
* Plotly/Altair charts for BI outputs.

---

## 🔜 Week 2 Preview

* **Day 8–9**: Unit tests + eval harnesses (router, BI accuracy).
* **Day 10–11**: Governance, compliance guardrails (opt-outs, audit logs).
* **Day 12–14**: Multi-agent workflows with LangGraph supervisor pattern.

```

---

Would you like me to go ahead and **generate the Day 6 Streamlit dashboard code (`dashboard.py`)** now, so you can run `streamlit run` and see your BI + router outputs live?
```

