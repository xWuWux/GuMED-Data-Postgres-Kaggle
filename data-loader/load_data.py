import os
import csv
import asyncio
import asyncpg

DATABASE_URL = os.environ["DATABASE_URL"]
CSV_PATH = os.environ.get("CSV_PATH")

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS heart_disease (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    sex INTEGER,
    cp INTEGER,
    trestbps INTEGER,
    chol INTEGER,
    fbs INTEGER,
    restecg INTEGER,
    thalach INTEGER,
    exang INTEGER,
    oldpeak FLOAT,
    slope INTEGER,
    ca INTEGER,
    thal INTEGER,
    target INTEGER
);
"""

INSERT_ROW = """
INSERT INTO heart_disease (
    age, sex, cp, trestbps, chol, fbs, restecg, thalach,
    exang, oldpeak, slope, ca, thal, target
) VALUES (
    $1,$2,$3,$4,$5,$6,$7,$8,
    $9,$10,$11,$12,$13,$14
);
"""

async def load():
    conn = await asyncpg.connect(DATABASE_URL)

    await conn.execute(CREATE_TABLE)
    await conn.execute("TRUNCATE TABLE heart_disease RESTART IDENTITY;")

    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            await conn.execute(
                INSERT_ROW,
                int(row["age"]),
                int(row["sex"]),
                int(row["cp"]),
                int(row["trestbps"]),
                int(row["chol"]),
                int(row["fbs"]),
                int(row["restecg"]),
                int(row["thalach"]),
                int(row["exang"]),
                float(row["oldpeak"]),
                int(row["slope"]),
                int(row["ca"]),
                int(row["thal"]),
                int(row["target"]),
            )

    await conn.close()

if __name__ == "__main__":
    asyncio.run(load())
