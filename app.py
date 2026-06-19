import streamlit as st
import json
import os
import time
import random

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v6.json"
CONTENT_FILE = "content_v6.json"

# --- עיצוב עתידני, אנימציות ניאון וסולמות ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    /* רקע גלקסיה עתידני / סייברפאנק */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 70%, #020617 100%) !important;
        color: #e2e8f0;
        font-family: 'Heebo', sans-serif !important;
        direction: rtl !important;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-left: 1px solid #38bdf8;
    }

    h1, h2, h3, h4, p { text-align: right !important; direction: rtl !important; }
    
    h1 { color: #38bdf8 !important; text-shadow: 0 0 15px rgba(56, 189, 248, 0.6); font-weight: 900 !important;}
    h2 { color: #c084fc !important; font-size: 2.5rem !important; text-shadow: 0 0 10px rgba(192, 132, 252, 0.5); }
    
    /* כרטיסיית תוכן מרכזית - Glassmorphism */
    .glass-panel {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(56, 189, 248, 0.05);
        margin-bottom: 30px;
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    /* תיבת אנסין מהממת */
    .hologram-box {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(139, 92, 246, 0.1));
        border-right: 4px solid #38bdf8;
        border-left: 1px solid rgba(56, 189, 248, 0.2);
        padding: 25px;
        border-radius: 12px;
        font-size: 20px !important;
        direction: ltr !important;
        text-align: left !important;
        color: #f8fafc;
        text-shadow: 0 0 2px rgba(255,255,255,0.2);
        margin-bottom: 25px;
    }

    /* כפתורי רדיו (תשובות) בעיצוב עתידני */
    div[role="radiogroup"] > div {
        background: rgba(2, 6, 23, 0.7) !important;
        padding: 15px 25px !important;
        border-radius: 12px !important;
        border: 2px solid #334155 !important;
        transition: all 0.3s ease !important;
        margin-bottom: 12px !important;
    }
    div[role="radiogroup"] > div:hover {
        border-color: #c084fc !important;
        box-shadow: 0 0 15px rgba(192, 132, 252, 0.4) !important;
        transform: scale(1.02);
    }
    div[role="radiogroup"] label span {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #f8fafc !important;
    }

    /* עיצוב כפתור ענק וזוהר */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.5) !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.8) !important;
        transform: translateY(-2px);
    }

    /* --- סולם משימות (Task Ladder) --- */
    .ladder-container {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(15, 23, 42, 0.8); padding: 15px 30px;
        border-radius: 50px; border: 1px solid #334155; margin-bottom: 20px;
        position: relative;
    }
    .ladder-container::before {
        content: ''; position: absolute; top: 50%; left: 30px; right: 30px;
        height: 4px; background: #334155; z-index: 1; transform: translateY(-50%);
    }
    .ladder-step {
        width: 40px; height: 40px; border-radius: 50%; z-index: 2;
        display: flex; justify-content: center; align-items: center;
        font-weight: bold; font-size: 18px; color: #fff;
        background: #1e293b; border: 3px solid #334155; transition: 0.3s;
    }
    .step-completed {
        background: #10b981; border-color: #34d399;
        box-shadow: 0 0 15px #10b981;
    }
    .step-active {
        background: #38bdf8; border-color: #bae6fd;
        box-shadow: 0 0 20px #38bdf8; transform: scale(1.2);
    }
    
    /* --- סולם שלבים גלובלי (Level Ladder) בתפריט הצד --- */
    .level-tracker {
        background: linear-gradient(180deg, #1e1b4b, #0f172a);
        padding: 20px; border-radius: 15px; border: 1px solid #6366f1;
        text-align: center; margin-bottom: 20px;
    }
    .level-tracker-text { font-size: 2rem; color: #38bdf8; font-weight: 900; text-shadow: 0 0 10px #38bdf8;}
    </style>
""", unsafe_allow_html=True)

# --- פונקציות תשתית ומסד נתונים ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- מנוע ייצור התוכן החכם (מייצר את ה-JSON) ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    themes = {
        "7-9": {
            "vocab": [("Space", "חלל"), ("Robot", "רובוט"), ("Star", "כוכב"), ("Jump", "לקפוץ"), ("Game", "משחק")],
            "unseens": [{"text": "The small robot jumps on the bright star. It is playing a fun space game.", "q": "Where does the robot jump?", "a": "On the star", "options": ["On the star", "In the water", "On the bed", "In the car"]}],
            "vids": [("https://www.youtube.com/watch?v=1vQO4O_P7-s", "What planet is shown?", "Mars", ["Mars", "Earth", "Jupiter", "Sun"])]
        },
        "10-12": {
            "vocab": [("Collector", "אספן"), ("Rare", "נדיר"), ("Courtyard", "חצר"), ("Tradition", "מסורת"), ("Combination", "שילוב")],
            "unseens": [
                {"text": "In Italy, children used to play a traditional courtyard game called Ruzzola. In Poland, they played Palant. These games were passed down through generations before digital screens existed.", "q": "What is the name of the traditional game from Poland?", "a": "Palant", "options": ["Palant", "Ruzzola", "Match Attax", "Chess"]},
                {"text": "Finding a holographic card for your Match Attax collection requires patience. When you find the ultimate striker, your team becomes unbeatable.", "q": "What does finding a holographic card require?", "a": "Patience", "options": ["Patience", "Speed", "Money", "Anger"]}
            ],
            "vids": [("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Listen carefully: What is the main message?", "Never give up", ["Never give up", "Stop trying", "Go home", "Play games"])]
        },
        "13-15": {
            "vocab": [("Mitochondria", "מיטוכונדריה"), ("Nucleus", "גרעין התא"), ("Hierarchy", "היררכיה"), ("Organelle", "אברון"), ("Structure", "מבנה")],
            "unseens": [
                {"text": "The biological hierarchy describes how living things are organized. Atoms form molecules, molecules form organelles like mitochondria or ribosomes, and these make up the cells.", "q": "According to the text, what do molecules form?", "a": "Organelles", "options": ["Organelles", "Organisms", "Biospheres", "Planets"]},
                {"text": "The nucleus acts as the control center of the cell, storing genetic information, while the mitochondria generate the necessary ATP energy for the cell to function.", "q": "Which organelle generates energy?", "a": "Mitochondria", "options": ["Mitochondria", "Nucleus", "Ribosome", "Cell Wall"]}
            ],
            "vids": [("https://www.youtube.com/watch?v=8IlzKzbA_BI", "What is the function of the cell membrane?", "Protection", ["Protection", "Energy", "Digestion", "None"])]
        }
    }

    for age_group in db.keys():
        t = themes[age_group]
        for level in range(1, 51):
            db[age_group][str(level)] = {}
            for sub in range(8):
                task = {}
                v_word, v_heb = random.choice(t["vocab"])
                
                # הבטחה שכל משימה מקבלת את המפתח 'title' כדי למנוע את ה-KeyError שלך
                if sub == 0: task = {"title": "מפענח אוצר מילים", "q": f"מה הפירוש המדויק של המילה '{v_word}'?", "a": v_heb, "options": [v_heb, "משהו אחר", "שגוי", "הפוך"]}
                elif sub == 1: task = {"title": "קידוד לאחור", "q": f"איך כותבים באנגלית '{v_heb}'?", "a": v_word, "options": [v_word, "System", "Error", "Data"]}
                elif sub == 2: task = {"title": "אלגוריתם דקדוק", "q": "The data ____ processing right now.", "a": "is", "options": ["is", "are", "am", "be"]}
                elif sub == 3: 
                    u = random.choice(t["unseens"])
                    task = {"title": "סריקת נתונים (Unseen)", "unseen": u["text"], "q": u["q"], "a": u["a"], "options": u["options"]}
                elif sub == 4: 
                    vid = random.choice(t["vids"])
                    task = {"title": "ניתוח וידאו 🎬", "video_url": vid[0], "q": vid[1], "a": vid[2], "options": vid[3]}
                elif sub == 5: task = {"title": "זיהוי תבניות", "q": f"איזו מילה אינה קשורה ל-'{v_word}'?", "a": "תפוח", "options": ["תפוח", "מבנה", "מערכת", "בסיס"]}
                elif sub == 6: task = {"title": "סימולטור משפטים", "q": f"Complete: The {v_word} is highly advanced.", "a": v_word, "options": [v_word, "Dog", "Table", "Car"]}
                elif sub == 7: task = {"title": "קרב בוס שלב ⚔️", "q": f"סיום שלב {level}! מוכן להמשיך?", "a": "כן", "options": ["כן", "לא", "אולי", "אף פעם"]}

                random.shuffle(task["options"])
                db[age_group][str(level)][str(sub)] = task
                
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- טעינת נתונים ---
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

if "user" not in st.session_state: st.session_state.user = None
if "screen" not in st.session_state: st.session_state.screen = "login"

# ==========================================
# מסך 1: מסוף התחברות
# ==========================================
if st.session_state.screen == "login" and st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>🌌 NEXUS PROTOCOL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:24px; color:#94a3b8;'>התחבר למערכת למידת האנגלית העתידנית</p>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-panel"><h3>🔑 התחברות קיימת</h3>', unsafe_allow_html=True)
        name = st.selectbox("בחר מזהה משתמש:", list(db.keys()) if db else ["אין משתמשים"])
        if st.button("הפעל מערכת 🚀", use_container_width=True, key="login_btn"):
            if name in db:
                st.session_state.user = db[name]
                st.session_state.screen = "game"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col2:
        st.markdown('<div class="glass-panel"><h3>✨ משתמש חדש</h3>', unsafe_allow_html=True)
        new_name = st.text_input("הזן כינוי חדש:")
        new_age = st.number_input("גיל (מערכת תתאים את הקושי):", 7, 100, 12)
        if st.button("צור חיבור 🎮", use_container_width=True, key="register_btn"):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.session_state.screen = "game"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# מסך 2: מסך פרס (Milestone)
# ==========================================
elif st.session_state.screen == "milestone":
    user = st.session_state.user
    st.balloons()
    st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#fcd34d !important; font-size:4rem !important;'>🏆 LEVEL UP!</h1>", unsafe_allow_html=True)
    
    completed = user['level'] - 1
    reward = f"קריסטל ניאון שלב {completed} 💎"
    
    st.markdown(f"<h2>פצחת את המערכת! סיימת {completed} שלבים!</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:rgba(252, 211, 77, 0.2); border:2px solid #fcd34d; padding:30px; border-radius:15px; font-size:30px; margin:30px 0;'>🎁 בונוס הוענק: {reward}</div>", unsafe_allow_html=True)
    
    if st.button("קבל פרס והמשך ➡️", use_container_width=True):
        if reward not in user["rewards"]: user["rewards"].append(reward)
        db[user['name']] = user
        save_json(DB_FILE, db)
        st.session_state.screen = "game"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# מסך 3: ממשק המשימה (המשחק)
# ==========================================
elif st.session_state.screen == "game" and st.session_state.user is not None:
    user = st.session_state.user
    
    # תפריט צד (Sidebar)
    with st.sidebar:
        st.markdown(f"<h2 style='color:#38bdf8 !important;'>אלוף: {user['name']}</h2>", unsafe_allow_html=True)
        
        # סולם שלבים מותאם אישית ויפה
        st.markdown('<div class="level-tracker">', unsafe_allow_html=True)
        st.markdown("<div>שלב נוכחי מתוך 50</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='level-tracker-text'>{user['level']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<h3>🎒 כספת פרסים</h3>", unsafe_allow_html=True)
        if not user.get('rewards'): st.info("הכספת ריקה. השלם 10 שלבים!")
        else:
            for r in user['rewards']: st.markdown(f"<div style='color:#fcd34d; font-size:18px;'>⭐ {r}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        # כפתור הורדת קובץ ה-JSON שמבוקש
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            json_data = f.read()
        st.download_button("📥 הורד קובץ שאלות (JSON)", data=json_data, file_name="nexus_database.json", mime="application/json", use_container_width=True)
        
        st.markdown("---")
        if st.button("ניתוק מערכת 🚪", use_container_width=True):
            st.session_state.user = None
            st.session_state.screen = "login"
            st.rerun()

    # שליפת השאלה הנוכחית בבטחה
    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl, sub = str(user['level']), str(user['sub_level'])
    mission = content[age_group].get(lvl, {}).get(sub, {})
    if not mission: st.error("המשחק הסתיים או אירעה שגיאה.") ; st.stop()

    # --- יצירת סולם המשימות האופקי היפה (1 עד 8) ---
    steps_html = '<div class="ladder-container">'
    for i in range(8):
        if i < user['sub_level']:
            steps_html += f'<div class="ladder-step step-completed">✔</div>'
        elif i == user['sub_level']:
            steps_html += f'<div class="ladder-step step-active">{i+1}</div>'
        else:
            steps_html += f'<div class="ladder-step">{i+1}</div>'
    steps_html += '</div>'
    st.markdown(steps_html, unsafe_allow_html=True)

    # אזור התוכן המרכזי העתידני
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    # שימוש ב-get כדי להגן משגיאת KeyError בעתיד
    title = mission.get("title", "משימה מסווגת")
    st.markdown(f"<h3>🎯 משימה נוכחית: {title}</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(56, 189, 248, 0.2);'>", unsafe_allow_html=True)
    
    if "unseen" in mission:
        st.markdown(f'<div class="hologram-box"><strong>📡 שדר נכנס (קרא היטב):</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        
    if "video_url" in mission:
        st.video(mission["video_url"])
        st.markdown("<p style='color:#94a3b8;'>נתח את הווידאו כדי לענות על השאלה.</p>", unsafe_allow_html=True)

    q = mission.get("q", "שאלה חסרה?")
    st.markdown(f"<p style='font-size:26px; color:#38bdf8; font-weight:bold; margin-bottom:20px;'>{q}</p>", unsafe_allow_html=True)
    
    opts = mission.get("options", ["A", "B", "C", "D"])
    ans = st.radio("בחר את התשובה הנכונה:", opts, index=None, key=f"q_{lvl}_{sub}", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("אימות נתונים ⚡", use_container_width=True):
        if ans == mission.get("a"):
            st.success("✅ אימות עבר בהצלחה!")
            time.sleep(0.8)
            user['sub_level'] += 1
            if user['sub_level'] > 7:
                user['level'] += 1
                user['sub_level'] = 0
                if (user['level'] - 1) % 10 == 0:
                    st.session_state.screen = "milestone"
            
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
        elif ans is not None:
            st.error("❌ התשובה שגויה. נסה שוב לחשב מסלול מחדש.")
