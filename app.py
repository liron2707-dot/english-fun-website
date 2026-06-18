import streamlit as st
import json
import os
import random

# --- הגדרות מסד נתונים ---
DB_FILE = "users_db.json"

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

# --- מנוע יצירת תוכן (Scalable Engine) ---
def get_mission_data(age, level, sub_level):
    """מנוע שמייצר שאלות לפי גיל ושלב"""
    # קביעת רמת קושי לפי גיל
    diff = "Easy" if age < 10 else "Medium" if age < 14 else "Hard"
    
    # 8 משימות קבועות
    missions = [
        ("משימה 1: אוצר מילים", "vocab"),
        ("משימה 2: איות (Scramble)", "spelling"),
        ("משימה 3: דקדוק", "grammar"),
        ("משימה 4: קריאה (Anseen)", "reading"),
        ("משימה 5: הבנת הנשמע", "video"),
        ("משימה 6: נכון או לא נכון", "tf"),
        ("משימה 7: משחק אינטראקטיבי", "game"),
        ("משימה 8: קרב בוס", "boss")
    ]
    
    title, m_type = missions[sub_level]
    return {"title": title, "type": m_type, "diff": diff}

# --- ממשק משתמש ---
st.set_page_config(page_title="SmartEnglish Academy", layout="wide")

# ניהול מצב
if "current_user" not in st.session_state: st.session_state.current_user = None

# כניסה
if not st.session_state.current_user:
    st.title("🚀 ברוכים הבאים לאקדמיית האנגלית")
    db = load_db()
    name = st.text_input("הקלד שם משתמש כדי להיכנס או להירשם:")
    if st.button("כניסה"):
        if name in db:
            st.session_state.current_user = db[name]
        else:
            # הרשמה חדשה
            st.session_state.current_user = {
                "name": name, "age": 9, "gender": "בן", "level": 1, "sub_level": 0, "rewards": []
            }
            db[name] = st.session_state.current_user
            save_db(db)
        st.rerun()
    st.stop()

# --- אם המשתמש מחובר ---
user = st.session_state.current_user
db = load_db()

# סרגל צד
with st.sidebar:
    st.header(f"שלום, {user['name']} 🌟")
    st.write(f"רמה: {user['level']} / 99")
    st.progress(user['sub_level'] / 8)
    st.write("---")
    st.write("### 🏆 אוסף הפרסים:")
    for r in user['rewards']: st.write(f"✨ {r}")
    if st.button("יציאה"):
        st.session_state.current_user = None
        st.rerun()

# --- לוגיקת המשחק ---
mission = get_mission_data(user['age'], user['level'], user['sub_level'])

st.title(f"שלב {user['level']} - {mission['title']}")

# אזור המשימות
with st.container(border=True):
    st.write(f"רמת קושי: {mission['diff']}")
    # פה שמים את תוכן המשימה (בהתאם ל-mission['type'])
    if mission['type'] == 'boss':
        st.warning("זהו שלב הבוס! ענה נכון כדי לעבור רמה.")
    
    answer = st.text_input("תשובה:")
    
    if st.button("הגש תשובה"):
        # לוגיקת ניצחון
        user['sub_level'] += 1
        
        # מעבר שלב
        if user['sub_level'] >= 8:
            user['level'] += 1
            user['sub_level'] = 0
            # מתן פרס כל 10 שלבים
            if user['level'] % 10 == 0:
                reward = f"כרטיס נדיר - {random.choice(['גביע הזהב', 'פוקימון אגדי', 'כדורגל זהב'])}"
                user['rewards'].append(reward)
                st.balloons()
        
        # שמירה למסד הנתונים
        db[user['name']] = user
        save_db(db)
        st.rerun()
