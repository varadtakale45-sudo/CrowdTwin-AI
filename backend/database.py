import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path


DB_PATH=Path(__file__).parents[1]/"crowd_twin.db"
TABLES=("simulation_runs","crowd_states","predictions","routes","what_if_results","experiments")


@contextmanager
def connect():
    db=sqlite3.connect(DB_PATH); db.row_factory=sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()


def initialize():
    with connect() as db:
        for table in TABLES:
            db.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, payload TEXT NOT NULL)")


def save(table,payload):
    if table not in TABLES: raise ValueError("Invalid database table")
    with connect() as db:
        cur=db.execute(f"INSERT INTO {table}(payload) VALUES (?)",(json.dumps(payload),)); return cur.lastrowid


def recent(table,limit=25):
    if table not in TABLES: raise ValueError("Invalid database table")
    with connect() as db:
        return [{"id":r["id"],"created_at":r["created_at"],**json.loads(r["payload"], parse_constant=lambda value: None)} for r in db.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?",(limit,))]


def report_by_id(report_id):
    with connect() as db:
        row = db.execute('SELECT payload FROM experiments WHERE id = ?', (report_id,)).fetchone()
        return json.loads(row['payload']).get('report') if row else None
