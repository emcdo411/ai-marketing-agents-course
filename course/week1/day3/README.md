# 📘 Week 1 — Day 3  
**Topic:** LangGraph Deep Dive — State, Nodes, and Executable Graphs (Claude-powered)  

---

## 🎯 What You’ll Learn Today
- How to define a **shared “state”** so each step in your graph knows what to expect.  
- How to create a **Claude-powered analysis node** that returns clean JSON insights.  
- How to wire up a simple flow: **START → segment_analyzer → END**.  
- How to preview real data from your SQLite database (`customer_features`).  
- How to run the graph from the **command line** with different options.  

---

## 🛠 Prerequisites
Before starting today:  
- ✅ Day 2 created a `customer_features` table in your database.  
  - Columns should be:  
    `user_email, p1, member_rating, purchase_frequency, recency_days`  
- ✅ You have a `.env` file with:  
  ```ini
  ANTHROPIC_API_KEY=your_key_here
  CLAUDE_MODEL=claude-3-5-sonnet-latest
  DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
````

* ✅ You have Python installed with these packages:

  ```bash
  pip install langgraph pandas sqlalchemy python-dotenv
  ```

---

## 📂 Files for Today

Today you’ll be working with four files in `course/week1/day3/`:

1. **`state_types.py`** → Defines the “shape” of data your graph uses.
2. **`segment_analyzer_node.py`** → The Claude-powered node that generates insights.
3. **`build_graph.py`** → Connects the pieces into a flow: START → Node → END.
4. **`run_graph.py`** → A simple command-line runner so you can try it out.

---

## 🧩 Step 1: Define the State

Think of **state** like a form everyone has to fill out the same way.

* It prevents “surprises” when nodes pass information.
* It ensures Claude always sends back the fields we need.

Open `state_types.py` and check that it looks like this:

```python
from typing_extensions import TypedDict

class GraphState(TypedDict):
    """
    Canonical state for segment analysis.
    """
    segment_id: int
    sample_df_json: str   # JSON preview of DB rows
    response: str         # executive summary (3-5 sentences)
    insights: str         # bullet points
    summary_table: str    # compact JSON (metric/value)
    chart_json: str       # optional, not used today
```

---

## 🧩 Step 2: Create the Segment Analyzer Node

This is your Claude-powered step.

* It takes a preview of data from the database.
* It asks Claude for a **summary, insights, and a table**.
* It returns everything in a structured format.

(You’ll use the `anthropic_client.py` from Day 1 here.)

---

## 🧩 Step 3: Build the Graph

Your graph is a **flowchart in code**.

* START: you load the data and set up the state.
* `segment_analyzer`: Claude reads the data and produces insights.
* END: you collect the output and show results.

This is wired in `build_graph.py`.

---

## 🧩 Step 4: Run the Graph from CLI

Now you’ll run your graph like a little app.

1. Open your terminal.
2. Navigate to Day 3 folder:

   ```bash
   cd ai-marketing-agents-course/course/week1/day3
   ```
3. Run the graph with a **segment ID** and row limit:

   ```bash
   python run_graph.py --segment 2 --limit 50
   ```
4. Try another one:

   ```bash
   python run_graph.py --segment 0 --limit 25
   ```

---

## 📊 Expected Output

When successful, you’ll see three sections in your console:

* **RESPONSE** → 3–5 sentences (executive-style summary).
* **INSIGHTS** → 4–6 bullet points.
* **SUMMARY TABLE** → JSON with `metric` and `value` pairs.

Example (simplified):

```text
RESPONSE
Segment 2 shows strong purchasing activity with high ratings.

INSIGHTS
- Most users are repeat buyers
- Recency trend is improving
- Strong cluster for retention

SUMMARY TABLE
[{"metric": "avg_p1", "value": "0.82"},
 {"metric": "avg_frequency", "value": "3.4"}]
```

---

## 🧠 Why This Matters

* Typed **state** keeps your graphs predictable and easy to test.
* The **segment\_analyzer** node is your first reusable building block.
* Using a **DB preview** keeps prompts grounded (no need to dump the entire table).

---

## ✅ Deliverables

By the end of Day 3 you should have:

* A **typed graph state** (`state_types.py`).
* A **Claude-powered node** (`segment_analyzer_node.py`).
* A **graph flow** (`build_graph.py`).
* A **CLI runner** (`run_graph.py`).
* A working example with real data flowing end-to-end.

---

## 🔜 Next (Day 4 Preview)

Tomorrow you’ll:

* Build a **Router Node** that classifies intent.
* Add conditional edges → route to BI, Product, Email, or Analyst nodes.
* Start moving toward **multi-agent orchestration**.

```

