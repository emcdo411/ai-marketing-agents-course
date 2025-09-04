# 📘 Week 1 — Day 2: Loading Sample Data into SQLite

This guide walks you through loading **sample data** into your SQLite database so that your **feature builder script (`build_features.py`)** has real data to work with.

---

## 📂 Step 1: Verify Your CSV Files

Make sure you already have these two files in your project:

### `course/week1/day2/leads_scored.csv`
```csv
user_email,p1,member_rating
alice@example.com,0.85,5
bob@example.com,0.62,3
carla@example.com,0.73,4
daniel@example.com,0.55,2
eva@example.com,0.91,5
course/week1/day2/transactions.csv
csv
Copy code
user_email,product_id,ts
alice@example.com,P001,2024-09-01T10:30:00Z
alice@example.com,P002,2024-09-15T14:00:00Z
bob@example.com,P003,2024-06-21T09:00:00Z
carla@example.com,P004,2024-07-01T16:00:00Z
carla@example.com,P005,2024-08-11T11:15:00Z
eva@example.com,P006,2024-09-10T08:45:00Z
eva@example.com,P007,2024-09-20T13:30:00Z
eva@example.com,P008,2024-09-28T19:00:00Z
These hold:

leads_scored.csv → Customers with scores and ratings.

transactions.csv → Their purchase history.

📂 Step 2: Load Data into SQLite
Open your terminal.

From the project root, launch SQLite:

bash
Copy code
sqlite3 data/leads_scored_segmentation.db
At the SQLite prompt, run these commands:

sql
Copy code
-- Create leads_scored table
DROP TABLE IF EXISTS leads_scored;
CREATE TABLE leads_scored (
  user_email TEXT PRIMARY KEY,
  p1 REAL,
  member_rating INTEGER
);

-- Import leads CSV (adjust path if needed)
.mode csv
.import course/week1/day2/leads_scored.csv leads_scored

-- Create transactions table
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
  user_email TEXT,
  product_id TEXT,
  ts TEXT
);

-- Import transactions CSV
.import course/week1/day2/transactions.csv transactions

-- Quick checks
.tables
SELECT * FROM leads_scored;
SELECT * FROM transactions LIMIT 5;
Exit SQLite when finished:

sql
Copy code
.quit
📂 Step 3: Run the Feature Script
Now that your tables are ready, run the feature builder:

bash
Copy code
python course/week1/day2/build_features.py
✅ Example Output
You should see something like:

sql
Copy code
📦 DB: sqlite:///data/leads_scored_segmentation.db
→ leads_scored rows: 5
→ transactions rows: 8
🧩 Preview:
        user_email    p1  member_rating  purchase_frequency  recency_days
eva@example.com     0.91              5                   3            40
alice@example.com   0.85              5                   2            54
carla@example.com   0.73              4                   2            75
bob@example.com     0.62              3                   1           100
daniel@example.com  0.55              2                   0           365
✅ Wrote 5 rows to table: customer_features
🎉 Result
Your new customer_features table is now populated with:

Frequency (how often they buy).

Recency (how recently they bought).

Rating (their value score).

This is the foundation for Day 3 insights.

yaml
Copy code

---

👉 Do you want me to also generate the **`seed_sample_data.py` script** (so you can skip SQLite commands entirely and just 
