# build_features.py
"""
📘 Week 1 — Day 2: Feature Store Builder

This script takes two existing tables in your database:
  1. leads_scored (basic info about each lead/customer)
  2. transactions (records of purchases)

It creates a new table:
  - customer_features
    with columns:
      user_email, p1, member_rating, purchase_frequency, recency_days

🎯 Why this matters:
Executives can easily understand frequency, recency, and rating.
These are the "features" that AI and BI systems will analyze.
"""

import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ------------------------------------------------------
# STEP 1 — Load settings and point to the database
# ------------------------------------------------------
load_dotenv()

# Default is a simple SQLite file inside /data folder
DEFAULT_SQLITE = "sqlite:///data/leads_scored_segmentation.db"
DB_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

# Make sure the /data folder exists (if using SQLite)
if DB_URL.startswith("sqlite:///"):
    data_dir = Path(DB_URL.replace("sqlite:///", "")).parent
    data_dir.mkdir(parents=True, exist_ok=True)

# Create a database connection
engine = create_engine(DB_URL, future=True)


# ------------------------------------------------------
# STEP 2 — Helper functions
# ------------------------------------------------------
def _table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    try:
        with engine.connect() as conn:
            conn.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
            return True
    except Exception:
        return False


def _require_tables_or_exit():
    """Stop the script if required tables are missing."""
    required = ["leads_scored", "transactions"]
    missing = [t for t in required if not _table_exists(t)]
    if missing:
        print(f"❌ Missing required table(s): {missing}")
        print("➡️ Make sure you have 'leads_scored' and 'transactions' loaded.")
        sys.exit(1)


def _read_tables():
    """Load leads and transactions into pandas DataFrames."""
    with engine.connect() as conn:
        leads = pd.read_sql(text("SELECT * FROM leads_scored"), conn)
        tx = pd.read_sql(text("SELECT * FROM transactions"), conn)
    return leads, tx


# ------------------------------------------------------
# STEP 3 — Build the features
# ------------------------------------------------------
def build_features(leads: pd.DataFrame, tx: pd.DataFrame) -> pd.DataFrame:
    # 1. Purchase Frequency → how many transactions per user
    purchase_freq = (
        tx.groupby("user_email")["product_id"]
          .count()
          .rename("purchase_frequency")
          .reset_index()
    )

    # 2. Recency Days → days since last transaction
    tx = tx.copy()
    tx["ts"] = pd.to_datetime(tx["ts"], errors="coerce", utc=True)
    max_ts = (
        tx.dropna(subset=["ts"])
          .groupby("user_email")["ts"]
          .max()
          .rename("last_ts")
          .reset_index()
    )
    now = pd.Timestamp.now(tz="UTC")
    max_ts["recency_days"] = (now - max_ts["last_ts"]).dt.days

    # 3. Merge everything into one table
    features = (
        leads.merge(purchase_freq, on="user_email", how="left")
             .merge(max_ts[["user_email", "recency_days"]], on="user_email", how="left")
    )

    # Fill missing values with sensible defaults
    features["purchase_frequency"] = features["purchase_frequency"].fillna(0).astype(int)
    features["recency_days"] = features["recency_days"].fillna(365).astype(int)

    # Select only the columns we care about
    return features[["user_email", "p1", "member_rating", "purchase_frequency", "recency_days"]]


# ------------------------------------------------------
# STEP 4 — Save results into the database
# ------------------------------------------------------
def write_features(df: pd.DataFrame):
    with engine.begin() as conn:
        df.to_sql("customer_features", conn, if_exists="replace", index=False)
    print(f"✅ Wrote {len(df):,} rows to 'customer_features'")


# ------------------------------------------------------
# STEP 5 — Main program
# ------------------------------------------------------
def main():
    print(f"📦 Connecting to DB: {DB_URL}")
    _require_tables_or_exit()

    leads, tx = _read_tables()
    print(f"→ leads_scored rows: {len(leads):,}")
    print(f"→ transactions rows: {len(tx):,}")

    feats = build_features(leads, tx)
    print("🧩 Preview of new features:")
    print(feats.head(10).to_string(index=False))

    write_features(feats)
    print("🎉 Done.")


if __name__ == "__main__":
    main()
```

---

### 📝 How this file works (plain English):

1. **Connects to your database** (defaults to SQLite in `/data`).
2. **Checks for two input tables**:

   * `leads_scored` (basic info about leads/customers).
   * `transactions` (history of purchases).
3. **Calculates three key features**:

   * How often people buy (frequency).
   * How long since they last bought (recency).
   * Their rating (comes from `leads_scored`).
4. **Merges those into one clean table** called `customer_features`.
5. **Saves it back** into the database so you can use it in Day 3.

---

Do you want me to also make a **matching non-technical Day 2 checklist (like Day 1)** that you can print and tick off as you go?

