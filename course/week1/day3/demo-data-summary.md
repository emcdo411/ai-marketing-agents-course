📦 Day 3 Demo Data (Trainer-Ready)

What this does

Creates (or overwrites) the SQLite DB in data/leads_scored_segmentation.db

Builds two source tables: leads_scored, transactions

Calls your Day 2 script to generate customer_features

Prints quick previews so you know it worked

Where to put it

ai-marketing-agents-course/
└─ course/
   └─ week1/
      └─ day3/
         └─ seed_demo_data.py   ← (new)

1) course/week1/day3/seed_demo_data.py
# seed_demo_data.py
"""
Trainer-ready demo seeder for Week 1 — Day 3

Creates a small SQLite dataset:
- leads_scored         (5 rows)
- transactions         (8 rows)
Then imports the Day 2 feature builder to produce:
- customer_features    (5 rows)

Run:
  python course/week1/day3/seed_demo_data.py
"""

import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load env (DATABASE_URL defaults to local SQLite if not set)
load_dotenv()
DEFAULT_SQLITE = "sqlite:///data/leads_scored_segmentation.db"
DB_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

# Ensure data dir exists for SQLite
if DB_URL.startswith("sqlite:///"):
    data_dir = Path(DB_URL.replace("sqlite:///", "")).parent
    data_dir.mkdir(parents=True, exist_ok=True)

# Connect
engine = create_engine(DB_URL, future=True)
print(f"📦 Using DB: {DB_URL}")

# --- Demo data (same as your Day 2 CSVs) ---
leads_scored_rows = [
    {"user_email": "alice@example.com",  "p1": 0.85, "member_rating": 5},
    {"user_email": "bob@example.com",    "p1": 0.62, "member_rating": 3},
    {"user_email": "carla@example.com",  "p1": 0.73, "member_rating": 4},
    {"user_email": "daniel@example.com", "p1": 0.55, "member_rating": 2},
    {"user_email": "eva@example.com",    "p1": 0.91, "member_rating": 5},
]

transactions_rows = [
    {"user_email": "alice@example.com",  "product_id": "P001", "ts": "2024-09-01T10:30:00Z"},
    {"user_email": "alice@example.com",  "product_id": "P002", "ts": "2024-09-15T14:00:00Z"},
    {"user_email": "bob@example.com",    "product_id": "P003", "ts": "2024-06-21T09:00:00Z"},
    {"user_email": "carla@example.com",  "product_id": "P004", "ts": "2024-07-01T16:00:00Z"},
    {"user_email": "carla@example.com",  "product_id": "P005", "ts": "2024-08-11T11:15:00Z"},
    {"user_email": "eva@example.com",    "product_id": "P006", "ts": "2024-09-10T08:45:00Z"},
    {"user_email": "eva@example.com",    "product_id": "P007", "ts": "2024-09-20T13:30:00Z"},
    {"user_email": "eva@example.com",    "product_id": "P008", "ts": "2024-09-28T19:00:00Z"},
]

def seed_tables():
    leads_df = pd.DataFrame(leads_scored_rows)
    tx_df = pd.DataFrame(transactions_rows)

    with engine.begin() as conn:
        # Drop & create (idempotent for demos)
        conn.execute(text("DROP TABLE IF EXISTS leads_scored"))
        conn.execute(text("""
            CREATE TABLE leads_scored (
                user_email TEXT PRIMARY KEY,
                p1 REAL,
                member_rating INTEGER
            )
        """))
        leads_df.to_sql("leads_scored", conn, if_exists="append", index=False)

        conn.execute(text("DROP TABLE IF EXISTS transactions"))
        conn.execute(text("""
            CREATE TABLE transactions (
                user_email TEXT,
                product_id TEXT,
                ts TEXT
            )
        """))
        tx_df.to_sql("transactions", conn, if_exists="append", index=False)

    print("✅ Seeded tables: leads_scored (5), transactions (8)")

def preview_source():
    with engine.connect() as conn:
        leads = pd.read_sql(text("SELECT * FROM leads_scored"), conn)
        tx = pd.read_sql(text("SELECT * FROM transactions LIMIT 5"), conn)
    print("\n🔎 leads_scored:")
    print(leads.to_string(index=False))
    print("\n🔎 transactions (first 5):")
    print(tx.to_string(index=False))

def build_features():
    # Import Day 2 builder from your repo
    from course.week1.day2.build_features import build_features

    with engine.connect() as conn:
        leads = pd.read_sql(text("SELECT * FROM leads_scored"), conn)
        tx    = pd.read_sql(text("SELECT * FROM transactions"), conn)

    feats = build_features(leads, tx)
    with engine.begin() as conn:
        feats.to_sql("customer_features", conn, if_exists="replace", index=False)

    print(f"\n✅ Wrote {len(feats):,} rows to table: customer_features")
    print("\n🔎 customer_features (preview):")
    print(feats.head(10).to_string(index=False))

if __name__ == "__main__":
    seed_tables()
    preview_source()
    build_features()
    print("\n🎉 Demo data ready for Day 3 runs.")

2) How to run (non-technical)

Open your terminal and go to your repo root:

cd ai-marketing-agents-course


Make sure you’ve installed the basics (only once):

pip install pandas sqlalchemy python-dotenv


Make sure your .env exists (or rely on default SQLite):

# .env at repo root (optional for SQLite)
DATABASE_URL=sqlite:///data/leads_scored_segmentation.db


Run the seeder:

python course/week1/day3/seed_demo_data.py


You should see:

tables leads_scored and transactions created & filled

customer_features built and previewed

Now run your Day 3 graph:

cd course/week1/day3
python run_graph.py --segment 2 --limit 50

3) Trainer tips (live session)

Timebox the seeding step (it runs in ~1–2 seconds).

After the preview prints, ask:

“Which of these fields (frequency, recency, rating) would you show an executive first, and why?”

Then run the graph and compare different --segment values so learners see varied summaries.
