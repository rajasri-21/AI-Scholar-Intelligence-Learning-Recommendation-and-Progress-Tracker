import sqlite3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

DB_PATH = "data/ai_learning.db"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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

# Add new student record
def add_record(name, subject, score, style, difficulty):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO student_progress (name, subject_interest, last_score, learning_style, next_difficulty) VALUES (?, ?, ?, ?, ?)",
        (name, subject, score, style, difficulty)
    )
    conn.commit()
    conn.close()
    print(f"✅ Record added for {name}")

# Load data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    data = pd.read_sql_query("SELECT * FROM student_progress", conn)
    conn.close()
    return data

# Train and save model
def train_model():
    data = load_data()
    if data.empty:
        print("⚠️ No data available in database. Please add some records first.")
        return None

    X = data[['last_score', 'learning_style']]
    y = data['next_difficulty']

    le = LabelEncoder()
    X['learning_style'] = le.fit_transform(X['learning_style'])

    clf = DecisionTreeClassifier()
    clf.fit(X, y)

    with open("models/learning_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    with open("models/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    print("✅ Model trained successfully using SQLite data.")

if __name__ == "__main__":
    init_db()

    # Optional: Add a few initial records (only first run)
    sample_data = [
        ("Sneha", "Artificial Intelligence", 85, "Visual", "Hard"),
        ("Priya", "Data Science", 78, "Auditory", "Medium"),
        ("Kavin", "Machine Learning", 92, "Kinesthetic", "Hard"),
        ("Rahul", "Web Development", 74, "Visual", "Medium"),
        ("Isha", "Cloud Computing", 88, "Auditory", "Hard")
    ]

    for record in sample_data:
        add_record(*record)

    train_model()
