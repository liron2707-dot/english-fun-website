import streamlit as st
import json
import os
import time
import random

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English Adventure", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")

# שינינו ל-V3 כדי להכריח את המערכת לייצר את התוכן החדש והמותאם
DB_FILE = "users_db_v3.json"
CONTENT_FILE = "content_v3.json"

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

# --- מנוע יצירת תוכן מותאם גיל (המפעל) ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return

    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מאגרי מילים מותאמים גיל
    vocab = {
        "7-9": [("Dog", "כלב"), ("Red", "אדום"), ("Apple", "תפוח"), ("Happy", "שמח"), ("Boy", "ילד"), ("Sun", "שמש"), ("Water", "מים")],
        "10-12": [("Beautiful", "יפה"), ("Quickly", "במהירות"), ("Friend", "חבר"), ("School", "בית ספר"), ("Always", "תמיד"), ("Country", "מדינה")],
        "13-15": [("Environment", "סביבה"), ("Successful", "מוצלח"), ("Opportunity", "הזדמנות"), ("Although", "למרות ש"), ("Development", "התפתחות")]
    }

    for age_group in db.keys():
        for level in range(1, 100):
            db[age_group][str(level)] = {}
            
            for sub in range(8):
                # בחירת מילה אקראית מותאמת גיל
                word, hebrew = random.choice(vocab[age_group])
                
                # כל המשימות עכשיו הן שאלות אמריקאיות בלבד
                if sub == 0:
                    task = {"title": "אוצר מילים 1", "q": f"איך אומרים '{hebrew}' באנגלית?", "a": word, "options": [word, "Cat", "House", "Tree"]}
                elif sub == 1:
                    task = {"title": "אוצר מילים 2", "q": f"מה הפירוש של המילה '{word}'?", "a": hebrew, "options": [hebrew, "חתול", "שולחן", "שמיים"]}
                elif sub == 2:
                    if age_group == "7-9":
                        task = {"title": "דקדוק בסיסי", "q": "I ____ a student.", "a": "am", "options": ["am", "is", "are", "be"]}
                    elif age_group == "10-12":
                        task = {"title": "דקדוק עבר", "q": "Yesterday, I ____ to the park.", "a": "went", "options": ["go", "went", "going", "goes"]}
                    else:
                        task = {"title": "דקדוק מתקדם", "q": "If it rains, we ____ at home.", "a": "will stay", "options": ["will stay", "stayed", "staying", "stays"]}
                elif sub == 3:
                    task = {"title": "השלמת משפט", "q": f"The {word.lower()} is very nice.", "a": word, "options": [word, "Car", "Pencil", "Book"]}
                elif sub == 4:
                    task = {"title": "אמת או שקר", "q": "The sun is cold. (True or False?)", "a": "False", "options": ["True", "False"]}
                elif sub == 5:
                    task = {"title": "יוצא דופן", "q": "איזו מילה יוצאת דופן?", "a": "Apple", "options": ["Dog", "Cat", "Lion", "Apple"]}
                elif sub == 6:
                    task = {"title": "הפכים", "q": "מה ההפך מ-Big (גדול)?", "a": "Small", "options": ["Small", "Tall", "Fast", "Hot"]}
                elif sub == 7:
                    task = {"title": "אתגר השלב! ⚔️", "q": f"איזו מילה מסכמת את שלב {level}?", "a": word, "options": [word, "Nothing", "Wrong", "Mistake"]}
                
                # ערבוב התשובות כדי שהתשובה הנכונה לא תהיה תמיד הראשונה
                random.shuffle(task["options"])
                task["type"] = "mcq" # Multiple Choice Question
                db[age_group][str(level)][str(sub)] = task

    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- CSS מעודכן לקריאות מקסימלית ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Heebo', sans-serif; direction: rtl;
        background-color: #0f172a; color: #ffffff; /* רקע כהה וטקסט לבן בוהק */
    }
    
    /* כרטיסיות בולטות וקריאות */
    .glass-card { 
        background: rgba(30, 41, 59, 0.95); /* כמעט שחור אטום */
        padding: 40px; border-radius: 20px; border: 2px solid #6366f1;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4); text-align: center; margin-bottom: 20px;
    }
    
    /* הגדלת פונטים משמעותית */
    h1 { color: #a5b4fc !important; font-size: 4rem !important; font-weight: 900;}
    h2 { color: #f472b6 !important; font-size: 3rem !important; }
    h3 { color: #ffffff !important; font-size: 2.2rem !important; margin-bottom: 30px !important;}
    p, span { font-size: 1.5rem; color: #f8fafc; }
    
    /* הגדלת כפתורי הרדיו (התשובות) */
    .stRadio>div { direction: rtl; background: rgba(0,0,0,0.5); padding: 25px; border-radius: 15px; border: 1px solid #4f46e5;}
    .stRadio label { font-size: 1.8rem !important; color: #ffffff !important; font-weight: bold; cursor: pointer; }
    
    /* כפתור אישור ענק */
    .stButton>button { 
        background: linear-gradient(90deg, #4f46e5, #ec4899) !important; color: white !important;
        font-size: 26px !important; font-weight: 900 !important; border-radius: 16px !important;
        padding: 20px 40px !important; border: none !important; width: 100%; 
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* סרגל התקדמות מובן */
    .progress-track {
        display: flex; justify-content: space-between; background: rgba(0,0,0,0.8);
        padding: 20px; border-radius: 20px; margin-bottom: 30px; font-weight: bold; font-size: 1.2rem;
    }
    .step-done { color: #34d399; }
    .step-active { color: #f472b6; font-size: 1.5rem; text-decoration: underline;}
    .step-lock { color: #64748b; }
    </style>
""", unsafe_allow_html=True)

# --- לוגיקה ---
if "user" not in st.session_state: st.session_state.user = None

db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# ==========================================
# מסך התחברות
# ==========================================
if st.session_state.user is None:
    st.markdown('<div class="glass-card"><h1>🌌 NEXUS ACADEMY</h1><p style="font-size:30px;">האקדמיה הדיגיטלית ללימוד אנגלית</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔑 שחקן חוזר")
        name = st.selectbox("בחר שם:", list(db.keys()) if db else ["אין משתמשים"])
        if st.button("היכנס 🚀"):
            if name in db:
                st.session_state.user = db[name]
                st.rerun()
                
    with col2:
        st.markdown("### ✨ שחקן חדש")
        new_name = st.text_input("הכנס שם חדש:")
        new_age = st.number_input("בחר גיל:", 7, 15, 12)
        if st.button("התחל משחק 🎮"):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.rerun()
            elif new_name in db:
                st.error("השם תפוס!")

# ==========================================
# מסך המשחק הראשי
# ==========================================
else:
    user = st.session_state.user
    
    # תפריט צד - פרסים בלבד
    with st.sidebar:
        st.markdown(f"<h2>{user['name']} 🕵️‍♂️</h2>", unsafe_allow_html=True)
        st.write(f"**רמה {user['level']} מתוך 99** (גיל: {user['age']})")
        st.progress(user['level'] / 99)
        
        st.markdown("---")
        st.markdown("### 🎒 ארון הפרסים (כל 10 שלבים):")
        if not user.get('rewards'):
            st.write("תקבל פרס אגדי כשתסיים את שלב 10!")
        for r in user.get('rewards', []):
            st.markdown(f"<div style='background:#1e293b; padding:15px; border-radius:10px; margin-bottom:10px; font-size:18px;'>🎁 {r}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("התנתק 🚪"):
            st.session_state.user = None
            st.rerun()

    # קביעת קבוצת גיל
    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    try:
        mission = content[age_group][lvl][sub]
    except KeyError:
        st.error("שגיאה בטעינת השלב.")
        st.stop()

    # בר התקדמות 8 משימות
    steps_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
    progress_html = '<div class="progress-track">'
    for i, name in enumerate(steps_names):
        if i < user['sub_level']: progress_html += f'<span class="step-done">✔ משימה {name}</span>'
        elif i == user['sub_level']: progress_html += f'<span class="step-active">🎯 משימה {name}</span>'
        else: progress_html += f'<span class="step-lock">🔒 משימה {name}</span>'
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)

    # אזור השאלה
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"<h2>שלב {lvl} • {mission['title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>{mission['q']}</h3>", unsafe_allow_html=True)
        
        ans = st.radio("בחר את התשובה הנכונה:", mission["options"], index=None, key=f"q_{lvl}_{sub}")
        st.markdown('</div>', unsafe_allow_html=True)

        # בדיקת התשובה
        if st.button("בצע סריקה ⚡"):
            if ans == mission["a"]:
                st.success("✅ מעולה! תשובה נכונה.")
                time.sleep(1)
                
                # קידום השחקן
                user['sub_level'] += 1
                
                # האם סיים את השלב (עשה 8 משימות)?
                if user['sub_level'] > 7:
                    # האם זה שלב עגול של 10? (פרס!)
                    if user['level'] % 10 == 0:
                        st.balloons()
                        reward = f"תיבת אוצר מטורפת של שלב {user['level']}!"
                        if "rewards" not in user: user["rewards"] = []
                        user["rewards"].append(reward)
                        st.success(f"🎉 ענק! השלמת 10 שלבים וקיבלת: {reward}")
                        time.sleep(3)
                        
                    user['level'] += 1
                    user['sub_level'] = 0
                    
                    # האם סיים את המשחק (עבר את שלב 99)? עליית גיל
                    if user['level'] > 99:
                        st.balloons()
                        if user['age'] <= 9: user['age'] = 11 # מקפיץ לגיל 10-12
                        elif user['age'] <= 12: user['age'] = 14 # מקפיץ לגיל 13-15
                        st.success("👑 סיימת את כל 99 השלבים! עלית לקבוצת הגיל הבאה!")
                        user['level'] = 1
                        time.sleep(4)

                db[user['name']] = user
                save_json(DB_FILE, db)
                st.rerun()
            elif ans is not None:
                st.error("❌ לא מדויק, נסה שוב!")
