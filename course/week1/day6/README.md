# 📘 Week 1 — Day 6

**Topic:** Executive Dashboard with Streamlit

This lesson turns everything you’ve built into an **executive-friendly dashboard**. No coding required today—just follow the steps to run it and understand how it works.

---

## 🎯 Learning Objectives

* Launch a **Streamlit** web app locally.
* Use **tabs** to explore four “co-bots”: **BI, Product, Email, Analyst**.
* Ask free-form questions in the **Router** tab (it auto-chooses the right co-bot).
* View **tables and summaries** (from your BI Expert).
* Use a **dark, boardroom-ready theme** for a professional look.

---

## 🧩 What’s Included Today

* `dashboard.py` — the Streamlit app with tabs.
* `style.css` — optional dark theme to keep visuals consistent.

> Re-uses:
>
> * Day 4: `build_router_app` (routes your question to BI/Product/Email/Analyst)
> * Day 5: `exec_bi` (runs safe, pre-approved BI queries)

---

## 🗺️ Big Picture (Mermaid Workflow)

```mermaid
flowchart TD
    A[User Question in Streamlit] --> B{Which Tab?}
    B -->|🔀 Router| C[build_router_app]
    C -->|Intent + Confidence| D[Co-bot Node (BI/Product/Email/Analyst)]
    D --> E[Answer back to Streamlit]

    B -->|📊 BI| F[exec_bi(question)]
    F --> G[Rows (JSON) + Summary]
    G --> H[Table in Streamlit]
    G --> I[Summary text in Streamlit]

    style A fill:#222,color:#fff,stroke:#555
    style H fill:#222,color:#fff,stroke:#555
    style I fill:#222,color:#fff,stroke:#555
```

**How to read this:**

* **Router tab**: You type any question → Router decides which co-bot should answer.
* **BI tab**: You ask BI-style questions (counts, averages, by-segment, etc.).
* The BI tool returns **rows (data)** + an **executive summary**, which the app shows as a table and text.

---

## ✅ Before You Start (Prereqs)

Make sure your project’s `.env` exists at the repo root and has:

```ini
ANTHROPIC_API_KEY=your_key
CLAUDE_MODEL=claude-3-5-sonnet-latest
DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
```

Install the one-time dependencies (from your repo root):

```bash
pip install streamlit pandas anthropic langgraph sqlalchemy python-dotenv plotly tabulate
```

> If you’re on Windows and use **Command Prompt**, the same command works.

---

## ▶️ Run the Dashboard (No Coding)

From the repo root:

```bash
cd course/week1/day6
streamlit run dashboard.py
```

Your browser should open to **[http://localhost:8501](http://localhost:8501)**
(If not, copy/paste that address into your browser.)

---

## 🖱️ How to Use Each Tab

### 🔀 Router (general Q\&A)

* Type **any** question (examples below).
* The Router chooses a co-bot (BI/Product/Email/Analyst) and returns the answer.
* You’ll see the **intent** (what it chose) and the **confidence**.

Try:

* “What’s the average `p1` by segment for the last 90 days?”
* “Draft a short renewal email for Segment 2.”
* “Summarize Segment 1 behavior.”

---

### 📊 BI Expert (analytics)

* Ask BI-style questions.
* You’ll see:

  * **Table** of results (converted from JSON rows)
  * **Executive summary** (plain language explanation)

Try:

* “How many users per member rating?”
* “Average `p1` by segment.”
* “Top purchase frequency by segment.”

> Tip: If the table is empty, confirm you ran **Day 2** and **Day 3** (your `customer_features` table is required).

---

### 📦 Product Expert (positioning ideas)

* Ask product-focused questions:

  * “Which features should we highlight for Segment 2?”
  * “What is the right value prop for high-frequency buyers?”

---

### ✉️ Email Writer (outreach drafts)

* Ask for outreach copy:

  * “Write a renewal email for high-value buyers.”
  * “Compose a short intro message for Segment 1.”

> You can copy/paste and tweak the text in your email tool—this is a **starting point**, not a final send.

---

### 🧑‍💼 Analyst (exec summaries)

* Ask for executive-style summaries:

  * “Summarize Segment 1 behavior in 4 bullets.”
  * “Give me a 3-sentence update on the last quarter’s trends.”

---

## 🧠 Design Notes (Plain English)

* **Router vs. BI tab**

  * *Router*: free-form; it figures out the right co-bot.
  * *BI*: direct line to analytics; guaranteed table + summary.

* **Dark theme**

  * The included `style.css` gives a consistent **PowerBI-style dark** look so the app feels boardroom-ready.

* **Grounded answers**

  * BI comes from **safe, pre-approved SQL templates** (Day 5).
  * This means answers are **consistent, explainable, and auditable**.

---

## 🧪 Quick Test Flow

1. Install (if you skipped earlier):

```bash
pip install streamlit pandas anthropic langgraph sqlalchemy python-dotenv plotly tabulate
```

2. Run:

```bash
cd course/week1/day6
streamlit run dashboard.py
```

3. In the **Router** tab, try:

* “What’s the average p1 by segment?”
* “Summarize Segment 1 behavior.”

4. In the **BI** tab, try:

* “How many users per member rating?”

5. In **Product / Email / Analyst**, try any of the prompts above.

---

## 🧯 Troubleshooting (Non-Technical)

* **The page loads but tables are empty**

  * Make sure you completed **Day 2** (built `customer_features`) and **Day 3** (the pipeline runs).
  * Confirm `.env` has `DATABASE_URL` pointing to your SQLite file.

* **Streamlit won’t start**

  * Re-run installs:

    ```bash
    pip install streamlit pandas anthropic langgraph sqlalchemy python-dotenv plotly tabulate
    ```
  * Close/reopen your terminal and try again.

* **Claude/Anthropic errors**

  * Double-check your `ANTHROPIC_API_KEY` in `.env`.
  * Ensure your internet connection is active.

---

## 📸 (Optional) Screenshot Checklist for Your Repo

Add these images to your repo (e.g., `docs/screenshots/`) and reference them in the main README:

* `router_tab.png` — a routed question with **intent + confidence**
* `bi_tab_table.png` — BI table with top 10 rows
* `bi_tab_summary.png` — the executive summary paragraph
* `product_tab.png`, `email_tab.png`, `analyst_tab.png` — one example each

> These help recruiters and stakeholders quickly understand the value.

---

## ✅ Deliverables (End of Day 6)

* A running **Streamlit dashboard** at `http://localhost:8501`
* **Router tab** demonstrating end-to-end orchestration
* **BI tab** showing **tables + summaries** with a dark, professional theme

---

### 🔜 What’s Next (Day 7 preview)

You’ll add **charts (Plotly)** to visualize BI results, and keep everything clean and exec-ready.
