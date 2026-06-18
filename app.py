import streamlit as st
import json
import os
import random

# --- הגדרות מסד נתונים ---
DB_FILE = "users_db.json"

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f:
        try: return json.load(f)
        except: return {}

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

def delete_user(username):
    db = load_db()
    if username in db:
        del db[username]
        save_db(db)
        return True
    return False

# --- מנוע תוכן (Content Generator) ---
def get_mission(age, level, sub_level):
    # הגדרת רמת קושי
    if age <= 9: group = "7-9"
    elif age <= 12: group = "10-12"
    else: group = "13-15"

    # בנק משימות לכל קבוצת גיל (כאן אתה מוסיף תוכן)
    content_map = {
        "7-9": {
            "vocab": {"q": "תרגם: Dog", "a": "כלב"},
            "grammar": {"q": "He ____ (eat) an apple.", "a": "eats"}
        },
        "10-12": {
            "vocab": {"q": "תרגם: Environment", "a": "סביבה"},
            "grammar": {"q": "I ____ (go) to the park yesterday.", "a": "went"}
        },
        "13-15": {
            "vocab": {"q": "תרגם: Sophisticated", "a": "מתוחכם"},
            "grammar": {"q": "If I ____ (be) you, I would go.", "a": "were"}
        }
    }
    
    # תיאורי המשימות
    mission_types = [
        "אוצר מילים", "איות", "דקדוק", "קריאה", 
        "הבנת הנשמע", "נכון/לא נכון", "משחק זיכרון", "קרב בוס!"
    ]
    
    return {
        "title": mission_types[sub_level],
        "content": content_map[group].get(list(content_map[group].keys())[sub_level % 2], {"q": "משימה כללית", "a": "כן"})
    }

# --- ממשק משתמש ---
st.set_page_config(page_title="Nexus Academy", layout="wide")

if "user" not in st.session_state: st.session_state.user = None

# כניסה/הרשמה
if st.session_state.user is None:
    st.title("🎓 Nexus Academy")
    db = load_db()
    
    tab1, tab2 = st.tabs(["כניסה", "הרשמה"])
    
    with tab1:
        name = st.selectbox("בחר משתמש:", list(db.keys()))
        if st.button("כניסה"):
            st.session_state.user = db[name]
            st.rerun()
            
    with tab2:
        with st.form("reg"):
            n = st.text_input("שם:")
            a = st.number_input("גיל:", 6, 18, 9)
            if st.form_submit_button("הירשם"):
                db[n] = {"name": n, "age": a, "level": 1, "sub_level": 0, "rewards": []}
                save_db(db)
                st.session_state.user = db[n]
                st.rerun()
    st.stop()

# --- אזור המשחק ---
user = st.session_state.user
db = load_db()

# סרגל צד
with st.sidebar:
    st.header(f"שלום {user['name']} 🛡️")
    st.write(f"רמה: {user['level']} | קבוצת גיל: {user['age']}")
    st.progress(user['sub_level'] / 8)
    
    st.write("### 🎒 תיק פרסים:")
    for r in user['rewards']: st.write(f"⭐ {r}")
    
    if st.button("❌ מחק משתמש"):
        delete_user(user['name'])
        st.session_state.user = None
        st.rerun()
    if st.button("התנתק"):
        st.session_state.user = None
        st.rerun()

# לוגיקת המשימות
mission = get_mission(user['age'], user['level'], user['sub_level'])
st.title(f"שלב {user['level']} - {mission['title']}")
st.info(mission['content']['q'])

if st.button("הגש תשובה"):
    user['sub_level'] += 1
    # מעבר שלב
    if user['sub_level'] >= 8:
        user['level'] += 1
        user['sub_level'] = 0
        # פרס כל 10 שלבים
        if user['level'] % 10 == 0:
            reward = "✨ גביע הזהב"
            user['rewards'].append(reward)
            st.balloons()
            
    # שמירה ל-DB
    db[user['name']] = user
    save_db(db)
    st.rerun()
