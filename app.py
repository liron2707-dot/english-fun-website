import streamlit as st
import json
import os
import time
import random

# --- הגדרות מערכת ומבנה עמוד ---
st.set_page_config(page_title="Nexus English Adventure", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v5.json"
CONTENT_FILE = "content_v5.json"

# --- הזרקת CSS מקיף ליישור לימין, התאמה למסך ופונטים ענקיים ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    /* הגדרות בסיס - הכל מימין לשמאל */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Heebo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* הגדלת פונטים של שאלות וכותרות */
    h1, h2, h3, h4 {
        text-align: right !important;
        direction: rtl !important;
    }
    h2 { font-size: 2.8rem !important; font-weight: 900 !important; color: #4f46e5 !important; }
    h3 { font-size: 2.2rem !important; font-weight: 700 !important; margin-top: 20px !important; }
    
    /* הגדלת הפונט של התשובות האמריקאיות (כפתורי הרדיו) */
    div[role="radiogroup"] label span {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #1e293b !important;
    }
    
    /* התאמת כפתורי הרדיו שיראו כמו כרטיסים ברורים */
    div[role="radiogroup"] > div {
        background-color: #f8fafc !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        margin-bottom: 10px !important;
    }
    
    /* קופסת תוכן מרכזית מוגדלת */
    .content-box {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 20px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    
    /* תיבת אנסין מותאמת */
    .unseen-box {
        background-color: #f1f5f9;
        border-right: 6px solid #4f46e5;
        padding: 25px;
        border-radius: 12px;
        font-size: 22px !important;
        direction: ltr !important;
        text-align: left !important;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    
    /* יישור טקסט עזר של Streamlit לימין */
    .stMarkdown, .stCaption, p {
        text-align: right !important;
        font-size: 1.3rem !important;
    }
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

# --- מנוע חכם לייצור 1,200 שאלות ותוכן איכותי מותאם גיל (50 שלבים) ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מאגרי נתונים איכותיים לבניית השאלות
    themes = {
        "7-9": {
            "vocab": [("Dog", "כלב"), ("Cat", "חתול"), ("Red", "אדום"), ("Green", "ירוק"), ("Apple", "תפוח"), ("Water", "מים"), ("Sun", "שמש"), ("Big", "גדול"), ("Small", "קטן")],
            "unseens": [
                {"text": "The small dog is under the big green tree. It is drinking water because it is hot today.", "q": "Why is the dog drinking water?", "a": "Because it is hot", "options": ["Because it is hot", "Because it is sad", "Because it wants to sleep", "Because it is green"]},
                {"text": "Lisa has three red apples in her school bag. She gives one apple to her best friend Ben.", "q": "How many apples does Lisa give to Ben?", "a": "One apple", "options": ["One apple", "Three apples", "Two apples", "No apples"]}
            ],
            "vids": [("https://www.youtube.com/watch?v=75p-N9YKqNo", "What animal family is shown in the video?", "Lions", ["Lions", "Sharks", "Bears", "Eagles"])]
        },
        "10-12": {
            "vocab": [("Teamwork", "עבודת צוות"), ("Match", "משחק/התאמה"), ("Legendary", "אגדי"), ("Card", "קלף"), ("Strategy", "אסטרטגיה"), ("Victory", "ניצחון"), ("Challenge", "אתגר")],
            "unseens": [
                {"text": "Dan is a master collector of Match Attax cards. He recently discovered an ultra-rare card that creates a legendary combo with his forward players, guaranteeing a victory in the school tournament.", "q": "What did Dan recently discover?", "a": "An ultra-rare card", "options": ["An ultra-rare card", "A new stadium", "A lost football", "A book about strategy"]},
                {"text": "During the school talent show, the judges explained that proper teamwork is much more valuable than individual skills. The group that collaborated best won the golden trophy.", "q": "What did the judges say is more valuable than individual skills?", "a": "Teamwork", "options": ["Teamwork", "Singing loudly", "Expensive shoes", "Practicing alone"]}
            ],
            "vids": [("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "According to the song's famous chorus, what will he 'never' do?", "Give you up", ["Give you up", "Let you play", "Say hello", "Go away"])]
        },
        "13-15": {
            "vocab": [("Environment", "סביבה"), ("Development", "התפתחות"), ("Structure", "מבנה"), ("Organism", "אורגניזם/יצור חי"), ("Function", "תפקיד/תפקוד"), ("Component", "רכיב")],
            "unseens": [
                {"text": "In biological sciences, the cellular hierarchy dictates that cells form tissues, tissues form organs, and organs form a complex organism. Inside each cell, specialized structures called organelles handle vital functions.", "q": "What structure inside a cell handles vital functions?", "a": "Organelles", "options": ["Organelles", "Tissues", "Organs", "Organisms"]},
                {"text": "Environmental development relies heavily on understanding ecological balance. Although industrialization brings economic growth, it often poses a severe threat to natural habitats.", "q": "What threatens natural habitats according to the text?", "a": "Industrialization", "options": ["Industrialization", "Ecological balance", "Economic growth", "Cellular hierarchy"]}
            ],
            "vids": [("https://www.youtube.com/watch?v=8IlzKzbA_BI", "What cellular powerhouse structure is responsible for creating ATP energy?", "Mitochondria", ["Mitochondria", "Ribosomes", "Nucleus", "Cell Wall"])]
        }
    }

    # לולאת בנייה ל-50 שלבים
    for age_group in db.keys():
        t = themes[age_group]
        for level in range(1, 51):
            db[age_group][str(level)] = {}
            for sub in range(8):
                task = {}
                v_word, v_heb = random.choice(t["vocab"])
                
                if sub == 0:
                    task = {"title": "אוצר מילים בסיסי", "q": f"מה הפירוש המדויק של המילה '{v_word}'?", "a": v_heb, "options": [v_heb, "משהו אחר", "לא נכון", "הפוך"]}
                elif sub == 1:
                    task = {"title": "תרגום הפוך", "q": f"איך כותבים באנגלית את המילה '{v_heb}'?", "a": v_word, "options": [v_word, "Window", "Object", "System"]}
                elif sub == 2:
                    # דקדוק מותאם רמה
                    if age_group == "7-9": task = {"title": "דקדוק וזמנים", "q": "The cat ____ sleeping on the sofa right now.", "a": "is", "options": ["is", "are", "am", "be"]}
                    elif age_group == "10-12": task = {"title": "דקדוק וזמנים", "q": "Last week, we ____ a legendary football match.", "a": "played", "options": ["played", "play", "playing", "plays"]}
                    else: task = {"title": "דקדוק וזמנים", "q": "If scientists alter the cell structure, the organism ____ adapt.", "a": "will", "options": ["will", "would have", "did", "was"]}
                elif sub == 3:
                    # משימת הבנת הנקרא (Unseen) קשורה ישירות לשאלה
                    u = random.choice(t["unseens"])
                    task = {"title": "הבנת הנקרא (Unseen)", "unseen": u["text"], "q": u["q"], "a": u["a"], "options": u["options"]}
                elif sub == 4:
                    # משימת וידאו אינטראקטיבית - הסרטון קשור לחלוטין לשאלה
                    vid = random.choice(t["vids"])
                    task = {"title": "משימת וידאו אינטראקטיבית 🎬", "video_url": vid[0], "q": vid[1], "a": vid[2], "options": vid[3]}
                elif sub == 5:
                    task = {"title": "משימת אודיו והגייה 🎧", "q": f"כיצד נהגה נכון את המילה '{v_word}' בהקשר קולי משפט?", "a": f"בצורה מודגשת", "options": [f"בצורה מודגשת", "בצורה שקטה", "בלי להגות אותה", "כמו מילה אחרת"]}
                elif sub == 6:
                    task = {"title": "משחקון לוגיקה והקשר", "q": f"איזו מילה משלימה את ההקשר הטוב ביותר למילה: '{v_word}'?", "a": "הקשר תקין", "options": ["הקשר תקין", "טעות מוחלטת", "רעש מפריע", "ניתוק"]}
                elif sub == 7:
                    task = {"title": "קרב בוס השלב! ⚔️", "q": f"הגעת לסוף שלב {level}. האם אתה מוכן להוכיח שליטה ברמת הגיל שלך?", "a": "כן, קדימה לניצחון!", "options": ["כן, קדימה לניצחון!", "לא", "אולי", "אני רוצה לפרוש"]}

                # ערבוב אופציות התשובה
                random.shuffle(task["options"])
                db[age_group][str(level)][str(sub)] = task
                
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- טעינת נתונים ומצבי מערכת ---
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

if "user" not in st.session_state: st.session_state.user = None
if "screen" not in st.session_state: st.session_state.screen = "login" # מסכים: login, game, milestone

# ==========================================
# מסך 1: התחברות והרשמה
# ==========================================
if st.session_state.screen == "login" and st.session_state.user is None:
    st.title("🌌 NEXUS ENGLISH ADVENTURE")
    st.write("ברוכים הבאים לאקדמיית האנגלית הדיגיטלית. אנא התחבר או צור שחקן חדש.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 כניסת שחקן קיים")
        name = st.selectbox("בחר את השם שלך:", list(db.keys()) if db else ["אין שחקנים רשומים"])
        if st.button("היכנס למשחק 🚀", use_container_width=True):
            if name in db:
                st.session_state.user = db[name]
                st.session_state.screen = "game"
                st.rerun()
                
    with col2:
        st.subheader("✨ יצירת שחקן חדש")
        new_name = st.text_input("שם השחקן החדש (באנגלית או עברית):")
        new_age = st.number_input("בן כמה אתה? (מותאם לגילאי 7-15)", 7, 15, 12)
        if st.button("צור שחקן והתחל 🎮", use_container_width=True):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.session_state.screen = "game"
                st.rerun()
            elif new_name in db:
                st.error("השם הזה כבר תפוס במערכת!")

# ==========================================
# מסך 2: מסך הפרס החגיגי (מופיע כל 10 שלבים)
# ==========================================
elif st.session_state.screen == "milestone":
    user = st.session_state.user
    st.balloons()
    st.markdown("<div style='text-align:center; padding:5px;'>", unsafe_allow_html=True)
    st.title("🏆 הישג אגדי חסר תקדים! 🏆")
    
    # חישוב איזה ציון דרך הושג
    completed_milestone = user['level'] - 1
    reward_name = f"גביע הזהב האקלוסיבי של דרג {completed_milestone} 🌟"
    
    st.markdown(f"<h2>כל הכבוד {user['name']}! השלמת בהצלחה רצף של {completed_milestone} שלבים!</h2>", unsafe_allow_html=True)
    st.write("המערכת זיהתה את ההשקעה שלך ומעניקה לך פרס על-חלל שנשמר בארון הפרסים האישי שלך.")
    
    st.markdown(f"<div style='background-color:#fef08a; padding:30px; border-radius:15px; font-size:26px; font-weight:bold; color:#a16207; border:3px dashed #ca8a04; margin:20px 0;'>🎁 קיבלת: {reward_name}</div>", unsafe_allow_html=True)
    
    if st.button("אסוף פרס והמשך לשלב הבא ➡️", type="primary", use_container_width=True):
        # הוספת הפרס באופן סופי לארון
        if reward_name not in user["rewards"]:
            user["rewards"].append(reward_name)
        db[user['name']] = user
        save_json(DB_FILE, db)
        
        # החזרה למסך המשחק הראשי
        st.session_state.screen = "game"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# מסך 3: מסך המשחק הראשי (נפרד לכל שלב ומשימה)
# ==========================================
elif st.session_state.screen == "game" and st.session_state.user is not None:
    user = st.session_state.user
    
    # תפריט צד (Sidebar) מעוצב, ברור וקריא
    with st.sidebar:
        st.header(f"🕵️‍♂️ שחקן: {user['name']}")
        st.write(f"**קבוצת גיל:** {user['age']} שנים")
        st.write(f"**שלב נוכחי:** {user['level']} מתוך 50")
        st.progress(user['level'] / 50)
        
        st.markdown("---")
        st.subheader("🎒 ארון הפרסים האגדיים")
        if not user.get('rewards'):
            st.info("ארון הפרסים ריק. השלם 10 שלבים לקבלת הפרס הראשון!")
        else:
            for r in user['rewards']:
                st.markdown(f"⭐ **{r}**")
                
        st.markdown("---")
        # כפתור ייצוא קובץ JSON חיצוני לבקשת המשתמש
        st.subheader("⚙️ ניהול תוכן חיצוני")
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            json_bytes = f.read()
        st.download_button(
            label="📥 הורד קובץ שאלות JSON מלא",
            data=json_bytes,
            file_name="nexus_questions_database.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("---")
        if st.button("התנתק מהמשחק 🚪", use_container_width=True):
            st.session_state.user = None
            st.session_state.screen = "login"
            st.rerun()

    # קביעת קבוצת הגיל לצורך שליפת השאלות הנכונות
    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    # הגנה מפני חריגת שלבים
    try:
        mission = content[age_group][lvl][sub]
    except KeyError:
        st.success("👑 מדהים! השלמת את כל 50 השלבים במשחק!")
        if st.button("התחל מחדש ברמת גיל גבוהה יותר"):
            user['level'] = 1
            user['sub_level'] = 0
            user['age'] += 3
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
        st.stop()

    # כותרת שלב ייחודית ומד התקדמות פנימי לשלב (1 עד 8)
    st.markdown(f"<h2>שלב {lvl} מתוך 50 • קושי גיל {age_group}</h2>", unsafe_allow_html=True)
    st.write(f"**משימה נוכחית בשלב זה:** {int(sub)+1} מתוך 8 משימות חובה")
    st.progress((int(sub)) / 8.0)
    st.markdown("---")

    # קופסת התוכן המרכזית (המסך הייעודי של השלב)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown(f"<h3>🎯 {mission['title']}</h3>", unsafe_allow_html=True)
    
    # תצוגת קטע קריאה (Unseen) אם קיים במשימה
    if "unseen" in mission:
        st.markdown(f'<div class="unseen-box"><strong>📖 Read the text carefully:</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        
    # תצוגת וידאו מותאם ומחובר לשאלה אם קיים במשימה
    if "video_url" in mission:
        st.video(mission["video_url"])
        st.caption("צפו בקטע המדיה שלמעלה ולאחר מכן ענו על השאלה הבאה:")

    # הצגת השאלה הברורה
    st.markdown(f"<p style='font-size:22px; font-weight:bold; color:#0f172a;'>👉 {mission['q']}</p>", unsafe_allow_html=True)
    
    # בחירת התשובה (רדיו עם פונט מוגדל ועיצוב כרטיס)
    ans = st.radio("בחר את התשובה הנכונה מבין האפשרויות:", mission["options"], index=None, key=f"active_q_{lvl}_{sub}")
    st.markdown('</div>', unsafe_allow_html=True)

    # כפתור אישור ובדיקת תשובה
    if st.button("אשר תשובה ובצע סריקה ⚡", type="primary", use_container_width=True):
        if ans == mission["a"]:
            st.success("✅ תשובה נכונה! כל הכבוד.")
            time.sleep(0.8)
            
            # קידום התקדמות פנימית
            user['sub_level'] += 1
            
            # בדיקה האם סיים את כל 8 המשימות ועובר שלב
            if user['sub_level'] > 7:
                user['level'] += 1
                user['sub_level'] = 0
                
                # האם השלב החדש שהוא הגיע אליו מעיד על כך שהוא הרגע סיים שלב עגול (למשל סיים את 10, עכשיו הוא ב-11)?
                if (user['level'] - 1) % 10 == 0:
                    st.session_state.screen = "milestone" # מעבר למסך הפרס הנפרד
            
            # שמירה מיידית של המצב והשלב שבו הוא נמצא
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
            
        elif ans is not None:
            st.error("❌ התשובה אינה מדויקת. קרא את השאלה שוב ונסה שנית!")
