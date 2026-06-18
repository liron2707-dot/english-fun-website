import streamlit as st
import json
import os
import time
import random
import streamlit.components.v1 as components # נוסף עבור ההקראה

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v4.json"
CONTENT_FILE = "content_v4.json"

# --- CSS מעודכן: יישור לימין (RTL), חריגת אנגלית (LTR) ופונטים גדולים ---
st.markdown("""
    <style>
    /* הגדרה כללית לכל האפליקציה - יישור לימין */
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }
    
    /* החרגה: כל הטקסטים באנגלית יישארו משמאל לימין */
    .en-text, div[role="radiogroup"] label {
        direction: ltr !important;
        text-align: left !important;
    }

    /* הגדלת הטקסט של כפתורי הבחירה האמריקאית - ענק וברור */
    div[role="radiogroup"] label span {
        font-size: 28px !important; 
        font-weight: bold !important;
        padding: 8px 0;
    }

    /* עיצוב כרטיסיית האנסין (קטע קריאה) */
    .unseen-box {
        background-color: rgba(100, 116, 139, 0.15);
        border-left: 5px solid #6366f1; /* הקו עבר לשמאל כי האנגלית משמאל */
        padding: 20px;
        border-radius: 10px;
        font-size: 22px;
        direction: ltr;
        text-align: left;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- פונקציית הקראה (TTS) ---
def text_to_speech(text):
    # קוד JS פשוט שמפעיל את מקריא הטקסט המובנה בדפדפן במבטא אנגלי
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text.replace("'", "\\'").replace('"', '\\"')}');
    msg.lang = 'en-US';
    msg.rate = 0.85; // קצב קצת איטי כדי שיהיה מובן
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# --- פונקציות מסד נתונים ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- מנוע יצירת תוכן (דוגמאות לתשתית - המאגר האמיתי יגיע מהאוטומציה) ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    unseens_7_9 = [{"text": "Tom has a big red ball. He plays with it in the park. His dog likes the ball too.", "q": "Where does Tom play?", "a": "In the park", "options": ["In the park", "At school", "In the house", "In the pool"]}]
    unseens_10_12 = [{"text": "Mike bought a new Match Attax 2025 card.", "q": "What was Mike looking for?", "a": "A rare card", "options": ["A rare card", "A football", "A new friend", "A video game"]}]
    unseens_13_15 = [{"text": "In biology, understanding the hierarchy of living things is crucial.", "q": "What are complex organisms made of?", "a": "Trillions of cells", "options": ["Trillions of cells", "Only one cell", "Water and air", "Plants"]}]
    
    videos = ["https://www.youtube.com/watch?v=fN1Cyr0ZK9M", "https://www.youtube.com/watch?v=3yXpeBGEqD0"]

    for age_group in db.keys():
        for level in range(1, 100):
            db[age_group][str(level)] = {}
            for sub in range(8):
                task = {}
                if sub == 0:
                    # הוספתי דוגמה לאיך מכניסים תמונה לשאלה (image_url)
                    task = {"q": "What color is this?", "a": "Yellow", "options": ["Yellow", "Green", "Blue", "Red"], "image_url": "https://images.unsplash.com/photo-1588714477688-cfbc116719b6?w=400"}
                elif sub == 1:
                    task = {"q": "She ____ a good friend.", "a": "is", "options": ["is", "are", "am", "be"]}
                elif sub == 2:
                    if age_group == "7-9": u = random.choice(unseens_7_9)
                    elif age_group == "10-12": u = random.choice(unseens_10_12)
                    else: u = random.choice(unseens_13_15)
                    task = {"unseen": u["text"], "q": u["q"], "a": u["a"], "options": u["options"]}
                elif sub == 3:
                    task = {"video_url": random.choice(videos), "q": "Based on the video, what is correct?", "a": "Yes", "options": ["Yes", "No", "Maybe", "Never"]}
                elif sub == 4:
                    task = {"q": "Cats can fly. (True/False)", "a": "False", "options": ["True", "False"]}
                elif sub == 5:
                    task = {"q": "Find the odd one out:", "a": "Table", "options": ["Dog", "Cat", "Table", "Fish"]}
                elif sub == 6:
                    task = {"q": "I eat an ____ every day.", "a": "apple", "options": ["apple", "chair", "sun", "dog"]}
                elif sub == 7:
                    task = {"q": f"Boss level {level}! Choose Victory:", "a": "Victory", "options": ["Victory", "Defeat", "Loss", "Fail"]}

                random.shuffle(task["options"])
                db[age_group][str(level)][str(sub)] = task
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- ניהול משתמש ---
if "user" not in st.session_state: st.session_state.user = None
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# ==========================================
# מסך התחברות
# ==========================================
if st.session_state.user is None:
    st.title("🌌 NEXUS ACADEMY - אנגלית חווייתית")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 שחקן חוזר")
        name = st.selectbox("בחר את השם שלך מתוך הרשימה:", list(db.keys()) if db else ["אין משתמשים רשומים"])
        if st.button("התחבר והמשך 🚀", use_container_width=True):
            if name in db:
                st.session_state.user = db[name]
                st.rerun()
                
    with col2:
        st.subheader("✨ שחקן חדש")
        new_name = st.text_input("הכנס שם משתמש חדש:")
        new_age = st.number_input("בן כמה אתה?", 7, 15, 12)
        if st.button("צור משתמש והתחל 🎮", use_container_width=True):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.rerun()
            elif new_name in db:
                st.error("השם כבר תפוס! בחר שם אחר.")

# ==========================================
# מסך המשחק הראשי
# ==========================================
else:
    user = st.session_state.user
    
    with st.sidebar:
        st.header(f"🕵️‍♂️ {user['name']}")
        st.write(f"**גיל מוגדר:** {user['age']}")
        st.write(f"**שלב נוכחי:** {user['level']} מתוך 99")
        st.progress(user['level'] / 99)
        
        st.markdown("---")
        st.subheader("🎒 ארון הפרסים שלי")
        st.caption("מרוויחים פרס אגדי בכל 10 שלבים!")
        if not user.get('rewards'):
            st.info("עדיין אין פרסים. המשך לשחק!")
        else:
            for r in user['rewards']:
                st.success(f"🎁 {r}")
        
        st.markdown("---")
        if st.button("התנתק 🚪", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    try: mission = content[age_group][lvl][sub]
    except KeyError:
        st.error("שגיאה בטעינת השלב.")
        st.stop()

    st.subheader(f"שלב {lvl} • משימה {int(sub)+1} מתוך 8")
    progress_val = (int(sub)) / 8.0
    st.progress(progress_val)
    st.markdown("---")

    # הצגת השאלה בתוך מחלקת en-text כדי שתהיה משמאל לימין
    st.markdown(f"<h2 class='en-text'>{mission['q']}</h2>", unsafe_allow_html=True)
    st.write("") 
    
    # ---------------------------------------------
    # שינויים דינמיים לפי מה שיש ב-JSON:
    # ---------------------------------------------

    # 1. אם יש תמונה
    if "image_url" in mission and mission["image_url"]:
        st.image(mission["image_url"], width=300)

    # 2. אם יש וידאו
    if "video_url" in mission and mission["video_url"]:
        st.video(mission["video_url"])
        st.caption("צפה בווידאו ולאחר מכן ענה על השאלה.")

    # 3. אם יש קטע קריאה (Unseen) + הוספת כפתור הקראה
    if "unseen" in mission:
        st.markdown(f'<div class="unseen-box"><strong>📖 Reading Text:</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        if st.button("🔊 הקרא את קטע הקריאה בקול"):
            text_to_speech(mission["unseen"])

    # בחירת התשובה
    ans = st.radio("בחר את התשובה הנכונה:", mission["options"], index=None, key=f"q_{lvl}_{sub}")

    st.write("") 

    if st.button("בצע בדיקה ✔️", type="primary", use_container_width=True):
        if ans == mission["a"]:
            st.success("✅ מעולה! תשובה נכונה.")
            time.sleep(1)
            
            user['sub_level'] += 1
            
            if user['sub_level'] > 7:
                if user['level'] % 10 == 0:
                    st.balloons()
                    reward = f"גביע מיוחד של שלב {user['level']}! 🏆"
                    if "rewards" not in user: user["rewards"] = []
                    user["rewards"].append(reward)
                    st.success(f"🎉 כל הכבוד! השלמת 10 שלבים ברצף וזכית ב: {reward}")
                    time.sleep(3)
                    
                user['level'] += 1
                user['sub_level'] = 0
                
                if user['level'] > 99:
                    st.balloons()
                    if user['age'] <= 9: user['age'] = 11
                    elif user['age'] <= 12: user['age'] = 14
                    st.success("👑 מדהים! סיימת את כל 99 השלבים! עלית אוטומטית לקבוצת הגיל ולרמת הקושי הבאה!")
                    user['level'] = 1
                    time.sleep(4)

            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
            
        elif ans is not None:
            st.error("❌ התשובה לא מדויקת, נסה שוב!")
