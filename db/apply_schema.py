"""Apply db/schema.sql directly to Postgres (no dashboard needed).

Uses SUPABASE_DB_URL (direct/pooler Postgres URI). Run from the project root:
    python -m db.apply_schema
"""
from pathlib import Path

import psycopg2

from config.settings import settings


def main() -> None:
    if not settings.supabase_db_url:
        raise SystemExit("SUPABASE_DB_URL is not set in .env")

    sql = Path(__file__).with_name("schema.sql").read_text()
    conn = psycopg2.connect(settings.supabase_db_url)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
    finally:
        conn.close()
    print("Schema applied: accounts, leads, opportunities.")


if __name__ == "__main__":
    main()
