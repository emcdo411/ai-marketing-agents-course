## 📘 Week 1 — Day 2: Step-by-Step Instructions

**Topic:** Database Connections & Feature Engineering for AI Systems

---

### 1. Get Your Tools Ready

1. Open your terminal.
2. Install the tools that help Python talk to databases:

   ```bash
   pip install sqlalchemy psycopg2 pandas
   ```

   * `sqlalchemy` → lets Python connect to databases.
   * `psycopg2` → connector for Postgres (optional).
   * `pandas` → helps you calculate and clean data.

---

### 2. Make Your Local Database (SQLite)

Think of this like creating a simple Excel file that Python can query.

1. Inside your project, make a folder called **`data`**.
2. Inside it, create an empty file named:

   ```
   leads_scored_segmentation.db
   ```

   That’s your SQLite database.

---

### 3. Peek Inside the Database

1. Run this in your terminal:

   ```bash
   sqlite3 data/leads_scored_segmentation.db
   ```

2. At the prompt, type:

   ```sql
   .tables
   ```

   * If you already loaded some sample tables (like `leads_scored` or `transactions`), you’ll see them here.

3. You can check a few rows with:

   ```sql
   SELECT * FROM leads_scored LIMIT 5;
   ```

---

### 4. Create Your Features

Now you’ll calculate **three simple traits** for each user:

* **Purchase Frequency** → How many purchases they’ve made.
* **Recency Days** → How long it’s been since their last purchase.
* **Member Rating** → Their customer rating (imported from your leads table).

This is done in a script called **`build_features.py`** in `course/week1/day2/`.
When you run it, it:

1. Connects to the database.
2. Pulls the leads + transactions.
3. Calculates the three features.
4. Saves everything into a new table called **`customer_features`**.

Run it with:

```bash
python course/week1/day2/build_features.py
```

---

### 5. Check the New Table

1. Go back into your SQLite shell:

   ```bash
   sqlite3 data/leads_scored_segmentation.db
   ```
2. Run:

   ```sql
   .tables
   ```

   You should now see `customer_features`.
3. Preview it:

   ```sql
   SELECT user_email, purchase_frequency, recency_days, member_rating
   FROM customer_features LIMIT 10;
   ```

---

### 6. Optional: Preview in Python

1. Open a Python shell or notebook.
2. Run:

   ```python
   import pandas as pd
   import sqlite3

   conn = sqlite3.connect("data/leads_scored_segmentation.db")
   df = pd.read_sql("SELECT * FROM customer_features LIMIT 5", conn)
   print(df)
   ```
3. You’ll see the first 5 rows, neatly formatted.

---

### 7. Business Context (Why It Matters)

* These features are **easy for executives to understand**:

  * Frequency → “How often do they buy?”
  * Recency → “Are they still active?”
  * Rating → “How valuable is this customer?”
* Having these in one clean table means Claude and LangGraph can later generate insights, summaries, and even charts without confusion.

---

### ✅ By the End of Day 2 You Should Have

* ✔️ A local SQLite database (`leads_scored_segmentation.db`).
* ✔️ A script `build_features.py` that creates features.
* ✔️ A new table: `customer_features`.
* ✔️ Confirmed you can view the data in SQLite and Pandas.

---

👉 Next, in **Day 3**, you’ll feed this **feature store** into Claude with a LangGraph node (`segment_analyzer`) to get your first executive-style insights.

---
