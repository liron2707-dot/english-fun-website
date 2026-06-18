import streamlit as st
import random
import json
import time

# --- הגדרות עמוד ---
st.set_page_config(page_title="Nexus English Academy", layout="wide")

# --- CSS מעוצב ---
st.markdown("""
    <style>
    .stApp { direction: rtl; font-family: 'Heebo', sans-serif; background: #f8fafc; }
    .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .mission-title { color: #0f172a; font-size: 24px; font-weight: bold; }
    .reward-box { background: #fef3c7; border: 2px dashed #f59e0b; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- ניהול משתמשים (התחברות ושמירה) ---
if 'user' not in st.session_state:
    st.session_state.user = None

def save_game():
    data = json.dumps(st.session_state.user)
    st.download_button("💾 שמור התקדמות למחשב", data, file_name="my_progress.json")

def load_game():
    uploaded_file = st.file_uploader("📂 טען התקדמות קיימת", type="json")
    if uploaded_file is not None:
        st.session_state.user = json.load(uploaded_file)
        st.rerun()

# --- דף כניסה ---
if not st.session_state.user:
    st.title("🎓 Nexus English Academy")
    load_game()
    with st.form("login_form"):
        name = st.text_input("שם:")
        age = st.number_input("גיל:", 6, 18, 9)
        gender = st.selectbox("מגדר:", ["בן", "בת"])
        if st.form_submit_button("התחל הרפתקה!"):
            st.session_state.user = {
                "name": name, "age": age, "gender": gender,
                "level": 1, "sub_level": 0, "rewards": []
            }
            st.rerun()
    st.stop()

# --- לוגיקת תוכן (מנוע שלבים) ---
def get_mission_content(level, sub_level, age):
    # כאן אפשר להוסיף לוגיקה שמגדילה את הקושי לפי הגיל
    difficulty = "קל" if age < 10 else "בינוני" if age < 14 else "קשה"
    
    missions = [
        {"title": "מילים: מצא את הזוג", "type": "vocab"},
        {"title": "איות: סדר את האותיות", "type": "scramble"},
        {"title": "דקדוק: השלם את המשפט", "type": "grammar"},
        {"title": "קריאה: הבנת הנקרא", "type": "story"},
        {"title": "הקשבה: צפה בסרטון", "type": "video"},
        {"title": "נכון או לא נכון", "type": "tf"},
        {"title": "משחק זיכרון", "type": "memory"},
        {"title": "הבוס הגדול!", "type": "boss"}
    ]
    return missions[sub_level], difficulty

# --- דשבורד בצד ---
with st.sidebar:
    u = st.session_state.user
    st.write(f"## 👤 שלום {u['name']}")
    st.write(f"### 🏆 רמה: {u['level']} / 99")
    st.progress(u['sub_level'] / 8)
    save_game()
    st.write("---")
    st.write("### 🎒 התיק שלי:")
    for r in u['rewards']: st.write(r)

# --- ממשק המשימות ---
mission, diff = get_mission_content(st.session_state.user['level'], st.session_state.user['sub_level'], st.session_state.user['age'])

st.markdown(f'<div class="card"><div class="mission-title">{mission["title"]} ({diff})</div></div>', unsafe_allow_html=True)

# תצוגת משימות לפי סוג
if mission['type'] == 'video':
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # החלף בקישור רלוונטי
    if st.button("סיימתי לצפות"):
        st.session_state.user['sub_level'] += 1
        st.rerun()

elif mission['type'] == 'boss':
    st.warning("זהו שלב הבוס! ענה נכון כדי לעבור רמה.")
    if st.button("ניצחתי את הבוס!"):
        st.session_state.user['level'] += 1
        st.session_state.user['sub_level'] = 0
        
        # מתן פרס כל 10 שלבים
        if st.session_state.user['level'] % 10 == 0:
            reward = "✨ פרס נדיר: קלף פוקימון זהב" if st.session_state.user['gender'] == "בן" else "🦄 פרס נדיר: חדי קרן קסומים"
            st.session_state.user['rewards'].append(reward)
            st.balloons()
        st.rerun()

else:
    # כאן אתה שם את השאלות שלך לכל משימה
    st.write(f"שאלה לדוגמה עבור משימת ה-{mission['type']}...")
    if st.button("הגש תשובה"):
        st.session_state.user['sub_level'] += 1
        st.rerun()
