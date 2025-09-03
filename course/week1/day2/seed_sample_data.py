# seed_sample_data.py
"""
Seeds sample source tables for Week 1, Day 2:

Tables created (replace if already exist):
  - leads_scored(user_email, p1, member_rating)
  - transactions(user_email, product_id, ts)

Usage:
  DATABASE_URL (optional) in .env, defaults to sqlite:///data/leads_scored_segmentation.db
  python seed_sample_data.py
"""

import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SQLITE = "sqlite:///data/leads_scored_segmentation.db"
DB_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

# Ensure local data dir exists for SQLite
if DB_URL.startswith("sqlite:///"):
    data_dir = Path(DB_URL.replace("sqlite:///", "")).parent
    data_dir.mkdir(parents=True, exist_ok=True)

engine = create_engine(DB_URL, future=True)

# -----------------------
# Configurable parameters
# -----------------------
RANDOM_SEED = 42
N_LEADS = 500
N_TX = 2000

PRODUCTS = [f"SKU-{i:03d}" for i in range(1, 51)]  # 50 products
DOMAINS = ["example.com", "sample.org", "mail.net", "demo.io"]

NOW = datetime.now(timezone.utc)
DAYS_BACK = 180  # spread transactions over the last ~6 months


def random_emails(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    firsts = np.array(
        ["alex","sam","jordan","chris","taylor","morgan","casey","jamie","riley",
         "drew","blake","cameron","avery","nate","max","jules","parker","reese",
         "devon","hayden","skyler","remy","peyton","ari","sage"]
    )
    lasts = np.array(
        ["lee","kim","lopez","garcia","miller","smith","johnson","anderson","davis",
         "martin","clark","lewis","robinson","walker","young","allen","king",
         "wright","scott","torres","nguyen","hill","green","adams"]
    )
    doms = np.array(DOMAINS)
    first = rng.choice(firsts, size=n)
    last = rng.choice(lasts, size=n)
    dom = rng.choice(doms, size=n)
    # add a numeric suffix to reduce collisions
    suffix = rng.integers(1, 9999, size=n)
    emails = np.char.add(np.char.add(np.char.add(first, "."), last), np.char.add(suffix.astype(str), "@" + dom))
    return emails


def make_leads_scored(n_leads: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    emails = random_emails(n_leads, seed + 1)

    # Member rating: discrete 1..5 (skewed toward 3-5)
    member_rating = rng.choice([1,2,3,4,5], size=n_leads, p=[0.05, 0.10, 0.35, 0.30, 0.20])

    # p1: probability-like score 0..1 (beta distribution for realism)
    p1 = rng.beta(a=2.0, b=3.0, size=n_leads)  # more mass around ~0.4

    df = pd.DataFrame({
        "user_email": emails,
        "p1": np.round(p1, 4),
        "member_rating": member_rating.astype(int),
    })

    # small chance of duplicates -> drop to ensure uniqueness
    df = df.drop_duplicates(subset=["user_email"]).reset_index(drop=True)
    return df


def random_timestamps(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    # generate days ago uniformly, then add random seconds within the day
    days_ago = rng.integers(0, DAYS_BACK, size=n)
    secs = rng.integers(0, 24*3600, size=n)
    ts = [NOW - timedelta(days=int(d), seconds=int(s)) for d, s in zip(days_ago, secs)]
    return np.array(ts, dtype="datetime64[ns]")


def make_transactions(leads_df: pd.DataFrame, n_tx: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    # Bias: users with higher p1 & rating transact a bit more often
    weights = (0.5 + 0.5*leads_df["p1"]) * (0.5 + 0.5*(leads_df["member_rating"] / 5.0))
    weights = np.clip(weights, 1e-3, None)
    weights = weights / weights.sum()

    buyer_idx = rng.choice(leads_df.index.values, size=n_tx, replace=True, p=weights)
    user_emails = leads_df.loc[buyer_idx, "user_email"].to_numpy()
    product_ids = rng.choice(PRODUCTS, size=n_tx, replace=True)

    ts = random_timestamps(n_tx, seed + 1)

    tx = pd.DataFrame({
        "user_email": user_emails,
        "product_id": product_ids,
        "ts": pd.to_datetime(ts).astype("datetime64[ns]"),
    }).sort_values("ts").reset_index(drop=True)

    return tx


def write_table(df: pd.DataFrame, name: str):
    with engine.begin() as conn:
        df.to_sql(name, conn, if_exists="replace", index=False)
    print(f"✅ Wrote {len(df):,} rows to table: {name}")


def main():
    print(f"📦 Database: {DB_URL}")
    np.random.seed(RANDOM_SEED)

    leads = make_leads_scored(N_LEADS, RANDOM_SEED)
    write_table(leads, "leads_scored")

    tx = make_transactions(leads, N_TX, RANDOM_SEED + 100)
    write_table(tx, "transactions")

    # quick previews
    print("\n🔎 leads_scored preview:")
    print(leads.head(5).to_string(index=False))

    print("\n🔎 transactions preview:")
    print(tx.head(5).to_string(index=False))

    print("\nDone. You can now run build_features.py to generate customer_features.")


if __name__ == "__main__":
    main()
