We’ll make two small CSV files that you can import into SQLite:

leads_scored.csv → holds your leads/customers with scores & ratings.

transactions.csv → holds their purchase history.

📂 Step 1: Create CSV Files
course/week1/day2/leads_scored.csv
user_email,p1,member_rating
alice@example.com,0.85,5
bob@example.com,0.62,3
carla@example.com,0.73,4
daniel@example.com,0.55,2
eva@example.com,0.91,5

course/week1/day2/transactions.csv
user_email,product_id,ts
alice@example.com,P001,2024-09-01T10:30:00Z
alice@example.com,P002,2024-09-15T14:00:00Z
bob@example.com,P003,2024-06-21T09:00:00Z
carla@example.com,P004,2024-07-01T16:00:00Z
carla@example.com,P005,2024-08-11T11:15:00Z
eva@example.com,P006,2024-09-10T08:45:00Z
eva@example.com,P007,2024-09-20T13:30:00Z
eva@example.com,P008,2024-09-28T19:00:00Z

📂 Step 2: Load Into SQLite

From your project root:

sqlite3 data/leads_scored_segmentation.db


Then run:

-- Create leads_scored table
DROP TABLE IF EXISTS leads_scored;
CREATE TABLE leads_scored (
  user_email TEXT PRIMARY KEY,
  p1 REAL,
  member_rating INTEGER
);

-- Import CSV (adjust path if needed)
.mode csv
.import course/week1/day2/leads_scored.csv leads_scored

-- Create transactions table
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
  user_email TEXT,
  product_id TEXT,
  ts TEXT
);

-- Import CSV
.import course/week1/day2/transactions.csv transactions

-- Quick checks
.tables
SELECT * FROM leads_scored;
SELECT * FROM transactions LIMIT 5;


Exit with .quit.

📂 Step 3: Run Your Feature Script

Now test your Day 2 script:

python course/week1/day2/build_features.py


You should see output like:

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

✅ Result

Your customer_features table is now populated with frequency, recency, and rating for each user.

👉 Want me to also give you a ready-made Python seeder script (seed_sample_data.py) that automatically creates these tables & inserts sample data — so you don’t have to touch the SQLite shell at all?
