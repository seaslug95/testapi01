import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from tabulate import tabulate

DB_PATH = Path("./data/db_providers.db")


def get_connection():
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_name TEXT NOT NULL,
            provider_number TEXT NOT NULL,
            ingested_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS provider_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            quarter TEXT NOT NULL,
            Ambulatory INTEGER,
            Hospital INTEGER,
            Other_NA INTEGER,
            FOREIGN KEY (report_id) REFERENCES providers(id)
        )
    """)


def save_provider_report(report: dict) -> int:
    ingested_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        # Ensure schema exists every time
        init_db(conn)

        cur = conn.cursor()

        # Insert provider metadata
        cur.execute("""
            INSERT INTO providers (
                provider_name,
                provider_number,
                ingested_at
            ) VALUES (?, ?, ?)
        """, (
            report["provider_name"],
            report["provider_number"],
            ingested_at
        ))

        report_id = cur.lastrowid

        # Insert quarterly expenses
        for row in report["provider_expenses_by_quarter"]:
            cur.execute("""
                INSERT INTO provider_expenses (
                    report_id,
                    quarter,
                    Ambulatory,
                    Hospital,
                    Other_NA
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                report_id,
                row["quarter"],
                row["Ambulatory"],
                row["Hospital"],
                row["Other_NA"]
            ))

        conn.commit()

    return report_id

def fetch_all_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT * FROM providers")
        providers = [dict(row) for row in cur.fetchall()]

        cur.execute("SELECT * FROM provider_expenses")
        expenses = [dict(row) for row in cur.fetchall()]

    return {
        "providers": providers,
        "provider_expenses": expenses
    }


