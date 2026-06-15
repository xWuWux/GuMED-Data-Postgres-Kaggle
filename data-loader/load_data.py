import os
import csv
import asyncio
import asyncpg
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
CSV_PATH     = os.environ.get("CSV_PATH", "/data/heart_disease_uci.csv")

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS heart_disease (
    id       SERIAL PRIMARY KEY,
    age      INTEGER NOT NULL,
    sex      INTEGER NOT NULL,
    cp       INTEGER NOT NULL,
    trestbps INTEGER,
    chol     INTEGER,
    fbs      INTEGER,
    restecg  INTEGER,
    thalach  INTEGER,
    exang    INTEGER,
    oldpeak  FLOAT,
    slope    INTEGER,
    ca       FLOAT,
    thal     FLOAT,
    target   INTEGER NOT NULL
);
"""

INSERT_ROW = """
INSERT INTO heart_disease
    (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
"""

def safe_int(val):
    try:
        return int(float(val)) if val not in ("", None, "NA") else None
    except (ValueError, TypeError):
        return None

def safe_float(val):
    try:
        return float(val) if val not in ("", None, "NA") else None
    except (ValueError, TypeError):
        return None

async def load():
    log.info("Connecting to database...")
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        log.info("Creating table if not exists...")
        await conn.execute(CREATE_TABLE)

        log.info(f"Loading data from {CSV_PATH}...")
        count = 0
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                await conn.execute(
                    INSERT_ROW,
                    safe_int(row.get("age")),
                    safe_int(row.get("sex")),
                    safe_int(row.get("cp")),
                    safe_int(row.get("trestbps")),
                    safe_int(row.get("chol")),
                    safe_int(row.get("fbs")),
                    safe_int(row.get("restecg")),
                    safe_int(row.get("thalach")),
                    safe_int(row.get("exang")),
                    safe_float(row.get("oldpeak")),
                    safe_int(row.get("slope")),
                    safe_float(row.get("ca")),
                    safe_float(row.get("thal")),
                    safe_int(row.get("target")),
                )
                count += 1
        log.info(f"Successfully inserted {count} records.")
        total = await conn.fetchval("SELECT COUNT(*) FROM heart_disease")
        log.info(f"Total rows in database: {total}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(load())
