import streamlit as st
import random

# --- עיצוב עתידני (Cyber-Glassmorphism) ---
st.set_page_config(page_title="Nexus Academy", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600;900&display=swap');
    
    [data-testid="stAppViewContainer"] { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
        color: white; font-family: 'Outfit', sans-serif; 
    }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); 
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 40px; 
    }
    h1 { color: #38bdf8 !important; text-align: center; }
    .stButton>button { 
        background: linear-gradient(90deg, #38bdf8, #818cf8) !important; 
        color: white !important; border: none !important; border-radius: 12px !important;
        font-weight: 600 !important; height: 55px !important; width: 100%; 
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(56, 189, 248, 0.4); }
    .rtl { direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

# --- כאן התוכן שלך (כאן אתה מוסיף 99 שלבים!) ---
# כל שלב הוא אובייקט. אפשר להוסיף עוד מאות כאלה.
GAME_DB = {
    1: {"q": "What is the meaning of 'Talent'?", "options": ["כישרון", "שולחן", "ספר"], "ans": "כישרון"},
    2: {"q": "Translate: 'Teamwork'", "options": ["עבודת צוות", "משחק", "לימוד"], "ans": "עבודת צוות"},
    3: {"q": "Complete: I ___ singing now.", "options": ["am", "is", "are"], "ans": "am"},
}

# --- ניהול משתמשים (State) ---
if 'user' not in st.session_state:
    st.session_state.update({'user': None, 'level': 1, 'inv': []})

# --- מסך כניסה ---
if not st.session_state.user:
    st.markdown("<h1>NEXUS ACADEMY</h1>", unsafe_allow_html=True)
    with st.container():
        name = st.text_input("שם השחקן:")
        if st.button("התחבר למערכת"):
            st.session_state.user = name
            st.rerun()
    st.stop()

# --- ממשק המשחק ---
st.sidebar.markdown(f"## 👤 {st.session_state.user}")
st.sidebar.markdown(f"### 🛡️ רמה: {st.session_state.level}")
st.sidebar.markdown("---")
st.sidebar.write("🎒 **ארנק פרסים:**")
for item in st.session_state.inv: st.write(item)

# מציג את השלב הנוכחי מהמאגר
current_data = GAME_DB.get(st.session_state.level, {"q": "סיימת את כל השלבים!", "options": [], "ans": ""})

st.markdown('<div class="glass-card rtl">', unsafe_allow_html=True)
st.markdown(f"<h1>שלב {st.session_state.level}</h1>", unsafe_allow_html=True)

if st.session_state.level <= len(GAME_DB):
    st.markdown(f"### {current_data['q']}")
    choice = st.radio("בחר תשובה:", current_data['options'], label_visibility="collapsed")
    
    if st.button("בדוק תשובה"):
        if choice == current_data['ans']:
            st.success("✅ נכון! ממשיכים לשלב הבא")
            
            # פרס כל 10 שלבים
            if st.session_state.level % 10 == 0:
                st.session_state.inv.append("⚽ קלף כדורגל נדיר")
            
            st.session_state.level += 1
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ טעות, נסה שוב!")
else:
    st.balloons()
    st.write("🎉 כל הכבוד! הגעת לקצה הרמה.")

st.markdown('</div>', unsafe_allow_html=True)
