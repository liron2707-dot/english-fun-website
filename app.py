import streamlit as st
import json
import os
import time
import random
import streamlit.components.v1 as components

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v4.json"
CONTENT_FILE = "content_v4.json"

# --- CSS: יישור לימין (RTL), חריגת אנגלית (LTR) ופונטים ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }
    .en-text, div[role="radiogroup"] label {
        direction: ltr !important;
        text-align: left !important;
    }
    div[role="radiogroup"] label span {
        font-size: 28px !important; 
        font-weight: bold !important;
        padding: 8px 0;
    }
    .unseen-box {
        background-color: rgba(100, 116, 139, 0.15);
        border-left: 5px solid #6366f1;
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

# --- פונקציות עזר ---
def text_to_speech(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text.replace("'", "\\'").replace('"', '\\"')}');
    msg.lang = 'en-US';
    msg.rate = 0.85;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- טעינת נתונים ---
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# --- ניהול משתמש ---
if "user" not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    st.title("🌌 NEXUS ACADEMY - אנגלית חווייתית")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 שחקן חוזר")
        name = st.selectbox("בחר את השם שלך:", list(db.keys()) if db else ["אין משתמשים"])
        if st.button("התחבר 🚀", use_container_width=True):
            if name in db:
                st.session_state.user = db[name]
                st.rerun()
    with col2:
        st.subheader("✨ שחקן חדש")
        new_name = st.text_input("שם משתמש חדש:")
        new_age = st.number_input("בן כמה אתה?", 7, 15, 12)
        if st.button("צור משתמש והתחל 🎮", use_container_width=True):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.rerun()

else:
    user = st.session_state.user
    with st.sidebar:
        st.header(f"🕵️‍♂️ {user['name']}")
        st.write(f"**שלב נוכחי:** {user['level']} מתוך 99")
        st.progress(user['level'] / 99)
        if st.button("התנתק 🚪", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    # טעינה מהקובץ החיצוני
    try:
        mission = content[age_group][lvl][sub]
    except KeyError:
        st.error("השלב טרם נוצר או שגיאה בטעינת הקובץ. וודא ש-content_v4.json מעודכן.")
        st.stop()

    st.subheader(f"שלב {lvl} • משימה {int(sub)+1} מתוך 8")
    st.progress((int(sub)) / 8.0)
    
    st.markdown(f"<h2 class='en-text'>{mission['q']}</h2>", unsafe_allow_html=True)

    if "image_url" in mission and mission["image_url"]:
        st.image(mission["image_url"], width=300)

    if "video_url" in mission and mission["video_url"]:
        st.video(mission["video_url"])

    if "unseen" in mission:
        st.markdown(f'<div class="unseen-box"><strong>📖 Reading:</strong><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        if st.button("🔊 הקרא קטע"): text_to_speech(mission["unseen"])

    ans = st.radio("בחר תשובה:", mission["options"], index=None, key=f"q_{lvl}_{sub}")

    if st.button("בצע בדיקה ✔️", type="primary", use_container_width=True):
        if ans == mission["a"]:
            st.success("✅ נכון מאוד!")
            time.sleep(1)
            user['sub_level'] += 1
            if user['sub_level'] > 7:
                user['level'] += 1
                user['sub_level'] = 0
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
        else:
            st.error("❌ לא מדויק, נסה שוב!")
