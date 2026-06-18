import streamlit as st
import random
import time

# --- הגדרות עמוד ---
st.set_page_config(page_title="SmartEnglish Pro", layout="wide", initial_sidebar_state="expanded")

# --- CSS משופר (תיקון פונטים ו-RTL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;600;900&display=swap');
    
    /* יישור לימין לכל האפליקציה */
    .stApp { direction: rtl; font-family: 'Heebo', sans-serif; }
    
    /* תיקון גודל פונט לרדיו ותשובות */
    [data-testid="stRadio"] label p { font-size: 22px !important; font-weight: bold; }
    
    /* עיצוב כרטיסיות */
    .big-card { background: #ffffff; padding: 30px; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); border: 2px solid #e0f2fe; }
    
    h1, h2 { color: #0369a1 !important; text-align: right; }
    
    .stButton>button { width: 100%; height: 60px; font-size: 22px !important; border-radius: 15px !important; background: linear-gradient(to right, #3b82f6, #2563eb) !important; color: white !important; }
    
    .sidebar-content { font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# --- ניהול משתמשים (Memory) ---
if 'profile' not in st.session_state:
    st.session_state.profile = None

# --- דף כניסה ---
if st.session_state.profile is None:
    st.title("🚀 ברוכים הבאים לאקדמיית האנגלית")
    with st.form("login"):
        name = st.text_input("שם הילד/ה:")
        age = st.number_input("גיל:", 6, 18, 9)
        gender = st.selectbox("מגדר:", ["בן", "בת"])
        if st.form_submit_button("התחל משחק"):
            st.session_state.profile = {
                "name": name, "age": age, "gender": gender, 
                "level": 1, "score": 0, "rewards": []
            }
            st.rerun()
    st.stop()

# --- פונקציות עזר למנוע המשחק ---
def get_reward(level, gender):
    # לוגיקת נדירות
    rarity = "נדיר" if level > 10 else "רגיל"
    rarity = "אגדי" if level > 30 else rarity
    rarity = "מיתולוגי" if level > 50 else rarity
    
    # בנק פרסים לפי מגדר
    if gender == "בן":
        items = ["⚽ קלף שחקן ליגת האלופות", "⚡ פוקימון אגדי", "🏎️ מכונית מרוץ זהב"]
    else:
        items = ["🦄 חד קרן קסום", "✨ שרביט כוכבים", "🎨 ערכת צבעים מלכותית"]
        
    return f"{rarity} ✨ {random.choice(items)}"

# --- מסד נתונים (תוכל להרחיב כאן ל-99 שלבים) ---
# הערה: פה הוספתי דוגמה לאיך בונים שלב. אפשר לייצר פונקציה שתגריל שאלות לפי גיל.
def get_level_data(level):
    # רמת קושי עולה ככל שה-level גבוה יותר
    return {
        "title": f"שלב {level}: הרפתקה באנגלית",
        "question": f"מה התרגום הנכון ל-Level {level}?",
        "options": ["אופציה א", "אופציה ב", "אופציה ג"],
        "correct": "אופציה א",
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # שנה לכל שלב
    }

# --- דשבורד בצד (הנתונים של הילד) ---
with st.sidebar:
    p = st.session_state.profile
    st.write(f"## 👤 {p['name']}")
    st.write(f"### 🛡️ שלב: {p['level']}")
    st.progress(min((p['level']-1)/99, 1.0))
    st.write("---")
    st.write("### 🎒 הארנק שלי:")
    for r in p['rewards']: st.write(f"- {r}")

# --- ממשק המשחק ---
p = st.session_state.profile
data = get_level_data(p['level'])

st.markdown(f"<h1>{data['title']}</h1>", unsafe_allow_html=True)
st.video(data['video'])

st.markdown('<div class="big-card">', unsafe_allow_html=True)
st.subheader(data['question'])
choice = st.radio("בחר תשובה:", data['options'], index=None)

if st.button("בדוק תשובה"):
    if choice == data['correct']:
        st.success("✅ כל הכבוד!")
        p['score'] += 100
        p['level'] += 1
        
        # זכייה בפרס כל 5 שלבים
        if p['level'] % 5 == 0:
            reward = get_reward(p['level'], p['gender'])
            p['rewards'].append(reward)
            st.balloons()
            st.success(f"🎊 זכית בפרס חדש: {reward}")
            
        time.sleep(1)
        st.rerun()
    else:
        st.error("❌ לא נורא, נסה שוב.")
st.markdown('</div>', unsafe_allow_html=True)
