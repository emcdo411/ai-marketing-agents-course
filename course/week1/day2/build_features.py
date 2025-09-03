# build_features.py
"""
Week 1 — Day 2: Feature Store Builder

Reads:
  - leads_scored(user_email, p1, member_rating, ...)
  - transactions(user_email, product_id, ts, ...)

Writes:
  - customer_features(user_email, p1, member_rating, purchase_frequency, recency_days)

Usage:
  - Configure DATABASE_URL in .env (defaults to SQLite under /data)
  - Run: python build_features.py
"""

import os
import sys
import math
import warnings
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError
from dotenv import load_dotenv

warnings.simplefilter("ignore", FutureWarning)
load_dotenv()

# --- Config ---
DEFAULT_SQLITE = "sqlite:///data/leads_scored_segmentation.db"
DB_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

# Ensure local data dir exists for SQLite
if DB_URL.startswith("sqlite:///"):
    data_dir = Path(DB_URL.replace("sqlite:///", "")).parent
    data_dir.mkdir(parents=True, exist_ok=True)

engine = create_engine(DB_URL, future=True)

REQUIRED_TABLES = ["leads_scored", "transactions"]


def _table_exists(engine, table_name: str) -> bool:
    try:
        with engine.connect() as conn:
            # Works across SQLite/Postgres
            conn.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
            return True
    except Exception:
        return False


def _require_tables_or_exit():
    missing = [t for t in REQUIRED_TABLES if not _table_exists(engine, t)]
    if missing:
        msg = (
            f"❌ Missing required table(s): {missing}\n"
            "Expected:\n"
            "  - leads_scored(user_email, p1, member_rating, ...)\n"
            "  - transactions(user_email, product_id, ts, ...)\n\n"
            "Tip: load or create these tables, then rerun.\n"
            f"Database: {DB_URL}\n"
        )
        print(msg)
        sys.exit(1)


def _read_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    with engine.connect() as conn:
        leads = pd.read_sql(text("SELECT * FROM leads_scored"), conn)
        tx = pd.read_sql(text("SELECT * FROM transactions"), conn)
    return leads, tx


def _to_datetime(series: pd.Series) -> pd.Series:
    """Best-effort parse to UTC datetime; returns NaT where impossible."""
    try:
        out = pd.to_datetime(series, errors="coerce", utc=True)
        # If parsed naive, localize to UTC
        if out.dt.tz is None:
            out = out.dt.tz_localize("UTC")
        return out
    except Exception:
        return pd.to_datetime(pd.Series([], dtype="datetime64[ns]"))


def build_features(leads: pd.DataFrame, tx: pd.DataFrame) -> pd.DataFrame:
    # Validate column presence (friendly errors)
    for col in ["user_email", "p1", "member_rating"]:
        if col not in leads.columns:
            raise ValueError(f"'leads_scored' missing column: {col}")

    for col in ["user_email", "product_id", "ts"]:
        if col not in tx.columns:
            raise ValueError(f"'transactions' missing column: {col}")

    # Purchase frequency: count of transactions per user
    purchase_freq = (
        tx.groupby("user_email")["product_id"]
          .count()
          .rename("purchase_frequency")
          .reset_index()
    )

    # Recency (days since last transaction)
    tx = tx.copy()
    tx["ts"] = _to_datetime(tx["ts"])
    max_ts = (
        tx.dropna(subset=["ts"])
          .groupby("user_email")["ts"]
          .max()
          .rename("last_ts")
          .reset_index()
    )

    now = pd.Timestamp.now(tz="UTC")
    max_ts["recency_days"] = (now - max_ts["last_ts"]).dt.days.astype("Int64")

    # Merge features together
    features = (
        leads.merge(purchase_freq, on="user_email", how="left")
             .merge(max_ts[["user_email", "recency_days"]], on="user_email", how="left")
             .copy()
    )

    # Fill nulls with interpretable defaults
    features["purchase_frequency"] = features["purchase_frequency"].fillna(0).astype(int)
    features["recency_days"] = features["recency_days"].fillna(365).astype(int)

    # Select clean output schema
    cols = [
        "user_email",
        "p1",
        "member_rating",
        "purchase_frequency",
        "recency_days",
    ]
    missing = [c for c in cols if c not in features.columns]
    if missing:
        raise ValueError(f"Output missing required columns: {missing}")

    return features[cols].sort_values(["purchase_frequency", "recency_days"], ascending=[False, True])


def write_features(df: pd.DataFrame):
    with engine.begin() as conn:
        df.to_sql("customer_features", conn, if_exists="replace", index=False)
    print(f"✅ Wrote {len(df):,} rows to table: customer_features")


def main():
    print(f"📦 DB: {DB_URL}")
    _require_tables_or_exit()

    leads, tx = _read_tables()
    print(f"→ leads_scored rows: {len(leads):,}")
    print(f"→ transactions rows: {len(tx):,}")

    feats = build_features(leads, tx)
    print("🧩 Preview:")
    print(feats.head(10).to_string(index=False))

    write_features(feats)
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except (ProgrammingError, OperationalError) as db_err:
        print(f"Database error: {db_err}")
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(3)
