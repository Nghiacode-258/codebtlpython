import sqlite3

def connect():
    return sqlite3.connect("students_data.db")

def init_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mssv TEXT,
            name TEXT,
            [class] TEXT,
            major TEXT,
            birthday TEXT,
            phone TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()