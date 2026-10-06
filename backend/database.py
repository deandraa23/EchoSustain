import sqlite3
import json
from typing import List, Optional, Dict, Any

DB_PATH = "echosustain.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            audit_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            file_size_bytes INTEGER,
            s3_path TEXT,
            timestamp TEXT NOT NULL,
            raw_text TEXT,
            transparency_score INTEGER,
            greenwashing_detected BOOLEAN,
            summary TEXT,
            claims_analyzed TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_audit(
    audit_id: str,
    filename: str,
    file_size_bytes: int,
    s3_path: str,
    timestamp: str,
    raw_text: str,
    results: Dict[str, Any]
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO audits (
            audit_id, filename, file_size_bytes, s3_path, timestamp,
            raw_text, transparency_score, greenwashing_detected, summary, claims_analyzed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        audit_id,
        filename,
        file_size_bytes,
        s3_path,
        timestamp,
        raw_text,
        results.get("transparency_score", 0),
        results.get("greenwashing_detected", False),
        results.get("summary", ""),
        json.dumps(results.get("claims_analyzed", []))
    ))
    conn.commit()
    conn.close()

def get_audit(audit_id: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audits WHERE audit_id = ?", (audit_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "audit_id": row["audit_id"],
        "filename": row["filename"],
        "file_size_bytes": row["file_size_bytes"],
        "s3_path": row["s3_path"],
        "timestamp": row["timestamp"],
        "raw_text": row["raw_text"],
        "audit_results": {
            "transparency_score": row["transparency_score"],
            "greenwashing_detected": bool(row["greenwashing_detected"]),
            "summary": row["summary"],
            "claims_analyzed": json.loads(row["claims_analyzed"])
        }
    }

def get_all_audits() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audits ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{
        "audit_id": r["audit_id"],
        "filename": r["filename"],
        "file_size_bytes": r["file_size_bytes"],
        "s3_path": r["s3_path"],
        "timestamp": r["timestamp"],
        "audit_results": {
            "transparency_score": r["transparency_score"],
            "greenwashing_detected": bool(r["greenwashing_detected"]),
            "summary": r["summary"],
            "claims_analyzed": json.loads(r["claims_analyzed"])
        }
    } for r in rows]