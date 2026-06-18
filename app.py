import streamlit as st
import json
import os

# --- הגדרות בסיסיות ---
st.set_page_config(page_title="Nexus Academy", layout="wide")
DB_FILE = "users_db.json"
CONTENT_FILE = "content.json"

# --- פונקציות מסד נתונים ---
def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, indent=4)

def load_content():
    if not os.path.exists(CONTENT_FILE): return {}
    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

# --- פונקציית משימה בטוחה ---
def get_mission(user):
    content = load_content()
    if not content: return None
    
    # חישוב קבוצת גיל
    age = user.get('age', 9)
    group = "7-9" if age <= 9 else "10-12" if age <= 12 else "13-15"
    
    lvl = str(user.get('level', 1))
    sub = str(user.get('sub_level', 0))
    
    # ניסיון שליפה
    try:
        return content[group][lvl][sub]
    except KeyError:
        return None

# --- עיצוב CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&display=swap');
    body { font-family: 'Heebo', sans-serif; direction: rtl; }
    .stApp { background: #f8fafc; }
    .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- לוגיקה ראשית ---
if "user" not in st.session_state: st.session_state.user = None

# 1. מסך התחברות
if st.session_state.user is None:
    st.title("🎓 ברוכים הבאים לאקדמיית האנגלית")
    db = load_db()
    
    tab1, tab2 = st.tabs(["כניסה", "הרשמה"])
    with tab1:
        name = st.selectbox("בחר שם משתמש:", list(db.keys()))
        if st.button("התחבר"):
            st.session_state.user = db[name]
            st.rerun()
    with tab2:
        with st.form("reg_form"):
            n = st.text_input("שם מלא")
            a = st.number_input("גיל", 6, 16, 9)
            if st.form_submit_button("הירשם"):
                if n not in db:
                    db[n] = {"name": n, "age": a, "level": 1, "sub_level": 0}
                    save_db(db)
                    st.session_state.user = db[n]
                    st.rerun()
                else: st.error("השם תפוס!")

# 2. מסך המשחק
else:
    user = st.session_state.user
    db = load_db()
    
    st.sidebar.title(f"היי {user['name']}! 👋")
    if st.sidebar.button("התנתק"):
        st.session_state.user = None
        st.rerun()
        
    mission = get_mission(user)
    
    if mission:
        st.markdown(f'<div class="card"><h2>{mission.get("q", "שאלה")}</h2></div>', unsafe_allow_html=True)
        
        # הצגת אפשרויות אם קיימות
        options = mission.get("options", [])
        if options:
            ans = st.radio("בחר תשובה:", options)
        else:
            ans = st.text_input("הקלד תשובה:")
            
        if st.button("בדוק תשובה"):
            if ans == mission.get("a"):
                st.success("✅ נכון מאוד!")
                # התקדמות
                user['sub_level'] += 1
                if user['sub_level'] > 7: # 8 משימות (0-7)
                    user['level'] += 1
                    user['sub_level'] = 0
                db[user['name']] = user
                save_db(db)
                st.rerun()
            else:
                st.error("❌ לא נכון, נסה שוב.")
    else:
        st.warning("עדיין אין משימות בשלב הזה, או שהקובץ ריק!")
