import streamlit as st
import json
import os

# --- הגדרות ---
DB_FILE = "users_db.json"
CONTENT_FILE = "content.json"

st.set_page_config(page_title="SmartEnglish Academy", layout="wide")

# --- פונקציית המפעל: מייצרת את כל 99 השלבים אוטומטית ---
def generate_all_levels():
    if os.path.exists(CONTENT_FILE):
        return # הקובץ כבר קיים, לא לדרוס

    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מבנה המשימות (8 משימות לכל שלב)
    tasks_types = ["vocab", "spelling", "grammar", "reading", "video", "tf", "game", "boss"]
    
    for age_group in db.keys():
        for level in range(1, 100): # 99 שלבים
            db[age_group][str(level)] = {}
            for sub in range(8):
                # מילוי אוטומטי של שלד השאלות
                db[age_group][str(level)][str(sub)] = {
                    "type": tasks_types[sub],
                    "q": f"שאלה {sub+1} לשלב {level} - קבוצת גיל {age_group}",
                    "a": "תשובה",
                    "options": ["תשובה 1", "תשובה 2", "תשובה 3", "תשובה 4"]
                }
    
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# הרצה ראשונית של המפעל
generate_all_levels()

# --- פונקציות טעינה ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- לוגיקה ---
if "user" not in st.session_state: st.session_state.user = None

db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# ממשק משתמש
if st.session_state.user is None:
    st.title("🎓 SmartEnglish Academy")
    n = st.text_input("שם משתמש")
    a = st.number_input("גיל", 7, 15, 9)
    if st.button("התחל לשחק"):
        db[n] = {"name": n, "age": a, "level": 1, "sub_level": 0}
        save_json(DB_FILE, db)
        st.session_state.user = db[n]
        st.rerun()
else:
    user = st.session_state.user
    age_group = "7-9" if user['age'] <= 9 else "10-12" if user['age'] <= 12 else "13-15"
    
    # ניסיון שליפת משימה
    try:
        mission = content[age_group][str(user['level'])][str(user['sub_level'])]
        
        st.header(f"שלב {user['level']} | משימה {int(user['sub_level'])+1}")
        st.subheader(mission['q'])
        
        ans = st.radio("בחר תשובה:", mission['options'])
        
        if st.button("בדוק תשובה"):
            if ans == mission['a']:
                st.success("נכון! עובר למשימה הבאה...")
                user['sub_level'] += 1
                if user['sub_level'] > 7:
                    user['level'] += 1
                    user['sub_level'] = 0
                db[user['name']] = user
                save_json(DB_FILE, db)
                st.rerun()
            else:
                st.error("לא נכון, נסה שוב")
    except:
        st.write("סיימת את כל השלבים! כל הכבוד!")
        if st.button("איפוס"):
            user['level'] = 1
            user['sub_level'] = 0
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
