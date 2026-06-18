import streamlit as st
import random
import time

# --- הגדרות עמוד ---
st.set_page_config(page_title="Nexus Academy Pro", layout="wide")

# --- CSS מותאם אישית (עיצוב עתידני) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;600;900&display=swap');
    
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle at top right, #0f172a, #1e293b); color: white; font-family: 'Heebo', sans-serif; direction: rtl; }
    
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 30px; }
    
    h1, h2, h3 { color: #38bdf8 !important; text-align: right; }
    
    /* הגדלת פונטים של רדיו */
    [role="radiogroup"] label { font-size: 22px !important; color: white !important; }
    
    .stButton>button { background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important; color: white !important; border-radius: 12px !important; height: 60px !important; width: 100%; font-size: 20px !important; border: none; }
    
    .reward-box { border: 2px solid #fbbf24; border-radius: 15px; padding: 15px; background: rgba(251, 191, 36, 0.1); text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- ניהול משתמשים ונתונים ---
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.level = 1
    st.session_state.age = 12
    st.session_state.gender = "בן"
    st.session_state.inventory = []
    st.session_state.stage = "Vocab" # Vocab, Grammar, Story, Video, Boss

# --- מסך כניסה ---
if not st.session_state.user:
    st.markdown("<h1 style='text-align:center;'>NEXUS ACADEMY - כניסה למערכת</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        name = st.text_input("שם השחקן:")
        age = st.number_input("גיל:", 7, 18, 12)
        gender = st.selectbox("מגדר:", ["בן", "בת"])
        if st.button("התחל הרפתקה"):
            st.session_state.user = name
            st.session_state.age = age
            st.session_state.gender = gender
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- פונקציית פרסים ---
def get_reward(level, gender):
    rarity = "נדיר" if level > 20 else "רגיל"
    rarity = "אגדי" if level > 50 else rarity
    
    items_boy = ["קלף מסי", "כדור מוזהב", "חולצת כדורגל", "נעל זהב"]
    items_girl = ["פוקימון הולוגרפי", "גביע קריסטל", "קסם נדיר", "סיכת כוכב"]
    
    item = random.choice(items_boy if gender == "בן" else items_girl)
    return f"{rarity} ✨ {item}"

# --- בסיס נתונים (דוגמה למבנה - כאן תוסיף עוד!) ---
GAME_DB = {
    1: {"q": "What is the meaning of 'Talent'?", "options": ["כישרון", "שולחן", "ספר"], "ans": "כישרון", "type": "Vocab"},
    2: {"q": "Translate: 'Teamwork'", "options": ["עבודת צוות", "משחק", "לימוד"], "ans": "עבודת צוות", "type": "Vocab"},
    # כאן תוסיף עוד עשרות שורות בסגנון הזה...
}

# --- דשבורד בצד ---
with st.sidebar:
    st.markdown(f"## 👤 {st.session_state.user}")
    st.markdown(f"### 🛡️ רמה: {st.session_state.level}/99")
    st.markdown("---")
    st.markdown("### 🎒 הארנק שלי:")
    if not st.session_state.inventory: st.write("אין פרסים עדיין...")
    for item in st.session_state.inventory: st.markdown(f"<div class='reward-box'>{item}</div>", unsafe_allow_html=True)

# --- ממשק משחק מרכזי ---
st.markdown(f"<h1>שלב {st.session_state.level}</h1>", unsafe_allow_html=True)

# לוגיקה לדילוג רמות (לצורך הדגמה)
data = GAME_DB.get(st.session_state.level, {"q": "שלב בונוס! מה זה Apple?", "options": ["תפוח", "בננה", "עגבניה"], "ans": "תפוח"})

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown(f"<h3>{data['q']}</h3>", unsafe_allow_html=True)

# רדיו עם עיצוב גדול
choice = st.radio("בחר תשובה:", data['options'], index=None, label_visibility="collapsed")

if st.button("אישור תשובה"):
    if choice == data['ans']:
        st.success("✅ נכון מאוד!")
        st.session_state.level += 1
        
        # פרס כל 10 שלבים
        if st.session_state.level % 10 == 0:
            reward = get_reward(st.session_state.level, st.session_state.gender)
            st.session_state.inventory.append(reward)
            st.balloons()
            st.success(f"🎊 זכית בפרס: {reward}!")
            
        time.sleep(1)
        st.rerun()
    else:
        st.error("❌ טעות, נסה שוב!")
st.markdown('</div>', unsafe_allow_html=True)
