import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------------- DATABASE CONNECTION ----------------------
def get_connection():
    conn = sqlite3.connect("learning_data.db", check_same_thread=False)
    return conn

def create_table():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS student_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject_interest TEXT,
        last_score INTEGER CHECK(last_score BETWEEN 0 AND 100),
        learning_style TEXT CHECK(learning_style IN ('Visual', 'Auditory', 'Kinesthetic')),
        next_difficulty TEXT CHECK(next_difficulty IN ('Easy', 'Medium', 'Hard')),
        entry_date TEXT DEFAULT (DATE('now'))
    );
    """)
    conn.commit()
    conn.close()

create_table()

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="AI Learning Progress Tracker", page_icon="📊", layout="wide")

# ---------------------- CUSTOM STYLES ----------------------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #F0F4FF, #E8F6F3);
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        color: #2B547E;
        text-align: center;
        font-size: 38px;
    }
    h2 {
        color: #1C2833;
        margin-top: 30px;
    }
    .stButton>button {
        background-color: #3C8DAD;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2B6C8A;
        color: white;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown("<h1>📚 AI-Based Learning Recommendation & Progress Tracker</h1>", unsafe_allow_html=True)
st.write("Empowering personalized learning through data and adaptive AI insights.")

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("Navigation 🧭")
menu = st.sidebar.radio("Choose a section:", ["🏠 Home", "➕ Add New Entry", "📈 View Progress", "🧠 AI Recommendation"])

# ---------------------- DATABASE HELPERS ----------------------
def fetch_all_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM student_progress ORDER BY entry_date DESC", conn)
    conn.close()
    return df

def insert_student(name, subject, score, style, difficulty):
    conn = get_connection()
    conn.execute("INSERT INTO student_progress (name, subject_interest, last_score, learning_style, next_difficulty) VALUES (?, ?, ?, ?, ?)",
                 (name, subject, score, style, difficulty))
    conn.commit()
    conn.close()

# ---------------------- HOME SECTION ----------------------
if menu == "🏠 Home":
    st.subheader("Welcome 👋")
    st.write("""
    This dashboard helps track student learning progress using AI-based insights.  
    You can:
    - Add new student performance data.  
    - View detailed progress charts.  
    - Get AI-based difficulty recommendations for the next learning session.
    """)
    df = fetch_all_data()
    if not df.empty:
        st.dataframe(df)

# ---------------------- ADD NEW ENTRY SECTION ----------------------
elif menu == "➕ Add New Entry":
    st.subheader("Add New Student Record 📝")

    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Student Name")
    with col2:
        subject = st.text_input("Subject Interest")
    with col3:
        score = st.number_input("Last Score", 0, 100, step=1)

    col4, col5 = st.columns(2)
    with col4:
        style = st.selectbox("Learning Style", ["Visual", "Auditory", "Kinesthetic"])
    with col5:
        difficulty = st.selectbox("Next Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Add Record"):
        if name and subject:
            insert_student(name, subject, score, style, difficulty)
            st.success(f"✅ Record added successfully for {name}")
        else:
            st.error("Please fill all required fields.")

# ---------------------- VIEW PROGRESS SECTION ----------------------
elif menu == "📈 View Progress":
    st.subheader("📊 Student Progress Analysis")

    df = fetch_all_data()
    if df.empty:
        st.warning("No data found. Please add some student progress records first.")
    else:
        students = df['name'].unique().tolist()
        selected_student = st.selectbox("Select Student to View Progress", students)

        student_data = df[df['name'] == selected_student].sort_values(by='entry_date')

        st.markdown(f"### Progress Overview for {selected_student}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Average Score", value=round(student_data['last_score'].mean(), 2))
        with col2:
            st.metric(label="Total Entries", value=len(student_data))

        # Plot progress chart
        fig = px.line(student_data, x='entry_date', y='last_score', 
                      title=f"{selected_student}'s Progress Over Time",
                      markers=True, color_discrete_sequence=['#3C8DAD'])
        st.plotly_chart(fig, use_container_width=True)

# ---------------------- AI RECOMMENDATION SECTION ----------------------
elif menu == "🧠 AI Recommendation":
    st.subheader("AI-Based Learning Recommendation Engine 🤖")
    st.write("This module predicts the next difficulty level based on recent performance trends.")

    df = fetch_all_data()
    if df.empty:
        st.warning("Please add data to generate AI-based recommendations.")
    else:
        name = st.selectbox("Select Student", df['name'].unique())
        student_data = df[df['name'] == name].sort_values(by='entry_date', ascending=False).head(3)
        avg_score = student_data['last_score'].mean()

        if avg_score >= 85:
            recommendation = "Hard"
        elif avg_score >= 70:
            recommendation = "Medium"
        else:
            recommendation = "Easy"

        st.markdown(f"""
        <div class="metric-card">
            <h2>🎯 Recommendation for {name}</h2>
            <p><b>Average of last 3 scores:</b> {round(avg_score,2)}</p>
            <h3 style='color:#3C8DAD;'>Recommended Next Difficulty: <b>{recommendation}</b></h3>
        </div>
        """, unsafe_allow_html=True)
