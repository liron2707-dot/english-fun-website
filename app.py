import streamlit as st
import json
import os
import time
import random
import base64

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English 2.0", page_icon="🌌", layout="wide")

DB_FILE = "users_db_v5.json"
CONTENT_FILE = "content_v5.json"

# --- CSS משופר ליישור לימין, פונטים ענקיים ונגישות ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Rubik', sans-serif;
    }
    
    /* החרגת אנגלית מיישור לימין */
    .en-text, [data-testid="stMarkdownContainer"] p, div[role="radiogroup"] label {
        direction: ltr !important;
        text-align: left !important;
    }

    /* הגדלת פונטים של התשובות (רדיו) */
    div[role="radiogroup"] label span {
        font-size: 28px !important; /* פונט ענק */
        font-weight: 700 !important;
        color: #1e293b !important;
        padding: 10px;
    }
    
    /* עיצוב קופסת האנסין */
    .unseen-box {
        background-color: #f8fafc;
        border-left: 8px solid #6366f1;
        padding: 25px;
        border-radius: 15px;
        font-size: 24px;
        line-height: 1.6;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }

    /* כפתורי פעולה */
    .stButton button {
        font-size: 20px !important;
        padding: 10px 24px !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- פונקציית הקראת טקסט (TTS) באמצעות JavaScript ---
def text_to_speech(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text.replace("'", "\\'")}');
    msg.lang = 'en-US';
    msg.rate = 0.9;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- פונקציות מסד נתונים ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- מנוע תוכן משופר ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    
    # מאגר דוגמה רחב יותר (כדי להגיע ל-2400 שאלות, מומלץ להשתמש ב-JSON חיצוני שמיוצר ע"י AI)
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # נתונים לדוגמה עם תמונות וסרטונים רלוונטיים
    sample_data = {
        "7-9": [
            {"q": "What color is this apple?", "a": "Red", "options": ["Red", "Blue", "Green", "Yellow"], "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400", "type": "visual"},
            {"q": "How do you say 'שלום'?", "a": "Hello", "options": ["Hello", "Goodbye", "Thank you", "Please"], "video": "https://www.youtube.com/watch?v=fN1Cyr0ZK9M"}
        ],
        "10-12": [
            {"unseen": "The space station orbits Earth every 90 minutes. Astronauts see 16 sunrises a day!", "q": "How many sunrises do they see?", "a": "16", "options": ["16", "90", "1", "24"]},
            {"q": "They ____ to the park yesterday.", "a": "went", "options": ["went", "go", "going", "goes"], "type": "grammar"}
        ],
        "13-15": [
            {"unseen": "Environmental conservation is crucial for our survival. Reducing carbon footprints helps mitigate climate change effects.", "q": "What helps mitigate climate change?", "a": "Reducing carbon footprints", "options": ["Reducing carbon footprints", "Increasing pollution", "Ignoring nature", "Cutting trees"]}
        ]
    }

    for age_group in db.keys():
        for level in range(1, 100):
            db[age_group][str(level)] = {}
            for sub in range(8):
                # בבחירה אמיתית היינו שואבים מתוך מאגר של אלפי שאלות
                task = random.choice(sample_data[age_group]).copy()
                random.shuffle(task["options"])
                db[age_group][str(level)][str(sub)] = task
    
    save_json(CONTENT_FILE, db)

ensure_content_exists()
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# --- ניהול משתמש ---
if "user" not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    st.title("🌌 NEXUS ACADEMY")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 כניסה")
        name = st.selectbox("מי אתה?", list(db.keys()) if db else ["אין משתמשים"])
        if st.button("התחל לשחק 🚀") and name in db:
            st.session_state.user = db[name]
            st.rerun()
    with col2:
        st.subheader("✨ חדש כאן?")
        new_name = st.text_input("שם משתמש:")
        new_age = st.slider("גיל:", 7, 15, 10)
        if st.button("צור משתמש"):
            db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
            save_json(DB_FILE, db)
            st.session_state.user = db[new_name]
            st.rerun()
else:
    user = st.session_state.user
    age_group = "7-9" if user['age'] <= 9 else ("10-12" if user['age'] <= 12 else "13-15")
    mission = content[age_group][str(user['level'])][str(user['sub_level'])]

    # Sidebar
    st.sidebar.title(f"שלום, {user['name']} 👋")
    st.sidebar.metric("שלב", user['level'])
    st.sidebar.progress(user['level'] / 99)
    if st.sidebar.button("התנתק"):
        st.session_state.user = None
        st.rerun()

    # Main Game UI
    st.header(f"משימה {user['sub_level'] + 1} / 8")
    
    # הצגת שאלה (באנגלית)
    st.markdown(f"<h1 class='en-text'>{mission['q']}</h1>", unsafe_allow_html=True)

    # הצגת אנסין + כפתור הקראה
    if "unseen" in mission:
        st.markdown(f"<div class='unseen-box en-text'>{mission['unseen']}</div>", unsafe_allow_html=True)
        if st.button("🔊 הקרא קטע קריאה"):
            text_to_speech(mission['unseen'])

    # הצגת תמונה אם קיימת
    if "image" in mission:
        st.image(mission["image"], width=400)

    # הצגת וידאו אם קיים
    if "video" in mission:
        st.video(mission["video"])

    # תשובות
    ans = st.radio("בחר תשובה:", mission["options"], index=None, key=f"ans_{user['level']}_{user['sub_level']}")

    if st.button("בדיקה ✔️", type="primary"):
        if ans == mission["a"]:
            st.success("כל הכבוד! 🎉")
            user['sub_level'] += 1
            if user['sub_level'] > 7:
                user['level'] += 1
                user['sub_level'] = 0
                st.balloons()
            db[user['name']] = user
            save_json(DB_FILE, db)
            time.sleep(1)
            st.rerun()
        elif ans:
            st.error("לא נכון, נסה שוב 😕")

### מענה על השאלות שלך:
1.  **יישור לימין:** השתמשתי ב-CSS גלובלי שמיישר את כל האתר ל-RTL, והחרגתי ספציפית את ה-Markdowns וה-Radio buttons (האנגלית) ל-LTR.
2.  **פונטים גדולים:** הגדרתי פונט בגודל `28px` לתשובות ב-CSS. עכשיו הן ברורות מאוד.
3.  **שאלות חוזרות וסרטונים:** שיניתי את מבנה הנתונים. עכשיו לכל שאלה יכול להיות `video` או `image` משלה. כדי למנוע חזרתיות, עליך למלא את קובץ ה-JSON בתוכן רב.
4.  **הקראת אנסין:** הוספתי פונקציית JavaScript מובנית שמפעילה את ה-Text-to-Speech של הדפדפן בלחיצת כפתור.
5.  **שאלות מעניינות:** הוספתי תמיכה ב"שאלות חזותיות" (עם תמונות).
6.  **שאלות עם תמונות:** הוספתי שדה `image` במילון המשימה שמוצג אוטומטית אם הוא קיים.
7.  **ניהול 2,400 שאלות:** הדרך הנכונה היא **לא** לכתוב אותן בתוך הקוד. עליך ליצור קובץ `content.json` נפרד. אתה יכול להשתמש ב-ChatGPT כדי לייצר את הקובץ הזה (לבקש ממנו "צור לי קובץ JSON עם 100 שאלות באנגלית לרמה X"). הקוד שכתבתי יודע לקרוא את זה בצורה דינמית.

התוכנית שלך מוכנה לשדרוג! האם תרצה שאעזור לך לייצר מאגר שאלות ראשוני בפורמט ה-JSON החדש?
