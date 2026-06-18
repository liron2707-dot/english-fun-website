import streamlit as st
import json
import os

# --- קבועים וקונפיגורציה ---
DB_FILE = "users_db.json"
st.set_page_config(page_title="SmartEnglish Academy", layout="wide")

# --- פונקציות מסד נתונים ---
def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f:
        try: return json.load(f)
        except: return {}

def save_db(db):
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

# --- ניהול משתמשים (Auth) ---
def login_or_register():
    st.title("🎓 ברוכים הבאים לאקדמיית האנגלית")
    db = load_db()
    
    # בחירת פעולה
    action = st.radio("מה תרצה לעשות?", ["אני כבר רשום (כניסה)", "אני חדש כאן (הרשמה)"])
    
    if action == "אני כבר רשום (כניסה)":
        if not db:
            st.warning("אין עדיין משתמשים במערכת. הירשם כמשתמש חדש.")
        else:
            username = st.selectbox("בחר את השם שלך:", list(db.keys()))
            if st.button("התחבר למשחק"):
                st.session_state.user = db[username]
                st.rerun()
                
    else: # הרשמה
        with st.form("register_form"):
            name = st.text_input("שם מלא:")
            age = st.number_input("גיל:", 6, 18, 9)
            gender = st.selectbox("מגדר:", ["בן", "בת"])
            
            if st.form_submit_button("הירשם והתחל לשחק"):
                if name in db:
                    st.error("השם הזה כבר תפוס! בחר שם אחר.")
                elif name.strip() == "":
                    st.error("חובה להזין שם.")
                else:
                    new_user = {
                        "name": name, "age": age, "gender": gender,
                        "level": 1, "sub_level": 0, "rewards": []
                    }
                    db[name] = new_user
                    save_db(db)
                    st.session_state.user = new_user
                    st.success("נרשמת בהצלחה! מעביר אותך למשחק...")
                    st.rerun()

# --- לוגיקת המשחק הראשית ---
def run_game():
    user = st.session_state.user
    st.sidebar.title(f"שלום {user['name']}! 👋")
    st.sidebar.write(f"גיל: {user['age']} | רמה: {user['level']}")
    
    if st.sidebar.button("התנתק"):
        st.session_state.user = None
        st.rerun()

    # אזור התוכן המרכזי
    st.title(f"שלב {user['level']}")
    st.write("כאן תופיע המשימה הנוכחית...")
    
    # דוגמה ללוגיקת התקדמות
    if st.button("סיימתי משימה"):
        user['sub_level'] += 1
        if user['sub_level'] >= 8:
            user['level'] += 1
            user['sub_level'] = 0
            st.balloons()
            
        # שמירה אוטומטית ל-DB
        db = load_db()
        db[user['name']] = user
        save_db(db)
        st.rerun()

# --- נקודת התחלה ---
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    login_or_register()
else:
    run_game()
