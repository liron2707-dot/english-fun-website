import streamlit as st
import json
import os
import random

# --- הגדרות ---
DB_FILE = "users_db.json"
st.set_page_config(page_title="Nexus English Academy", layout="wide")

# --- CSS עיצוב פרימיום ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700;900&display=swap');
    
    * { font-family: 'Heebo', sans-serif; }
    
    /* עיצוב כללי */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }
    
    /* כרטיסים */
    .hero-card { background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 30px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center; }
    
    /* כפתורים */
    .stButton>button { width: 100%; border-radius: 50px; font-weight: 900; background: #3b82f6; border: none; padding: 20px; font-size: 20px; }
    
    /* ממשק */
    [data-testid="stSidebar"] { background: #020617; }
    h1, h2, h3 { color: #f8fafc; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- פונקציות מסד נתונים ---
def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

# --- מנוע תוכן (הלב של המערכת) ---
def get_mission_content(level, age):
    # מנוע שמייצר שאלות דינמיות
    categories = ["אוצר מילים", "איות", "דקדוק", "קריאה", "הבנת הנשמע", "נכון/לא נכון", "חידון", "בוס!"]
    current_mission = categories[level % 8] # מחזיר משימה לפי השלב
    
    # תבניות תוכן לפי גיל
    difficulty = "קל" if age < 10 else "בינוני" if age < 13 else "מתקדם"
    
    return {
        "title": f"שלב {level} - {current_mission}",
        "question": f"שאלה עבור {difficulty} - מה הפירוש של Word {level}?",
        "options": ["אפשרות א", "אפשרות ב", "אפשרות ג"],
        "answer": "אפשרות א"
    }

# --- מסך כניסה ---
def render_login():
    st.markdown('<div class="hero-card"><h1>🚀 Nexus English Academy</h1><p>הדרך הכי מרגשת ללמוד אנגלית</p></div>', unsafe_allow_html=True)
    db = load_db()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("כניסה למשתמש קיים")
        name = st.selectbox("בחר שם:", list(db.keys()))
        if st.button("התחבר"):
            st.session_state.user = db[name]
            st.rerun()
            
    with col2:
        st.subheader("משתמש חדש")
        n = st.text_input("שם מלא")
        a = st.number_input("גיל", 6, 16, 9)
        if st.button("התחל מסע!"):
            if n not in db:
                db[n] = {"name": n, "age": a, "level": 1, "rewards": []}
                save_db(db)
                st.session_state.user = db[n]
                st.rerun()
            else: st.error("שם תפוס!")

# --- מסך המשחק ---
def render_game():
    u = st.session_state.user
    db = load_db()
    
    # סרגל צד
    with st.sidebar:
        st.title(f"שלום {u['name']}")
        st.write(f"רמה: {u['level']} / 99")
        st.progress(u['level'] / 99)
        if st.button("מחק משתמש ❌"):
            del db[u['name']]
            save_db(db)
            st.session_state.user = None
            st.rerun()
        if st.button("התנתק"):
            st.session_state.user = None
            st.rerun()

    # משימה נוכחית
    m = get_mission_content(u['level'], u['age'])
    st.markdown(f"## {m['title']}")
    
    with st.container():
        st.write(f"### {m['question']}")
        ans = st.radio("בחר תשובה:", m['options'])
        if st.button("הגש"):
            u['level'] += 1
            db[u['name']] = u
            save_db(db)
            st.rerun()

# --- לוגיקה ראשית ---
if "user" not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    render_login()
else:
    render_game()
