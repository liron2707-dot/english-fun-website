import streamlit as st
import json

# 1. הגדרת משתנה ה-Session State בהתחלה (חובה!)
if "user" not in st.session_state:
    st.session_state.user = None

# פונקציות הטעינה שלך (נשארות אותו דבר)
def load_content():
    if not os.path.exists("content.json"): return {}
    with open("content.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_current_mission(user):
    content = load_content()
    # ... כאן הלוגיקה שלך ...
    return mission_data

# 2. הלוגיקה המרכזית: רק אם יש משתמש - תריץ את המשחק
if st.session_state.user is None:
    # כאן אתה קורא לפונקציית ההתחברות שלך
    render_login() 
else:
    # כאן, ורק כאן, המשתמש מחובר בבטחה
    user = st.session_state.user # הגדרת המשתנה בצורה בטוחה
    
    # עכשיו בטוח להשתמש בו:
    mission = get_current_mission(user)
    
    # כאן תמשיך להציג את המשחק
    st.write(f"שלום {user['name']}, בוא נתחיל!")
