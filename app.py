import streamlit as st
import json
import os

# --- הגדרות ---
DB_FILE = "users_db.json"
CONTENT_FILE = "content.json"

st.set_page_config(page_title="English Academy", layout="wide")

# --- פונקציות תשתית בטוחות ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def initialize_system():
    """מייצר את בסיס הנתונים של השאלות אם הוא לא קיים"""
    if not os.path.exists(CONTENT_FILE):
        db = {"7-9": {}, "10-12": {}, "13-15": {}}
        for age_group in db.keys():
            for level in range(1, 100):
                db[age_group][str(level)] = {}
                for sub in range(8):
                    db[age_group][str(level)][str(sub)] = {
                        "q": f"שאלה לדוגמה לשלב {level}, משימה {sub+1}",
                        "options": ["תשובה א", "תשובה ב", "תשובה ג", "תשובה ד"],
                        "a": "תשובה א"
                    }
        save_json(CONTENT_FILE, db)

# הרצה ראשונית של המערכת
initialize_system()

# --- לוגיקה וניהול משתמש ---
if "user" not in st.session_state:
    st.session_state.user = None

def get_mission(user, content):
    """שולפת משימה בצורה בטוחה בלי לגרום לקריסת המערכת"""
    age = user.get('age', 9)
    group = "7-9" if age <= 9 else "10-12" if age <= 12 else "13-15"
    lvl = str(user.get('level', 1))
    sub = str(user.get('sub_level', 0))
    
    # בודקים אם המפתח קיים לפני שניגשים אליו
    if group in content and lvl in content[group] and sub in content[group][lvl]:
        return content[group][lvl][sub]
    return None

# --- ממשק משתמש ---
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

if st.session_state.user is None:
    st.title("🎓 ברוכים הבאים")
    # טאב כניסה
    name = st.selectbox("בחר משתמש:", list(db.keys()) if db else ["אין משתמשים"])
    if st.button("התחבר"):
        if name in db:
            st.session_state.user = db[name]
            st.rerun()
    
    # טאב הרשמה
    with st.expander("משתמש חדש? הירשם כאן"):
        n = st.text_input("שם מלא")
        a = st.number_input("גיל", 6, 16, 9)
        if st.button("הירשם"):
            if n and n not in db:
                db[n] = {"name": n, "age": a, "level": 1, "sub_level": 0}
                save_json(DB_FILE, db)
                st.session_state.user = db[n]
                st.rerun()

else:
    user = st.session_state.user
    
    # ניווט
    if st.sidebar.button("התנתק"):
        st.session_state.user = None
        st.rerun()
        
    st.sidebar.write(f"היי {user['name']}! רמה: {user['level']}")
    
    # טעינת משימה
    mission = get_mission(user, content)
    
    if mission:
        st.header(f"שלב {user['level']} - משימה {int(user['sub_level'])+1}")
        st.info(mission["q"])
        
        ans = st.radio("בחר תשובה:", mission["options"])
        
        if st.button("בדוק"):
            if ans == mission["a"]:
                st.success("כל הכבוד! עוברים לשלב הבא")
                # עדכון התקדמות
                user['sub_level'] += 1
                if user['sub_level'] > 7:
                    user['level'] += 1
                    user['sub_level'] = 0
                
                # שמירה
                db[user['name']] = user
                save_json(DB_FILE, db)
                st.session_state.user = user
                st.rerun()
            else:
                st.error("לא נורא, נסה שוב!")
    else:
        st.warning("השלב הנוכחי טרם הוגדר בתוכן.")
        if st.button("אפס התקדמות לחזרה להתחלה"):
            user['level'] = 1
            user['sub_level'] = 0
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
