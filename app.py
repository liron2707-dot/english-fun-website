import streamlit as st
import json
import os
import random
import time

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English Adventure", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")

DB_FILE = "users_db.json"
CONTENT_FILE = "content.json"

# --- פונקציות תשתית ומסד נתונים ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def delete_user(username):
    db = load_json(DB_FILE)
    if username in db:
        del db[username]
        save_json(DB_FILE, db)
        return True
    return False

# --- מנוע יצירת תוכן (המפעל) ---
def ensure_content_exists():
    """מייצר את כל 99 השלבים ו-8 המשימות לכל רמת גיל"""
    if os.path.exists(CONTENT_FILE): return

    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # תבניות תוכן מיוחדות לשלבים הראשונים (משולב עם פנטזיה, כדורגל וסיפורים)
    templates = [
        {
            "theme": "The Talent Show 🎤", 
            "story": "Today is the talent show! Ben and Sarah show great teamwork in their performance.",
            "boss_reward": "🏆 גביע כוכב נולד מהספר Teamwork"
        },
        {
            "theme": "The Match Attax 2025 Master ⚽", 
            "story": "Mike is building his ultimate football team. He just found an ultra-rare card and made a legendary combo!",
            "boss_reward": "⚽ קלף Match Attax 2025 זוהר נדיר 100!"
        },
        {
            "theme": "Catch Them All ⚡", 
            "story": "The young trainer walks into the tall grass. Suddenly, a wild electric creature appears for a battle!",
            "boss_reward": "⚡ תג פוקימון הולוגרפי"
        },
        {
            "theme": "The Upside Down Mystery 🔦", 
            "story": "Four friends ride their bikes at night with flashlights. They see something strange in the sky.",
            "boss_reward": "🚲 מדבקת מועדון Hellfire"
        }
    ]

    for age_group in db.keys():
        for level in range(1, 100):
            db[age_group][str(level)] = {}
            
            # בחירת נושא (תבניות מיוחדות לשלבים 1-4, ואז נושאים כלליים)
            t = templates[level-1] if level <= len(templates) else {"theme": f"Galaxy Mission {level} 🚀", "story": "An amazing adventure in space awaits you.", "boss_reward": f"💎 קריסטל חלל {level}"}
            
            # יצירת 8 משימות לכל שלב
            for sub in range(8):
                task_data = {}
                if sub == 0:
                    task_data = {"type": "vocab", "title": "מילים", "q": f"איך כותבים מילה חשובה מתוך {t['theme']}?", "a": "Word", "options": ["Word", "Sword", "Bird", "Board"]}
                elif sub == 1:
                    task_data = {"type": "scramble", "title": "פיצוח מילה", "q": "סדר את האותיות למילה נכונה:", "a": "TEAM", "hint": "קבוצה של אנשים שעובדים יחד"}
                elif sub == 2:
                    task_data = {"type": "grammar", "title": "דקדוק", "q": "בחר את הזמן הנכון (Present Progressive): I ____ playing right now.", "a": "am", "options": ["am", "is", "are", "was"]}
                elif sub == 3:
                    task_data = {"type": "story", "title": "סיפור (Unseen)", "text": t['story'], "q": "What is the main idea of the story?", "a": "An exciting adventure", "options": ["An exciting adventure", "Going to sleep", "Eating lunch", "Cleaning the room"]}
                elif sub == 4:
                    task_data = {"type": "video", "title": "וידאו", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "q": "מה הנושא המרכזי ששמעת?", "a": "Music", "options": ["Music", "Cooking", "Sports", "Sleeping"]}
                elif sub == 5:
                    task_data = {"type": "tf", "title": "נכון או לא נכון", "q": "The sky is usually green. (True/False)", "a": "False", "options": ["True", "False"]}
                elif sub == 6:
                    task_data = {"type": "game", "title": "משחקון", "q": "מצא את המילה הנרדפת ל-Happy:", "a": "Glad", "options": ["Sad", "Glad", "Angry", "Mad"]}
                elif sub == 7:
                    task_data = {"type": "boss", "title": "קרב בוס! 🐉", "q": f"שאלת הבוס לשלב {level}! האם אתה מוכן?", "a": "Yes", "options": ["Yes", "No", "Maybe", "Never"], "reward": t['boss_reward']}
                
                db[age_group][str(level)][str(sub)] = task_data

    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- עיצוב CSS עתידני ומרהיב ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Heebo', sans-serif; direction: rtl;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc;
    }
    
    /* קלפים עתידניים */
    .glass-card { 
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        padding: 40px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 0 40px rgba(99, 102, 241, 0.2); text-align: center; margin-bottom: 20px;
    }
    
    h1 { color: #818cf8 !important; font-size: 3.5rem !important; text-shadow: 0 0 20px rgba(129, 140, 248, 0.5); font-weight: 900;}
    h2, h3 { color: #c7d2fe !important; }
    
    /* כפתורים מוארים */
    .stButton>button { 
        background: linear-gradient(90deg, #4f46e5, #ec4899) !important; color: white !important;
        font-size: 22px !important; font-weight: 900 !important; border-radius: 16px !important;
        padding: 15px 30px !important; border: none !important; width: 100%; 
        box-shadow: 0 10px 20px rgba(236, 72, 153, 0.3); transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-5px) scale(1.02); box-shadow: 0 15px 25px rgba(236, 72, 153, 0.5); }
    
    /* סרגל התקדמות */
    .progress-track {
        display: flex; justify-content: space-between; background: rgba(0,0,0,0.3);
        padding: 15px 30px; border-radius: 50px; border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 30px; font-weight: bold;
    }
    .step-done { color: #34d399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.5); }
    .step-active { color: #f472b6; font-weight: 900; text-shadow: 0 0 10px rgba(244, 114, 182, 0.8); font-size: 1.1em;}
    .step-lock { color: #64748b; }
    
    .stRadio>div { direction: rtl; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 12px; }
    .stTextInput>div>div>input { text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- לוגיקה וניהול משתמש ---
if "user" not in st.session_state: st.session_state.user = None
if "score" not in st.session_state: st.session_state.score = 0

db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# ==========================================
# מסך התחברות והרשמה
# ==========================================
if st.session_state.user is None:
    st.markdown('<div class="glass-card"><h1>🌌 NEXUS ACADEMY</h1><p style="font-size:24px;">האקדמיה הדיגיטלית ללימוד אנגלית</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔑 התחברות שחקן חוזר")
        name = st.selectbox("בחר את השחקן שלך:", list(db.keys()) if db else ["אין משתמשים"])
        if st.button("היכנס למשחק 🚀"):
            if name in db:
                st.session_state.user = db[name]
                st.session_state.score = db[name].get('level', 1) * 100
                st.rerun()
                
    with col2:
        st.markdown("### ✨ יצירת שחקן חדש")
        new_name = st.text_input("שם השחקן:")
        new_age = st.number_input("גיל:", 7, 15, 12)
        if st.button("צור שחקן והתחל 🎮"):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.session_state.score = 100
                st.balloons()
                st.rerun()
            elif new_name in db:
                st.error("השם כבר תפוס! בחר שם אחר.")

# ==========================================
# מסך המשחק הראשי
# ==========================================
else:
    user = st.session_state.user
    
    # תפריט צד (Sidebar)
    with st.sidebar:
        st.markdown(f"<h2 style='text-align:center;'>סוכן: {user['name']} 🕵️‍♂️</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center; color:#f472b6 !important;'>ניקוד: {st.session_state.score} 💎</h3>", unsafe_allow_html=True)
        st.progress(user['level'] / 99)
        st.write(f"רמה {user['level']} מתוך 99")
        
        st.markdown("---")
        st.markdown("### 🎒 אוסף הפרסים שלי:")
        if not user.get('rewards'):
            st.write("עדיין אין פרסים... הבס את הבוס כדי להרוויח!")
        for r in user.get('rewards', []):
            st.markdown(f"<div style='background:rgba(255,255,255,0.1); padding:10px; border-radius:8px; margin-bottom:5px;'>⭐ {r}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("התנתק 🚪"):
            st.session_state.user = None
            st.rerun()
        if st.button("מחק משתמש ⚠️"):
            delete_user(user['name'])
            st.session_state.user = None
            st.rerun()

    # שליפת המשימה הנוכחית
    age_group = "7-9" if user['age'] <= 9 else "10-12" if user['age'] <= 12 else "13-15"
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    try:
        mission = content[age_group][lvl][sub]
    except KeyError:
        st.balloons()
        st.markdown('<div class="glass-card"><h1>👑 סיימת את המשחק!</h1><p>ניצחת את כל 99 השלבים!</p></div>', unsafe_allow_html=True)
        st.stop()

    # בר התקדמות עליון (8 משימות)
    steps_names = ["מילים", "פיצוח", "דקדוק", "סיפור", "וידאו", "אמת/שקר", "משחקון", "בוס!"]
    progress_html = '<div class="progress-track">'
    for i, name in enumerate(steps_names):
        if i < user['sub_level']:
            progress_html += f'<span class="step-done">✅ {name}</span>'
        elif i == user['sub_level']:
            progress_html += f'<span class="step-active">👉 {name}</span>'
        else:
            progress_html += f'<span class="step-lock">🔒 {name}</span>'
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)

    # כותרת המשימה
    st.markdown(f'<div style="text-align:center; margin-bottom: 20px;"><h2 style="color:#f472b6 !important;">שלב {lvl} • {mission["title"]}</h2></div>', unsafe_allow_html=True)

    # אזור התוכן המרכזי
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # תצוגה מותאמת לפי סוג המשימה
        if mission["type"] == "story":
            st.markdown(f"<div style='background:rgba(0,0,0,0.3); padding:20px; border-radius:15px; border-right:5px solid #818cf8; font-size:22px; direction:ltr; text-align:left; margin-bottom:20px;'>📖 {mission['text']}</div>", unsafe_allow_html=True)
        
        elif mission["type"] == "video":
            st.video(mission["url"])
            
        elif mission["type"] == "scramble":
            st.markdown(f"<h1 style='letter-spacing: 15px; color:#34d399 !important;'>{' - '.join(random.sample(mission['a'], len(mission['a'])))}</h1>", unsafe_allow_html=True)
            st.markdown(f"**💡 רמז:** {mission.get('hint', '')}")

        st.markdown(f"<h3>{mission['q']}</h3>", unsafe_allow_html=True)
        
        # אזור התשובות
        if mission["type"] == "scramble":
            ans = st.text_input("הקלד את המילה הנכונה באנגלית:").strip().upper()
        else:
            ans = st.radio("בחר את התשובה שלך:", mission["options"], index=None, key=f"q_{lvl}_{sub}")

        st.markdown('</div>', unsafe_allow_html=True)

        # כפתור הגשה
        if st.button("בצע סריקה ⚡" if mission["type"] != "boss" else "הכה את הבוס! 💥"):
            if ans == mission["a"]:
                st.success("✅ ביצוע מושלם!")
                st.session_state.score += 20
                
                # טיפול בבוס ומתן פרס
                if mission["type"] == "boss":
                    st.balloons()
                    reward = mission.get("reward", f"💎 תיבת אוצר שלב {lvl}")
                    if "rewards" not in user: user["rewards"] = []
                    user["rewards"].append(reward)
                    st.success(f"🎉 ניצחת את הבוס! קיבלת: {reward}")
                    time.sleep(2)
                else:
                    time.sleep(1)
                
                # קידום השחקן
                user['sub_level'] += 1
                if user['sub_level'] > 7:
                    user['level'] += 1
                    user['sub_level'] = 0
                
                db[user['name']] = user
                save_json(DB_FILE, db)
                st.rerun()
            elif ans is not None and ans != "":
                st.error("❌ מערכות מתריעות על שגיאה. נסה שוב!")
