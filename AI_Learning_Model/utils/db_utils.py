import sqlite3

def get_connection():
    return sqlite3.connect("data/learning_data.db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # ✅ Using your schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject_interest TEXT,
            last_score INTEGER CHECK(last_score BETWEEN 0 AND 100),
            learning_style TEXT CHECK(learning_style IN ('Visual', 'Auditory', 'Kinesthetic')),
            next_difficulty TEXT CHECK(next_difficulty IN ('Easy', 'Medium', 'Hard')),
            entry_date TEXT DEFAULT (DATE('now'))
        )
    """)
    
    conn.commit()
    conn.close()

def insert_student(name, subject, score, style, difficulty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_progress (name, subject_interest, last_score, learning_style, next_difficulty)
        VALUES (?, ?, ?, ?, ?)
    """, (name, subject, score, style, difficulty))
    conn.commit()
    conn.close()

def fetch_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, subject_interest, last_score, learning_style, next_difficulty FROM student_progress")
    data = cursor.fetchall()
    conn.close()
    return data
