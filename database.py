import sqlite3

def get_db():
    conn = sqlite3.connect('lifelog.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    
    db.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    db.commit()
    db.close()