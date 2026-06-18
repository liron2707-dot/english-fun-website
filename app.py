import streamlit as st
import json
import os  # <--- זה החלק שהיה חסר!

# --- 1. טעינת נתונים ---
def load_content():
    # בדיקה אם הקובץ קיים לפני שקוראים לו
    if not os.path.exists("content.json"): 
        st.error("הקובץ content.json לא נמצא בתיקייה!")
        return {}
    with open("content.json", "r", encoding="utf-8") as f:
        return json.load(f)

# --- 2. לוגיקת המשימה ---
def get_current_mission(user):
    content = load_content()
    if not content: return None
    
    age_group = "7-9" if user['age'] <= 9 else "10-12" if user['age'] <= 12 else "13-15"
    level = str(user['level'])
    sub_level = str(user['sub_level'])
    
    try:
        return content[age_group][level][sub_level]
    except KeyError:
        return {"type": "error", "q": "לא נמצאה משימה", "a": "סיום"}

# --- 3. ניהול מצב (State) ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- 4. הממשק הראשי ---
def main():
    # אם אין משתמש, הצג מסך התחברות
    if st.session_state.user is None:
        st.title("ברוכים הבאים לאקדמיה")
        # כאן תשים את מסך ההתחברות שלך...
        # למטרת בדיקה, נניח שהגדרנו משתמש
        if st.button("התחבר"):
            st.session_state.user = {"name": "Test", "age": 9, "level": 1, "sub_level": 0}
            st.rerun()
    else:
        # אם יש משתמש, אפשר בבטחה לקרוא לפונקציה
        user = st.session_state.user
        mission = get_current_mission(user)
        
        st.write(f"שלום {user['name']}!")
        st.json(mission) # כאן יופיע התוכן

if __name__ == "__main__":
    main()
