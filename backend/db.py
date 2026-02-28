import sqlite3
import json
from pathlib import Path

DB_FILE = Path("database.db")

def init_db():
    """Initialise SQLite tables if they do not exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Simple table for runs
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            created_at TEXT,
            data_json TEXT
        )
    ''')
    
    # Table for LLM audit logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS llm_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            timestamp TEXT,
            model TEXT,
            prompt TEXT,
            response_json TEXT,
            error TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_run(run_id: str, created_at: str, run_dict: dict):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO runs (run_id, created_at, data_json)
        VALUES (?, ?, ?)
    ''', (run_id, created_at, json.dumps(run_dict)))
    conn.commit()
    conn.close()

def load_run(run_id: str) -> dict:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT data_json FROM runs WHERE run_id = ?', (run_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def load_all_runs() -> list[dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT data_json FROM runs ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in rows]

def log_llm_call(run_id: str, timestamp: str, model: str, prompt: str, response: str, error: str = ""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO llm_logs (run_id, timestamp, model, prompt, response_json, error)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (run_id, timestamp, model, prompt, response, error))
    conn.commit()
    conn.close()
