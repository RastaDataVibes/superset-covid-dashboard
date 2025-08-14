# live_total_deaths_updater.py
# ------------------------------------------------------------
# Pulls COVID-19 total deaths for ALL countries from
# Our World in Data and upserts into a Postgres table:
#   total_deaths(date DATE, country VARCHAR , totaldeaths NUMERIC)
# The script runs on an interval (default: 3600s).
# Configure DB via env vars or let it use defaults below.
# ------------------------------------------------------------

import os
import time
import math
import psycopg2
import psycopg2.extras as extras
import pandas as pd

OWID_URL = os.getenv(
    "OWID_CSV_URL",
    "https://covid.ourworldindata.org/data/owid-covid-data.csv",
)

# ---- Database config (env vars take precedence) ----
DB_HOST = os.getenv("DB_HOST", "dpg-d285uac9c44c73a3sa70-a.frankfurt-postgres.render.com")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "greenchain_db")
DB_USER = os.getenv("DB_USER", "greenchain_admin")
DB_PASS = os.getenv("DB_PASS", "MTvRpQRtD2c5yIpQplT9dDDgXRC6BhYm")  # your password

# Update interval in seconds (default 1 hour)
UPDATE_INTERVAL_SEC = int(os.getenv("UPDATE_INTERVAL_SEC", "3600"))

# Batch size for upserts (tune if needed)
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5000"))


def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )


def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS total_deaths (
                date DATE NOT NULL,
                country VARCHAR(100) NOT NULL,
                totaldeaths NUMERIC,
                PRIMARY KEY (date, country)
            );
            """
        )
        conn.commit()


def upsert_rows(conn, rows):
    """
    rows: list of tuples (date, country, totaldeaths)
    """
    if not rows:
        return

    query = """
        INSERT INTO total_deaths (date, country, totaldeaths)
        VALUES %s
        ON CONFLICT (date, country)
        DO UPDATE SET totaldeaths = EXCLUDED.totaldeaths;
    """
    with conn.cursor() as cur:
        extras.execute_values(cur, query, rows, page_size=BATCH_SIZE)
    conn.commit()


def fetch_and_prepare_chunks():
    """
    Stream OWID CSV and yield cleaned batches of tuples:
    (date, country, totaldeaths)
    """
    usecols = ["location", "date", "total_deaths"]
    for chunk in pd.read_csv(OWID_URL, usecols=usecols, chunksize=100_000):
        chunk = chunk.dropna(subset=["location", "date"])

        excludes = {
            "World",
            "International",
            "Africa",
            "Asia",
            "Europe",
            "European Union",
            "North America",
            "South America",
            "Oceania",
        }
        chunk = chunk[~chunk["location"].isin(excludes)]
        chunk = chunk[~chunk["location"].str.startswith("OWID_")]

        # Convert to numeric, allow decimals, fill NaN with 0
        chunk["total_deaths"] = pd.to_numeric(chunk["total_deaths"], errors="coerce").fillna(0)

        rows = list(
            zip(
                pd.to_datetime(chunk["date"]).dt.date,
                chunk["location"].astype(str),
                chunk["total_deaths"],
            )
        )

        for i in range(0, len(rows), BATCH_SIZE):
            yield rows[i : i + BATCH_SIZE]


def run_once():
    conn = get_conn()
    try:
        ensure_table(conn)
        total_upserted = 0
        for batch in fetch_and_prepare_chunks():
            upsert_rows(conn, batch)
            total_upserted += len(batch)
        print(f"[OK] Upserted {total_upserted} rows into total_deaths.")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        print("[INFO] Starting update cycle...")
        run_once()
        print("[INFO] Update completed successfully.")
    except Exception as e:
        print(f"[ERROR] Update cycle failed: {e}")



