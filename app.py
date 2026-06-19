import streamlit as st
import json
import os
import time
import random

# --- הגדרות דף בסיסיות ומורחבות ---
st.set_page_config(page_title="Nexus English Academy V10", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v10.json"
CONTENT_FILE = "content_v10.json"

# --- הזרקת עיצוב CSS יציב, מנוגד וברור לילדים ובני נוער ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Heebo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8fafc;
    }
    
    /* כרטיסיית משימה מרכזית */
    .cyber-card {
        background-color: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        padding: 30px !important;
        border-radius: 15px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.1) !important;
    }
    
    .cyber-title { color: #1e3a8a !important; font-size: 26px !important; font-weight: 900 !important; margin-bottom: 15px; }
    .cyber-text { color: #1e293b !important; font-size: 22px !important; font-weight: bold !important; line-height: 1.6; }
    
    /* תיבת קטע קריאה (Unseen) */
    .english-unseen-box {
        background-color: #f1f5f9 !important;
        border-left: 6px solid #3b82f6 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        font-size: 22px !important;
        color: #0f172a !important;
        direction: ltr !important;
        text-align: left !important;
        margin: 20px 0 !important;
        line-height: 1.6;
    }
    
    /* עיצוב כפתורי הרדיו של התשובות */
    div[role="radiogroup"] label span {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #1e293b !important;
    }
    
    div[role="radiogroup"] {
        direction: rtl !important;
        text-align: right !important;
        background: #f8fafc;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- פונקציות ניהול קבצים ומאגרי מידע ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- מנוע פדגוגי מתקדם לייצור 50 שלבים עם שאלות אמיתיות ורמזים ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מאגר סרטונים חינוכיים איכותיים
    videos = [
        "https://www.youtube.com/watch?v=tRNy2i75tCc", # צבעים
        "https://www.youtube.com/watch?v=75p-N9YKqNo"  # חיות
    ]
    
    # מאגרי מידע עשירים ומובנים ללא מילים שבורות
    raw_data = {
        "7-9": {
            "vocab": [("Dog", "כלב", "חיה מבויתת שנובחת"), ("Cat", "חתול", "חיה קטנה שמיללת ומגרגרת"), ("Apple", "תפוח", "פרי עגול וטעים שיכול להיות אדום או ירוק"), ("Milk", "חלב", "משקה לבן ומזין שמגיע מהפרה"), ("Sun", "שמש", "הכוכב הגדול בשמיים שמביא לנו אור וחום")],
            "unseens": [
                {"text": "Toby is a small brown dog. He loves to run in the big green park and play with his favorite red ball.", "q": "What is Toby's favorite toy?", "a": "A red ball", "options": ["A red ball", "A green bone", "A blue cat", "A yellow car"], "hint": "חפשו בטקסט את המשפט שמדבר על מה הוא אוהב לשחק איתו (play with...)"}
            ],
            "scrambles": [("G O D", "Dog", "חבר על ארבע שנובח"), ("T A C", "Cat", "אוהבת לשתות חלב ומגרגרת"), ("N U S", "Sun", "נמצאת בשמיים ביום ומחממת אותנו")]
        },
        "10-12": {
            "vocab": [("Football", "כדורגל", "ענף ספורט פופולרי שבו בועטים בכדור לשער"), ("Breakfast", "ארוחת בוקר", "הארוחה החשובה ביותר שאוכלים כשמתעוררים"), ("School", "בית ספר", "המקום אליו הולכים בכל בוקר כדי ללמוד ולפגוש חברים"), ("Beautiful", "יפה", "מילה שמתארת משהו שנראה טוב ונעים לעין")],
            "unseens": [
                {"text": "Mia and Liam love playing Minecraft. Yesterday, they built a giant castle with high stone walls to protect themselves from creepers.", "q": "Why did they build high stone walls?", "a": "To protect from creepers", "options": ["To protect from creepers", "To hide from their friends", "To make a kitchen", "To catch fish"], "hint": "קראו את סוף המשפט השני, המילה protect פירושה להגן."}
            ],
            "scrambles": [("O S C H O L", "School", "המקום שבו יש מורים, כיתות ולוח"), ("F I R E N D", "Friend", "אדם קרוב שאוהבים לבלות איתו ולסמוך עליו")]
        },
        "13-15": {
            "vocab": [("Opportunity", "הזדמנות", "סיטואציה שמאפשרת לנו להשיג או לעשות משהו חדש"), ("Challenge", "אתגר", "משימה קשה שדורשת מאמץ אך עוזרת לנו להשתפר"), ("Succeed", "להצליח", "להשיג את המטרה שקבענו לעצמנו לאחר עבודה קשה")],
            "unseens": [
                {"text": "Many teenagers dream of becoming digital content creators. While it looks easy, it actually requires hours of video editing, strategic planning, and consistent dedication.", "q": "What does being a content creator actually require?", "a": "Hours of editing and planning", "options": ["Hours of editing and planning", "Only a smartphone", "No effort at all", "Just walking in the park"], "hint": "חפשו את המילה requires (דורש) בטקסט וראו מה מופיע מיד אחריה."}
            ],
            "scrambles": [("S U C C E S S", "Success", "התוצאה שמגיעים אליה אחרי שלא מוותרים"), ("L A N G U A G E", "Language", "כלי תקשורת שבאמצעותו מדברים וכותבים, כמו אנגלית")]
        }
    }

    # בניית 50 שלבים מלאים עם 8 משימות מגוונות לכל גיל
    for age, data in raw_data.items():
        for level in range(1, 51):
            db[age][str(level)] = {}
            for sub in range(8):
                task = {}
                if sub == 0:
                    word, heb, hint = random.choice(data["vocab"])
                    task = {"title": "אוצר מילים: תרגום מאנגלית", "q": f"מהו הפירוש המדויק של המילה: '{word}'?", "a": heb, "options": [heb, "פירוש לא נכון א'", "פירוש לא נכון ב'", "פירוש לא נכון ג'"], "hint": hint}
                elif sub == 1:
                    word, heb, hint = random.choice(data["vocab"])
                    task = {"title": "אוצר מילים: תרגום לאנגלית", "q": f"כיצד נכתוב באנגלית את המילה: '{heb}'?", "a": word, "options": [word, "Table", "Computer", "Window"], "hint": f"המילה מתחילה באות {word[0]}"}
                elif sub == 2:
                    if age == "7-9":
                        task = {"title": "דקדוק בסיסי", "q": "השלם את המשפט: She ____ a good pupil.", "a": "is", "options": ["is", "am", "are", "be"], "hint": "עבור יחיד (He/She/It) נשתמש בפועל העזר המשפחתי הקצר ביותר."}
                    else:
                        task = {"title": "דקדוק וזמנים", "q": "השלם את המשפט: They ____ football in the park yesterday.", "a": "played", "options": ["played", "play", "playing", "plays"], "hint": "המילה yesterday מסמנת שהאירוע קרה בעבר (נוסיף ed)."}
                elif sub == 3:
                    u = random.choice(data["unseens"])
                    task = {"title": "הבנת הנקרא (Unseen)", "unseen": u["text"], "q": u["q"], "a": u["a"], "options": u["options"], "hint": u["hint"]}
                elif sub == 4:
                    scrambled, correct, hint = random.choice(data["scrambles"])
                    task = {"title": "🎮 משחקון: פיצוח אותיות מבולבלות", "q": f"סדרו את האותיות הבאות ליצירת מילה תקינה: [ {scrambled} ]", "a": correct, "options": [correct, "Book", "Game", "House"], "hint": hint}
                elif sub == 5:
                    task = {"title": "🎬 משימת סרטון והקשבה", "video_url": random.choice(videos), "q": "האם הסרטון המוצג מיועד לתרגול ולימוד השפה האנגלית?", "a": "כן, בהחלט", "options": ["כן, בהחלט", "לא, זה סרטון בצרפתית"], "hint": "הקשיבו למילים המושמעות בסרטון."}
                elif sub == 6:
                    if age == "7-9":
                        task = {"title": "יוצא דופן (Odd One Out)", "q": "איזו מילה יוצאת דופן ואינה שייכת למשפחת ה'חיות'?", "a": "Banana", "options": ["Dog", "Cat", "Banana", "Bird"], "hint": "שלוש אפשרויות הן בעלי חיים, ואחת היא משהו שאוכלים."}
                    elif age == "10-12":
                        task = {"title": "יוצא דופן (Odd One Out)", "q": "איזו מילה יוצאת דופן ואינה שייכת ל'מקצועות לימוד'?", "a": "Pizza", "options": ["Math", "Science", "Pizza", "History"], "hint": "חפשו את המאכל הטעים שאינו שיעור בכיתה."}
                    else:
                        task = {"title": "יוצא דופן (Odd One Out)", "q": "איזו מילה יוצאת דופן ואינה מתארת קושי או מאמץ?", "a": "Easy", "options": ["Challenge", "Difficult", "Hard", "Easy"], "hint": "שלוש מילים מתארות משהו קשוח ומאתגר, ומילה אחת מתארת משהו פשוט וקליל."}
                elif sub == 7:
                    task = {"title": "⚔️ משימת הבוס הגדול של השלב!", "q": f"הגעת למשימה ה-8 והאחרונה בשלב {level}! האם אתה מוכן להשלים את השלב ולשמור את ההתקדמות?", "a": "כן! בוא ננצח את הבוס!", "options": ["כן! בוא ננצח את הבוס!", "לא, אני רוצה לחזור אחר כך"], "hint": "לחץ על האפשרות הראשונה כדי להעפיל לשלב הבא בגאווה!"}
                
                # ערבוב תשובות מבוקר ובטוח
                opts = list(set(task["options"]))
                if len(opts) < 4 and sub not in [5, 7]: opts += ["אפשרות הגנה 1", "אפשרות הגנה 2"]
                random.shuffle(opts)
                task["options"] = opts[:4] if sub not in [5, 7] else task["options"]
                db[age][str(level)][str(sub)] = task
                
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- טעינת נתונים קיימים ---
users_db = load_json(DB_FILE)
content_db = load_json(CONTENT_FILE)

if "user" not in st.session_state: st.session_state.user = None
if "screen" not in st.session_state: st.session_state.screen = "login"
if "hint_clicked" not in st.session_state: st.session_state.hint_clicked = False

# ==========================================
# מסך 1: מסך כניסה ורישום שחקנים
# ==========================================
if st.session_state.screen == "login":
    st.title("🌌 NEXUS ENGLISH ACADEMY - V10")
    st.write("ברוכים הבאים למערכת המורחבת ללימוד אנגלית. היכנסו לחשבון או צרו שחקן חדש:")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 כניסת שחקן קיים")
        existing_name = st.selectbox("בחר את השם שלך מהרשימה:", list(users_db.keys()) if users_db else ["אין עדיין שחקנים רשומים"])
        if st.button("התחבר והמשך מהנקודה שעצרת 🚀", use_container_width=True):
            if existing_name in users_db:
                st.session_state.user = users_db[existing_name]
                st.session_state.screen = "game"
                st.session_state.hint_clicked = False
                st.rerun()
                
    with col2:
        st.subheader("✨ יצירת פרופיל שחקן חדש")
        new_name = st.text_input("הכנס שם מלא או כינוי:")
        new_age = st.number_input("בן כמה אתה? (גילאי 7 עד 15)", 7, 15, 11)
        if st.button("פתח משתמש חדש והתחל מאפס 🎮", use_container_width=True):
            if new_name and new_name not in users_db:
                # קביעת קבוצת הגיל הפדגוגית
                if new_age <= 9: group = "7-9"
                elif new_age <= 12: group = "10-12"
                else: group = "13-15"
                
                users_db[new_name] = {"name": new_name, "age": new_age, "group": group, "level": 1, "sub_level": 0, "rewards": [], "score": 0}
                save_json(DB_FILE, users_db)
                st.session_state.user = users_db[new_name]
                st.session_state.screen = "game"
                st.session_state.hint_clicked = False
                st.rerun()
            elif new_name in users_db:
                st.error("השם הזה כבר תפוס במערכת! בחר שם אחר או התחבר משמאל.")

# ==========================================
# מסך 2: מסך אבן דרך חגיגי וקבלת פרס (כל 10 שלבים)
# ==========================================
elif st.session_state.screen == "milestone":
    user = st.session_state.user
    st.balloons()
    
    st.markdown("<div style='text-align: center; padding: 30px;'>", unsafe_allow_html=True)
    st.title("🏆 הישג אגדי! עליתם ב-10 שלבים! 🏆")
    
    completed_stage = user['level'] - 1
    prize = f"גביע זהב עתידני - דרגת {completed_stage} שלבים 🌟"
    
    st.markdown(f"<h2>כל הכבוד {user['name']}! הפגנת התמדה מטורפת באנגלית!</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#eff6ff; color:#1e40af; padding:25px; border-radius:15px; font-size:26px; font-weight:bold; border:2px solid #3b82f6; margin:25px 0;'>🎁 הפרס שנוסף לכספת שלך: {prize}</div>", unsafe_allow_html=True)
    
    if st.button("אסוף את הפרס לארון והמשך לשלב הבא ➡️", type="primary", use_container_width=True):
        if prize not in user["rewards"]:
            user["rewards"].append(prize)
        users_db[user['name']] = user
        save_json(DB_FILE, users_db)
        st.session_state.screen = "game"
        st.session_state.hint_clicked = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# מסך 3: לוח המשחק והלמידה המרכזי העשיר
# ==========================================
elif st.session_state.screen == "game" and st.session_state.user is not None:
    user = st.session_state.user
    
    # --- סיידבר ניהול, התקדמות וארון גביעים מלא ---
    with st.sidebar:
        st.markdown(f"## 🕵️‍♂️ פרופיל: {user['name']}")
        st.write(f"**קבוצת לימוד:** גילאי {user['group']}")
        st.write(f"**ניקוד מצטבר:** {user.get('score', 0)} 🏆")
        st.write(f"**שלב נוכחי:** {user['level']} / 50")
        st.progress(user['level'] / 50)
        
        st.markdown("---")
        st.markdown("### 🎒 כספת ארון הפרסים שלך")
        if not user.get('rewards'):
            st.info("ארון הפרסים ריק כרגע. הגיעו לשלב 10 כדי לפתוח את הגביע הראשון שלכם!")
        else:
            for r in user['rewards']:
                st.success(f"⭐ {r}")
                
        st.markdown("---")
        # כפתור הורדת קובץ ה-JSON לבקשתך
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            json_data_to_download = f.read()
        st.download_button(
            label="📥 הורד קובץ שאלות JSON מלא",
            data=json_data_to_download,
            file_name="english_academy_content.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("---")
        if st.button("התנתק וחזור למסך הבית 🚪", use_container_width=True):
            st.session_state.user = None
            st.session_state.screen = "login"
            st.rerun()

    # שליפת המשימה הספציפית מתוך ה-JSON הפדגוגי הנכון
    lvl_str = str(user['level'])
    sub_str = str(user['sub_level'])
    age_group = user['group']
    
    mission = content_db.get(age_group, {}).get(lvl_str, {}).get(sub_str, {})
    
    if not mission:
        st.balloons()
        st.success("👑 מדהים! השלמתם את כל 50 השלבים באפליקציה בהצלחה ענקית!")
        st.stop()

    # --- כותרות עליונות ומחוון התקדמות בתוך השלב הנוכחי ---
    st.title(f"📍 שלב: {lvl_str} מתוך 50")
    st.subheader(f"🎯 משימה פנימית: {int(sub_str)+1} מתוך 8")
    st.progress((int(sub_str)) / 8.0)
    st.markdown("---")

    # כרטיסיית המשימה המרכזית בעיצוב נקי וברור
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="cyber-title">סוג המשימה: {mission.get("title", "משימה")}</div>', unsafe_allow_html=True)
    
    # במידה ויש קטע קריאה (Unseen)
    if "unseen" in mission:
        st.markdown(f'<div class="english-unseen-box"><strong>📖 Read the story:</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        
    # במידה ויש סרטון מובנה
    if "video_url" in mission:
        st.video(mission["video_url"])
        st.markdown("<p style='color:#3b82f6; font-weight:bold;'>צפו בסרטון הלימודי שלמעלה וענו על השאלה:</p>", unsafe_allow_html=True)

    # הצגת השאלה האמיתית והמובנת
    st.markdown(f'<div class="cyber-text">👉 {mission.get("q", "שאלה חסרה")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # הצגת אפשרויות הבחירה (התשובות האמריקאיות)
    options = mission.get("options", ["A", "B", "C", "D"])
    ans = st.radio("בחר את התשובה הנכונה:", options, index=None, key=f"radio_v10_{lvl_str}_{sub_str}")

    # --- מנגנון הרמזים החדש שהתבקש ---
    col_hint, col_space = st.columns([1, 3])
    with col_hint:
        if st.button("💡 קבל רמז לעזרה", use_container_width=True):
            st.session_state.hint_clicked = True
            
    if st.session_state.hint_clicked:
        st.info(f"🔍 **רמז פדגוגי:** {mission.get('hint', 'חשוב לקרוא את השאלה ואת האפשרויות בעיון.')}")

    st.markdown("---")

    # כפתור אישור ובדיקת התשובה
    if st.button("אשר תשובה והמשך קדימה ⚡", type="primary", use_container_width=True):
        if ans is None:
            st.warning("בבקשה בחר אפשרות אחת לפני שתלחץ על כפתור האישור!")
        elif ans == mission.get("a"):
            st.success("✅ מדהים! תשובה נכונה בהחלט. כל הכבוד! מרוויחים 10 נקודות.")
            time.sleep(1)
            
            # עדכון המצב והניקוד של המשתמש
            user['sub_level'] += 1
            user['score'] = user.get('score', 0) + 10
            
            # אם הוא סיים 8 משימות, הוא עולה שלב
            if user['sub_level'] > 7:
                user['level'] += 1
                user['sub_level'] = 0
                
                # בדיקה האם הגיע לאבן דרך של 10 שלבים (למשל אחרי שלב 10, 20, 30...)
                if (user['level'] - 1) % 10 == 0:
                    st.session_state.screen = "milestone"
            
            # שמירה לקובץ ה-JSON
            users_db[user['name']] = user
            save_json(DB_FILE, users_db)
            st.session_state.hint_clicked = False
            st.rerun()
        else:
            st.error("❌ התשובה אינה נכונה. קראו שוב את השאלה או השתמשו ברמז ונסו שנית!")
