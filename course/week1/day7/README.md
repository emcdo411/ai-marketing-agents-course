# 📘 Week 1 — Day 7
**Topic:** Visualizing BI Outputs with Plotly + Streamlit

---

## 🎯 Learning Objectives
- Convert **BI JSON rows** into **Plotly** charts (bar / line / scatter).
- Select sensible defaults based on the **template** and **columns** returned.
- Wire charts into a **Streamlit** dashboard alongside tables and summaries.
- Keep the stack clean: **no seaborn**, Plotly only; dark theme for exec polish.

---

## 🗂 Files in This Lesson
- `chart_utils.py` — Helpers that convert BI `rows` → Plotly figures.
- `bi_charts.py` — One call that runs the **Day 5 BI Expert** and returns `df`, `figure`, and summary.
- `dashboard_charts.py` — A Streamlit app (Day 6 style) that renders **tables + charts**.
- (Optional) `style.css` — Reuse Day 6 CSS if you want the same dark theme.

> Re-uses:
> - Day 5 runner: `course/week1/day5/bi_templates_runner.py` (`exec_bi`)

---

## 🧩 Prereqs
- `.env` already set (from earlier days).
- Install:
  ```bash
  pip install plotly streamlit pandas
▶️ Run
From repo root:

bash
Copy code
cd course/week1/day7
streamlit run dashboard_charts.py
🧠 Design Notes
We map well-known templates → chart types:

avg_p1_by_segment → bar chart (x=segment, y=avg_p1)

avg_p1_by_member_rating → bar (x=member_rating, y=avg_p1)

count_by_member_rating → bar (x=member_rating, y=n)

top_purchase_frequency_by_segment → bar (x=segment, y=max_purchase_frequency)

If an unexpected template/columns appear, we auto-detect numeric columns and plot a generic bar.

We don’t hardcode colors; we use Plotly’s template="plotly_dark" for a professional dark style.

✅ Deliverables
Chart utilities ready for reuse in your Day 6 dashboard or any UI.

A charts-enabled Streamlit app that execs can use immediately.

🔜 After Day 7
Add unit tests for chart generation.

Serialize figure specs (e.g., fig.to_json()) for API delivery.

Start wiring chart_json back into LangGraph state if you want end-to-end JSON-only UIs.
