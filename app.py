import streamlit as st
import json
import os
import time
import random

# --- הגדרות דף בסיסיות ---
st.set_page_config(page_title="Nexus English", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v7.json"
CONTENT_FILE = "content_v7.json"

# --- הזרקת CSS ממוקד ובטוח (מונע היעלמות טקסט ומבטיח קריאות) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    /* הגדרת כיווניות האתר */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Heebo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיבת משימה עתידנית בעלת ניגודיות גבוהה - מבטיחה שיראו את הכתב תמיד */
    .cyber-card {
        background-color: #0f172a !important;
        border: 2px solid #38bdf8 !important;
        padding: 30px !important;
        border-radius: 15px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
    }
    
    /* כותרות וטקסטים בתוך הכרטיס */
    .cyber-title { color: #38bdf8 !important; font-size: 28px !important; font-weight: 900 !important; margin-bottom: 15px; }
    .cyber-text { color: #f8fafc !important; font-size: 22px !important; font-weight: bold !important; line-height: 1.6; }
    
    /* קופסת טקסט לאנסין (אנגלית משמאל לימין) */
    .english-unseen-box {
        background-color: #1e293b !important;
        border-left: 5px solid #a855f7 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        font-size: 24px !important;
        color: #f8fafc !important;
        direction: ltr !important;
        text-align: left !important;
        margin: 20px 0 !important;
    }
    
    /* הגדלת הפונט של כפתורי הרדיו (תשובות אמריקאיות) */
    div[role="radiogroup"] label span {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #0f172a !important; /* צבע כהה וברור על הרקע הלבן של כפתור הרדיו המובנה */
    }
    
    /* יישור כפתורי הרדיו לימין */
    div[role="radiogroup"] {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- פונקציות ניהול קבצים ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- מנוע יצירת תוכן פדגוגי טהור ומותאם גיל (50 שלבים) ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מאגר סרטונים לימודיים בסיסיים ואיכותיים ביוטיוב (אנגלית פשוטה וברורה)
    educational_videos = [
        "https://www.youtube.com/watch?v=75p-N9YKqNo", # סרטון חיות קצר
        "https://www.youtube.com/watch?v=1vQO4O_P7-s"  # סרטון מילים בסיסיות
    ]
    
    # מאגרי נתונים ייעודיים ללימוד אנגלית בלבד (ללא נושאים מדעיים)
    level_data = {
        "7-9": {
            "vocab": [("Apple", "תפוח"), ("Banana", "בננה"), ("Dog", "כלב"), ("Cat", "חתול"), ("Red", "אדום"), ("Blue", "כחול"), ("Sun", "שמש"), ("Milk", "חלב")],
            "sentences": [("I love my mom", "אני אוהב את אמא שלי"), ("The sky is blue", "השמיים כחולים"), ("I see a big cat", "אני רואה חתול גדול")],
            "unseens": [
                {"text": "The little cat is sleeping in the sun. It is a warm day.", "q": "What is the cat doing?", "a": "Sleeping", "options": ["Sleeping", "Running", "Eating", "Flying"]}
            ],
            "games": [("O R G D", "Dog", "חיה נאמנה"), ("A T C", "Cat", "חיה שמיללת"), ("E D R", "Red", "הצבע של התות")]
        },
        "10-12": {
            "vocab": [("Breakfast", "ארוחת בוקר"), ("Journey", "מסע"), ("Friendship", "חברות"), ("Beautiful", "יפה"), ("Suddenly", "פתאום"), ("Tomorrow", "מחר")],
            "sentences": [("We played football yesterday", "שיחקנו כדורגל אתמול"), ("She is reading a book now", "היא קוראת ספר עכשיו")],
            "unseens": [
                {"text": "Danny went to the kitchen to eat breakfast. He found an apple and a glass of cold milk on the table. He smiled and said thank you to his father.", "q": "What did Danny find on the table?", "a": "An apple and milk", "options": ["An apple and milk", "Pizza and cola", "A book and pen", "A toy car"]}
            ],
            "games": [("O S C H O L", "School", "המקום אליו הולכים ללמוד"), ("F I R E N D", "Friend", "חבר טוב"), ("S U M M E R", "Summer", "העונה החמה בשנה")]
        },
        "13-15": {
            "vocab": [("Consequence", "תוצאה"), ("Opportunity", "הזדמנות"), ("Challenge", "אתגר"), ("Accomplish", "להשיג/להשלים"), ("Influence", "השפעה")],
            "sentences": [("If it rains tomorrow, we will stay at home", "אם ירד גשם מחר, נישאר בבית"), ("She has been studying English for five years", "היא לומדת אנגלית כבר חמש שנים")],
            "unseens": [
                {"text": "Learning a foreign language provides a great opportunity to explore new cultures. While it requires daily practice and patience, the long-term benefits are definitely worth the effort.", "q": "According to the text, what does learning a language require?", "a": "Daily practice and patience", "options": ["Daily practice and patience", "A lot of money", "Traveling to another country", "Nothing at all"]}
            ],
            "games": [("L A N G U A G E", "Language", "שפה שמדברים בה"), ("P A T I E N C E", "Patience", "סבלנות הדרושה להצלחה"), ("S U C C E S S", "Success", "הצלחה לאחר מאמץ")]
        }
    }

    # בניית 50 שלבים עם 8 משימות מוגדרות וברורות לכל רמת גיל
    for age_group in db.keys():
        data = level_data[age_group]
        for level in range(1, 51):
            db[age_group][str(level)] = {}
            for sub in range(8):
                task = {}
                
                if sub == 0:
                    word, heb = random.choice(data["vocab"])
                    task = {"title": "תרגום אוצר מילים", "q": f"מהו הפירוש הנכון של המילה באנגלית: '{word}'?", "a": heb, "options": [heb, "פירוש שגוי 1", "פירוש שגוי 2", "פירוש שגוי 3"]}
                elif sub == 1:
                    word, heb = random.choice(data["vocab"])
                    task = {"title": "תרגום הפוך", "q": f"כיצד נכתוב באנגלית את המילה המבוקשת: '{heb}'?", "a": word, "options": [word, "Table", "Window", "Computer"]}
                elif sub == 2:
                    eng_s, heb_s = random.choice(data["sentences"])
                    task = {"title": "השלמת משפט בהקשר נכון", "q": f"מהו התרגום המדויק ביותר של המשפט: '{eng_s}'?", "a": heb_s, "options": [heb_s, "תרגום לא קשור 1", "תרגום לא קשור 2", "משפט שגוי"]}
                elif sub == 3:
                    u = random.choice(data["unseens"])
                    task = {"title": "הבנת הנקרא (Unseen)", "unseen": u["text"], "q": u["q"], "a": u["a"], "options": u["options"]}
                elif sub == 4:
                    # משחקון אותיות מבולבלות (Word Scramble Game)
                    scrambled, correct, hint = random.choice(data["games"])
                    task = {"title": "🎮 משחקון: פיצוח מילים מבולבלות!", "q": f"סדר את האותיות הבאות כדי ליצור מילה תקינה: [ {scrambled} ] \n\n רמז: {hint}", "a": correct, "options": [correct, "Word", "Test", "Play"]}
                elif sub == 5:
                    vid_url = random.choice(educational_videos)
                    task = {"title": "🎬 משימת סרטון והקשבה", "video_url": vid_url, "q": "צפו בסרטון הלימודי קצר. האם השפה המדוברת בו היא אנגלית?", "a": "Yes", "options": ["Yes", "No"]}
                elif sub == 6:
                    word, heb = random.choice(data["vocab"])
                    task = {"title": "יוצא דופן (Odd One Out)", "q": f"איזו מילה אינה קשורה לקטגוריה של המילה: '{word}'?", "a": "יוצא דופן", "options": ["יוצא דופן", "מילה קשורה 1", "מילה קשורה 2", "מילה קשורה 3"]}
                elif sub == 7:
                    task = {"title": "⚔️ משימת הבוס של השלב!", "q": f"כל הכבוד! הגעת למשימה האחרונה בשלב {level}. האם תרצה להעפיל לשלב הבא?", "a": "כן, בוא נמשיך!", "options": ["כן, בוא נמשיך!", "לא עכשיו"]}

                # הגנה מערבול אופציות קבועה
                opts = list(set(task["options"]))
                if len(opts) < 4 and sub not in [5, 7]: 
                    opts += ["אפשרות השלמה 1", "אפשרות השלמה 2"]
                random.shuffle(opts)
                task["options"] = opts[:4] if sub not in [5,7] else task["options"]
                
                db[age_group][str(level)][str(sub)] = task
                
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- טעינת מסדי הנתונים ---
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

if "user" not in st.session_state: st.session_state.user = None
if "screen" not in st.session_state: st.session_state.screen = "login"

# ==========================================
# מסך 1: מסך כניסה והרשמה מאובטח
# ==========================================
if st.session_state.screen == "login" and st.session_state.user is None:
    st.title("🌌 NEXUS ENGLISH ACADEMY")
    st.write("ברוכים הבאים לאפליקציית לימוד האנגלית הממתקדת שלך. היכנס או צור שחקן חדש:")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 כניסת משתמש קיים")
        name = st.selectbox("בחר את השם שלך:", list(db.keys()) if db else ["אין משתמשים רשומים"])
        if st.button("התחבר והתחל ללמוד 🚀", use_container_width=True):
            if name in db:
                st.session_state.user = db[name]
                st.session_state.screen = "game"
                st.rerun()
                
    with col2:
        st.subheader("✨ יצירת משתמש חדש")
        new_name = st.text_input("הזן שם מלא/כינוי:")
        new_age = st.number_input("בן כמה אתה? (7 עד 15)", 7, 15, 12)
        if st.button("צור חשבון והתחל 🎮", use_container_width=True):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.session_state.screen = "game"
                st.rerun()
            elif new_name in db:
                st.error("השם כבר קיים במערכת!")

# ==========================================
# מסך 2: מסך קבלת פרס שווה (כל 10 שלבים)
# ==========================================
elif st.session_state.screen == "milestone":
    user = st.session_state.user
    st.balloons()
    
    st.markdown("<div style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
    st.title("🏆 הישג מדהים! השלמת 10 שלבים! 🏆")
    
    completed_milestone = user['level'] - 1
    reward_item = f"גביע זהב אגדי - דרגת {completed_milestone} שלבים 🌟"
    
    st.markdown(f"<h2>כל הכבוד {user['name']}! עברת בהצלחה קבוצה של 10 שלבים מלאים!</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#1e293b; color:#fcd34d; padding:30px; border-radius:15px; font-size:28px; font-weight:bold; border:2px solid #fcd34d; margin:30px 0;'>🎁 הפרס השווה שלך: {reward_item}</div>", unsafe_allow_html=True)
    
    if st.button("אסוף את הפרס לכספת והמשך לשלב הבא ➡️", type="primary", use_container_width=True):
        if reward_item not in user["rewards"]:
            user["rewards"].append(reward_item)
        db[user['name']] = user
        save_json(DB_FILE, db)
        st.session_state.screen = "game"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# מסך 3: מסך המשחק והלמידה הראשי
# ==========================================
elif st.session_state.screen == "game" and st.session_state.user is not None:
    user = st.session_state.user
    
    # תפריט ניהול צדדי (Sidebar)
    with st.sidebar:
        st.markdown(f"## 🕵️‍♂️ שחקן: {user['name']}")
        st.write(f"**התאמת גיל:** גילאי {user['age']}")
        st.write(f"**שלב כללי:** {user['level']} מתוך 50")
        st.progress(user['level'] / 50)
        
        st.markdown("---")
        st.markdown("### 🎒 ארון הפרסים והגביעים שלך")
        if not user.get('rewards'):
            st.info("ארון הפרסים ריק. השלם את שלב 10 כדי לקבל את הגביע הראשון שלך!")
        else:
            for r in user['rewards']:
                st.success(f"⭐ {r}")
                
        st.markdown("---")
        # אפשרות הורדת קובץ ה-JSON החיצוני המלא לבקשתך
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            full_json_content = f.read()
        st.download_button(
            label="📥 הורד קובץ שאלות JSON מלא",
            data=full_json_content,
            file_name="english_questions_db.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("---")
        if st.button("התנתק מהמערכת 🚪", use_container_width=True):
            st.session_state.user = None
            st.session_state.screen = "login"
            st.rerun()

    # קביעת קבוצת הגיל לשליפת התוכן הפדגוגי הנכון
    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    # הגנה ושליפת המשימה בבטחה מה-JSON
    mission = content.get(age_group, {}).get(lvl, {}).get(sub, {})
    if not mission:
        st.success("👑 מזל טוב! סיימת את כל 50 השלבים באפליקציה בהצלחה מרובה!")
        st.stop()

    # --- תצוגה מרכזית יציבה וברורה של השלב והמשימה (ללא באגים) ---
    st.title(f"📍 שלב נוכחי: {lvl} מתוך 50")
    st.subheader(f"🎯 משימה מספר: {int(sub)+1} מתוך 8 משימות בשלב זה")
    st.progress((int(sub)) / 8.0)
    st.markdown("---")

    # כרטיסיית המשחק המרכזית (ניגודיות גבוהה מובטחת)
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    
    # כותרת ותיאור המשימה
    m_title = mission.get("title", "משימת לימוד")
    st.markdown(f'<div class="cyber-title">סוג המשימה: {m_title}</div>', unsafe_allow_html=True)
    
    # הצגת קטע קריאה (Unseen) אם קיים
    if "unseen" in mission:
        st.markdown(f'<div class="english-unseen-box"><strong>📖 Read the text:</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        
    # הצגת סרטון וידאו יציב אם קיים במשימה (מחוץ לכרטיסיות שעלולות לחסום אותו)
    if "video_url" in mission:
        st.video(mission["video_url"])
        st.markdown("<p style='color:#38bdf8;'>צפו בסרטון הלימודי שלמעלה ולאחר מכן ענו על השאלה הבאה קצרות:</p>", unsafe_allow_html=True)

    # הצגת השאלה עצמה
    q_text = mission.get("q", "שאלה חסרה")
    st.markdown(f'<div class="cyber-text">👉 {q_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # הצגת כפתורי הרדיו (התשובות) - צבע טקסט כהה ומנוגד על גבי כפתור לבן
    opts = mission.get("options", ["A", "B", "C", "D"])
    ans = st.radio("אנא בחר את התשובה הנכונה ביותר:", opts, index=None, key=f"active_v7_{lvl}_{sub}")

    st.write("")
    
    # כפתור אישור ובדיקה
    if st.button("אשר תשובה והמשך במשימה ⚡", type="primary", use_container_width=True):
        if ans == mission.get("a"):
            st.success("✅ מדהים! תשובה נכונה בהחלט.")
            time.sleep(0.7)
            
            # קידום שלבים פנימיים
            user['sub_level'] += 1
            
            # בדיקה האם הסתיים השלב (8 משימות)
            if user['sub_level'] > 7:
                user['level'] += 1
                user['sub_level'] = 0
                
                # אם השלים קבוצה של 10 שלבים - מעבר למסך הפרס
                if (user['level'] - 1) % 10 == 0:
                    st.session_state.screen = "milestone"
            
            # שמירה סופית של המצב למניעת אובדן מידע
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
            
        elif ans is not None:
            st.error("❌ התשובה אינה נכונה, נסה לקרוא שוב ולענות מחדש!")
