## 📋 Week 1 — Day 2 Checklist

**Topic:** Database Connections & Feature Engineering

---

### 🔧 Setup

* [ ] Open your terminal (Command Prompt / PowerShell on Windows, Terminal on Mac).
* [ ] Install required tools:

  ```bash
  pip install sqlalchemy psycopg2 pandas
  ```
* [ ] Confirm your `data/` folder exists in your project.
* [ ] Make sure you have a file named:

  ```
  data/leads_scored_segmentation.db
  ```

---

### 🗄️ Database Tables

* [ ] Open the SQLite shell:

  ```bash
  sqlite3 data/leads_scored_segmentation.db
  ```

* [ ] Check for tables:

  ```sql
  .tables
  ```

  You should see:

  * `leads_scored`
  * `transactions`

* [ ] If missing, load or create these tables before moving forward.

---

### 🧮 Build Features

* [ ] Navigate to your Day 2 folder:

  ```bash
  cd course/week1/day2
  ```
* [ ] Run the script:

  ```bash
  python build_features.py
  ```
* [ ] Watch the terminal:

  * Confirms DB connection.
  * Shows how many rows are in each input table.
  * Prints a **preview** of 10 new rows.
  * Writes everything into a new table called `customer_features`.

---

### 🔍 Verify Results

* [ ] Reopen SQLite:

  ```bash
  sqlite3 data/leads_scored_segmentation.db
  ```

* [ ] Check tables again:

  ```sql
  .tables
  ```

  You should now see:

  * `customer_features`

* [ ] Peek at the data:

  ```sql
  SELECT user_email, purchase_frequency, recency_days, member_rating
  FROM customer_features
  LIMIT 10;
  ```

* [ ] (Optional) Open Python and preview in Pandas:

  ```python
  import pandas as pd, sqlite3
  conn = sqlite3.connect("data/leads_scored_segmentation.db")
  df = pd.read_sql("SELECT * FROM customer_features LIMIT 5", conn)
  print(df)
  ```

---

### 📊 Business Context

* [ ] You now have **frequency**, **recency**, and **rating** stored for each user.
* [ ] These are easy-to-explain metrics for executives.
* [ ] This clean feature table will be the foundation for **Day 3 insights**.

---

### ✅ End of Day 2 Deliverables

* [ ] `build_features.py` in `course/week1/day2/`.
* [ ] A new table called `customer_features` inside your SQLite database.
* [ ] Previewed and verified at least 10 rows of results.

---

👉 Next up: **Day 3** → feeding these features into Claude with a **LangGraph node** (`segment_analyzer`) to get your first executive-style insights.

---

Would you like me to also prep a **ready-to-run sample dataset (CSV inserts for `leads_scored` + `transactions`)** so you don’t start with an empty database during Day 2?
