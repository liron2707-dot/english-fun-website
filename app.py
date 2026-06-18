import streamlit as st
import time

# --- הגדרות בסיס ---
st.set_page_config(page_title="Nexus English Academy", layout="wide")

# --- CSS עתידני ומודרני (Cyber-Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;600;900&display=swap');
    
    /* עיצוב כללי - עתידני */
    body, [data-testid="stAppViewContainer"] { 
        background: radial-gradient(circle at center, #0f172a, #020617);
        color: white; 
        font-family: 'Heebo', sans-serif;
        direction: rtl;
    }
    
    /* כרטיסיות שקופות */
    .glass-card { 
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* טיפוגרפיה */
    h1, h2, h3 { color: #38bdf8 !important; text-align: right; }
    
    /* כפתורים מודרניים */
    .stButton>button { 
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 30px !important;
        font-weight: 900 !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover { transform: scale(1.05); filter: brightness(1.2); }
    
    /* יישור לימין */
    .rtl { text-align: right; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# --- ניהול ה-State (כדי שלא יהיו שגיאות) ---
def init_session():
    if 'initialized' not in st.session_state:
        st.session_state.user = None
        st.session_state.level = 1
        st.session_state.inv = []
        st.session_state.initialized = True
        st.session_state.points = 0

init_session()

# --- מאגר השלבים (כאן מוסיפים את כל ה-99 שלבים) ---
GAME_DB = {
    1: {"q": "What is the meaning of 'Talent'?", "options": ["כישרון", "שולחן", "ספר"], "ans": "כישרון"},
    2: {"q": "Translate: 'Teamwork'", "options": ["עבודת צוות", "משחק", "לימוד"], "ans": "עבודת צוות"},
    3: {"q": "What is the opposite of 'Old'?", "options": ["חדש", "גדול", "מהיר"], "ans": "חדש"},
}

# --- לוגיקת המערכת ---
if not st.session_state.user:
    st.markdown("<h1 style='text-align:center;'>🚀 NEXUS ACADEMY</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        name = st.text_input("הכנס שם שחקן:")
        if st.button("התחל מסע"):
            if name:
                st.session_state.user = name
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- סרגל צד (Dashboard) ---
with st.sidebar:
    st.markdown(f"## 👤 שחקן: {st.session_state.user}")
    st.markdown(f"### 🛡️ רמה: {st.session_state.level}")
    st.markdown("---")
    st.markdown("### 🎒 הארנק שלי:")
    if not st.session_state.inv:
        st.write("עדיין אין פריטים בארנק...")
    for item in st.session_state.inv:
        st.success(f"✨ {item}")

# --- לוגיקת המשחק הראשית ---
st.markdown(f"<h1>שלב {st.session_state.level}</h1>", unsafe_allow_html=True)
st.markdown('<div class="glass-card rtl">', unsafe_allow_html=True)

current_data = GAME_DB.get(st.session_state.level)

if current_data:
    st.markdown(f"<h3>{current_data['q']}</h3>", unsafe_allow_html=True)
    choice = st.radio("בחר:", current_data['options'], label_visibility="collapsed")
    
    if st.button("אישור תשובה ⚡"):
        if choice == current_data['ans']:
            st.success("✅ תשובה נכונה! מתקדם לשלב הבא...")
            
            # פרס כל 10 שלבים
            if st.session_state.level % 10 == 0:
                reward = "קלף פוקימון נדיר"
                st.session_state.inv.append(reward)
            
            st.session_state.level += 1
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ טעות! נסה שוב.")
else:
    st.balloons()
    st.write("🎉 סיימת את כל השלבים הזמינים!")

st.markdown('</div>', unsafe_allow_html=True)
