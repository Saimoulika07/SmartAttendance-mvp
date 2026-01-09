import sqlite3

conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    class_id TEXT,
    start_time TEXT,
    end_time TEXT,
    active INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    student_email TEXT,
    timestamp TEXT,
    UNIQUE(session_id, student_email)
)
""")

conn.commit()
