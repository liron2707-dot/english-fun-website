import streamlit as st
import json
import os

# --- הגדרות ---
st.set_page_config(page_title="SmartEnglish Academy", layout="wide")
DB_FILE = "users_db.json"
CONTENT_FILE = "content.json"

# --- פונקציות תשתית ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def ensure_content_exists():
    """יוצר את בסיס הנתונים של השאלות אם הוא לא קיים"""
    if not os.path.exists(CONTENT_FILE):
        db = {"7-9": {}, "10-12": {}, "13-15": {}}
        for age_group in db.keys():
            for level in range(1, 100):
                db[age_group][str(level)] = {}
                for sub in range(8):
                    db[age_group][str(level)][str(sub)] = {
                        "q": f"שאלה לדוגמה לשלב {level} - משימה {sub+1}",
                        "options": ["אפשרות א", "אפשרות ב", "אפשרות ג", "אפשרות ד"],
                        "a": "אפשרות א"
                    }
        save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- CSS עיצוב ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    * { font-family: 'Heebo', sans-serif; direction: rtl; }
    .stApp { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); }
    .hero { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; }
    .task-card { background: white; padding: 40px; border-radius: 25px; border: 2px solid #bae6fd; box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
    h1 { color: #0369a1 !important; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 900; background: #3b82f6; color: white; padding: 15px; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- לוגיקה ---
if "user" not in st.session_state: st.session_state.user = None

# מסך התחברות
if st.session_state.user is None:
    st.markdown('<div class="hero"><h1>🚀 SmartEnglish Adventure</h1><p>התחל את המסע שלך לאנגלית מושלמת</p></div>', unsafe_allow_html=True)
    db = load_json(DB_FILE)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.selectbox("כניסת משתמש קיים:", list(db.keys()) if db else ["אין משתמשים"])
        if st.button("התחבר"):
            st.session_state.user = db[name]
            st.rerun()
    with col2:
        with st.form("new_user"):
            n = st.text_input("שם מלא למשתמש חדש")
            a = st.number_input("גיל", 6, 16, 9)
            if st.form_submit_button("הירשם!"):
                if n and n not in db:
                    db[n] = {"name": n, "age": a, "level": 1, "sub_level": 0}
                    save_json(DB_FILE, db)
                    st.session_state.user = db[n]
                    st.rerun()
                else: st.error("השם תפוס או ריק!")

# מסך משחק
else:
    user = st.session_state.user
    db = load_json(DB_FILE)
    content = load_json(CONTENT_FILE)
    
    # ניווט
    st.sidebar.title(f"שלום {user['name']} 👋")
    st.sidebar.write(f"### רמה: {user['level']} / 99")
    st.sidebar.progress(user['level'] / 99)
    if st.sidebar.button("התנתק"):
        st.session_state.user = None
        st.rerun()

    # טעינת משימה
    group = "7-9" if user['age'] <= 9 else "10-12" if user['age'] <= 12 else "13-15"
    m = content[group][str(user['level'])][str(user['sub_level'])]
    
    st.markdown(f'<div class="hero"><h1>שלב {user["level"]} - משימה {user["sub_level"]+1}</h1></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f'<div class="task-card"><h2>{m["q"]}</h2></div>', unsafe_allow_html=True)
        ans = st.radio("בחר את התשובה הנכונה:", m["options"], key="q_radio")
        
        if st.button("בדוק תשובה ✅"):
            if ans == m["a"]:
                st.success("מעולה! מתקדמים...")
                user['sub_level'] += 1
                if user['sub_level'] > 7:
                    user['level'] += 1
                    user['sub_level'] = 0
                db[user['name']] = user
                save_json(DB_FILE, db)
                st.rerun()
            else:
                st.error("לא נכון, נסה שוב!")
