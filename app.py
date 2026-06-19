import streamlit as st
import json
import os
import time
import random

# --- הגדרות דף בסיסיות ומורחבות ---
st.set_page_config(page_title="Nexus English Academy V11", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v11.json"
CONTENT_FILE = "content_v11.json"

# --- הזרקת עיצוב CSS יציב, מנוגד וברור לילדים ובני נוער ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght=400;700;900&display=swap');
    
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

# --- מנוע פדגוגי מתקדם לייצור 50 שלבים ללא סרטונים וללא אותיות מבולבלות ---
def ensure_content_exists():
    # במידה והקובץ כבר קיים, נמחק וניצור מחדש כדי לרענן את השאלות לפי הדרישות החדשות
    if os.path.exists(CONTENT_FILE):
        try: os.remove(CONTENT_FILE)
        except: pass

    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מאגר מידע עשיר ומובנה לכל קבוצת גיל לשם יצירת מסיחים אמיתיים
    raw_data = {
        "7-9": {
            "vocab": [
                ("Dog", "כלב", "חיה מבויתת שנובחת ומכשכשת בזנב"),
                ("Cat", "חתול", "חיה קטנה שמיללת ומגרגרת"),
                ("Apple", "תפוח", "פרי עגול וטעים שיכול להיות אדום או ירוק"),
                ("Milk", "חלב", "משקה לבן ומזין שמגיע מהפרה"),
                ("Sun", "שמש", "הכוכב הגדול בשמיים שמביא לנו אור וחום"),
                ("Book", "ספר", "דפים מחוברים יחד שקוראים בהם סיפורים"),
                ("School", "בית ספר", "המקום שאליו הולכים הילדים בבוקר ללמוד"),
                ("Happy", "שמח", "הרגשה טובה ומחויכת, ההפך מעצוב"),
                ("Water", "מים", "משקה שקוף וטבעי שחיוני לחיים"),
                ("Red", "אדום", "הצבע של עגבנייה בשלה או של תות שדה"),
                ("Green", "ירוק", "הצבע של הדשא בגינה או של מלפפון"),
                ("Banana", "בננה", "פרי צהוב וארוך שקופים אוהבים לאכול")
            ],
            "grammar": [
                {"q": "She ____ a very good pupil.", "a": "is", "opts": ["is", "am", "are", "be"], "hint": "עבור כינוי הגוף She (היא) נשתמש בפועל העזר הקצר והמתאים ליחיד."},
                {"q": "I ____ eating a sweet apple right now.", "a": "am", "opts": ["am", "is", "are", "have"], "hint": "כשמדברים בגוף ראשון על עצמי (I), פועל העזר בראש ההווה הוא תמיד am."},
                {"q": "The kids ____ playing in the big park.", "a": "are", "opts": ["are", "is", "am", "was"], "hint": "המילה Kids פירושה ילדים (רבים), לכן נבחר בפועל העזר לרבים."},
                {"q": "He has ____ old bicycle.", "a": "an", "opts": ["an", "a", "the", "some"], "hint": "לפני מילה שמתחילה באות ניקוד (A, E, I, O, U) נשתמש בתווית הייחודית."}
            ],
            "unseens": [
                {"text": "Tom has a small blue bike. He rides his bike to school every morning. He loves his bike very much.", "q": "What color is Tom's bike?", "a": "Blue", "opts": ["Blue", "Red", "Green", "Yellow"], "hint": "חפשו את תיאור הצבע מיד בתחילת המשפט הראשון בטקסט."},
                {"text": "Lily has a white cat named Fluffy. Fluffy likes to sleep on the big red sofa in the living room all day long.", "q": "Where does Fluffy like to sleep?", "a": "On the sofa", "opts": ["On the sofa", "In the garden", "Under the bed", "In the kitchen"], "hint": "חפשו את המילה sleep (לישון) בטקסט וראו איזה רהיט מוזכר מיד אחריה."}
            ],
            "completions": [
                {"q": "Every night, I go to sleep in my cozy ____.", "a": "bed", "opts": ["bed", "car", "chair", "tree"], "hint": "איפה אנחנו נשכבים לישון כשמגיע הלילה?"},
                {"q": "Look at the sky! The sun is shining and it is very ____ today.", "a": "hot", "opts": ["hot", "cold", "sad", "green"], "hint": "אם השמש זורחת חזק, איך נרגיש בחוץ?"}
            ],
            "opposites": [
                {"q": "What is the opposite (ההפך) of the word 'Big'?", "a": "Small", "opts": ["Small", "Tall", "Good", "Heavy"], "hint": "אם משהו הוא לא גדול, הוא כנראה..."},
                {"q": "What is the opposite (ההפך) of the word 'Happy'?", "a": "Sad", "opts": ["Sad", "Bad", "Cold", "Short"], "hint": "כשמישהו לא שמח ומחויך, הוא מרגיש..."}
            ],
            "odd_out": [
                {"q": "Which word is the ODD one out (יוצא דופן)?", "a": "Table", "opts": ["Dog", "Cat", "Table", "Lion"], "hint": "שלוש מהאפשרויות הן חיות, ואילו אפשרות אחת היא רהיט בבית."},
                {"q": "Which word is the ODD one out (יוצא דופן)?", "a": "Car", "opts": ["Apple", "Banana", "Car", "Orange"], "hint": "חפשו את פריט התחבורה שלא שייך למשפחת הפירות המתוקים."}
            ],
            "boss": [
                {"q": "כיצד נתרגם נכון לאנגלית את המשפט: 'שלום, השם שלי הוא דן'?", "a": "Hello, my name is Dan", "opts": ["Hello, my name is Dan", "Goodbye, I am Dan", "Hello, this is a dog", "Good morning, friend"], "hint": "חפשו את המילים המדויקות ל'שלום' (Hello) ו'השם שלי' (my name)."}
            ]
        },
        "10-12": {
            "vocab": [
                ("Football", "כדורגל", "ענף ספורט פופולרי שבו בועטים בכדור לשער"),
                ("Breakfast", "ארוחת בוקר", "הארוחה החשובה ביותר שאוכלים כשמתעוררים בבוקר"),
                ("School", "בית ספר", "המקום אליו הולכים בכל בוקר כדי ללמוד ולפגוש חברים"),
                ("Beautiful", "יפה", "מילה שמתארת משהו שנראה טוב ונעים לעין"),
                ("Tomorrow", "מחר", "היום שיגיע מיד אחרי שהיום הנוכחי יסתיים"),
                ("Summer", "קיץ", "העונה החמה בשנה שבה יוצאים לחופש הגדול"),
                ("Doctor", "רופא", "אדם שעובד בבית חולים ועוזר לאנשים חולים להבריא"),
                ("Journey", "מסע", "טיול ארוך או מעבר ממקום למקום")
            ],
            "grammar": [
                {"q": "They ____ football in the park yesterday afternoon.", "a": "played", "opts": ["played", "play", "playing", "plays"], "hint": "המילה yesterday (אתמול) מסמנת שהאירוע כבר קרה בעבר (נוסיף סיומת ed לעבר פשוט)."},
                {"q": "Listen! The teacher ____ to the class right now.", "a": "is talking", "opts": ["is talking", "talks", "talked", "are talking"], "hint": "המילים Listen ו-right now מראות שהפעולה קורת ברגע זה ממש (Present Progressive)."}
            ],
            "unseens": [
                {"text": "Mia and Liam love playing computer games. Yesterday, they built a giant castle with high stone walls to protect their virtual village from monsters.", "q": "Why did they build high stone walls?", "a": "To protect their village", "opts": ["To protect their village", "To hide from friends", "To build a kitchen", "To catch fish"], "hint": "קראו את סוף המשפט השני, המילה protect פירושה להגן."}
            ],
            "completions": [
                {"q": "I always wash my hands with soap before having ____.", "a": "dinner", "opts": ["dinner", "games", "sleep", "clothes"], "hint": "לפני איזה אירוע הגיוני ואחראי לשטוף ידיים היטב עם סבון?"}
            ],
            "opposites": [
                {"q": "What is the opposite of 'Strong'?", "a": "Weak", "opts": ["Weak", "Fast", "Hard", "Heavy"], "hint": "ההפך ממישהו חזק ובעל כוח רב."}
            ],
            "odd_out": [
                {"q": "Which word is the ODD one out?", "a": "Pizza", "opts": ["Math", "Science", "Pizza", "History"], "hint": "חפשו את המאכל הטעים שאינו נחשב למקצוע לימוד בכיתה."}
            ],
            "boss": [
                {"q": "השלם את משפט התנאי הבא: If it rains tomorrow, we ____ go to the park.", "a": "will not", "opts": ["will not", "did not", "have not", "are"], "hint": "במשפט תנאי ראשון (First Conditional), נשתמש ב-will/will not עבור תוצאת העתיד."}
            ]
        },
        "13-15": {
            "vocab": [
                ("Opportunity", "הזדמנות", "סיטואציה שמאפשרת לנו להשיג או לעשות משהו חדש"),
                ("Challenge", "אתגר", "משימה קשה שדורשת מאמץ אך עוזרת לנו להשתפר"),
                ("Succeed", "להצליח", "להשיג את המטרה שקבענו לעצמנו לאחר עבודה קשה"),
                ("Environment", "סביבה", "העולם שסובב אותנו כולל הטבע, הצמחים והאוויר"),
                ("Government", "ממשלה", "הגוף המנהיג והמנהל את ענייני המדינה"),
                ("Influence", "השפעה", "היכולת לשנות או לעצב דעה והתנהגות של מישהו אחר")
            ],
            "grammar": [
                {"q": "By the time the police arrived, the thief ____ escaped.", "a": "had", "opts": ["had", "has", "have", "was"], "hint": "פעולה שהתרחשה והסתיימה לפני פעולה אחרת בעבר דורשת זמן עבר מושלם (Past Perfect)."},
                {"q": "If I ____ more time, I would learn how to code computer programs.", "a": "had", "opts": ["had", "have", "will have", "having"], "hint": "זהו משפט תנאי שני (Second Conditional) המביע מצב היפותטי, לכן בחלק של ה-If נשתמש ב-Past Simple."}
            ],
            "unseens": [
                {"text": "Many teenagers dream of becoming digital content creators. While it looks remarkably easy on screen, it actually requires hours of precise video editing, strategic planning, and consistent dedication to grow an audience.", "q": "What does being a content creator actually require?", "a": "Hours of editing and planning", "opts": ["Hours of editing and planning", "Only a premium smartphone", "No effort at all", "Just walking around"], "hint": "חפשו את המילה requires (דורש) בטקסט וראו איזה מאמץ מפורט מיד אחריה."}
            ],
            "completions": [
                {"q": "Learning a second language gives you a wonderful ____ to travel and work abroad.", "a": "opportunity", "opts": ["opportunity", "problem", "danger", "accident"], "hint": "לימוד שפה פותח דלתות ונותן לנו...?"}
            ],
            "opposites": [
                {"q": "What is the opposite of the word 'Succeed'?", "a": "Fail", "opts": ["Fail", "Win", "Try", "Grow"], "hint": "אם המטרה לא הושגה חלילה והפעולה נכשלה."}
            ],
            "odd_out": [
                {"q": "Which word is the ODD one out?", "a": "Easy", "opts": ["Challenge", "Difficult", "Hard", "Easy"], "hint": "שלוש מילים מתארות קושי ומאמץ, ומילה אחת מתארת משהו פשוט וקליל."}
            ],
            "boss": [
                {"q": "Choose the correct passive voice version: 'The chef prepared the food.'", "a": "The food was prepared by the chef.", "opts": ["The food was prepared by the chef.", "The food is prepared by the chef.", "The chef was prepared by the food.", "The food had prepared by the chef."], "hint": "במעבר לסביל בעבר (Past Passive), נשתמש ב-was/were בתוספת הפועל בצורת ה-V3 שלו."}
            ]
        }
    }

    # בניית 50 שלבים יציבים ומלאים
    for age, data in raw_data.items():
        # יצירת רשימה פשוטה של כל המילים בעברית ובאנגלית של אותה קבוצת גיל למסיחים דינמיים
        all_hebrews = [item[1] for item in data["vocab"]]
        all_english = [item[0] for item in data["vocab"]]
        
        for level in range(1, 51):
            db[age][str(level)] = {}
            for sub in range(8):
                task = {}
                
                if sub == 0:
                    # אוצר מילים: אנגלית לעברית (מסיחים אמיתיים לגמרי מהמאגר)
                    word, heb, hint = random.choice(data["vocab"])
                    other_options = [h for h in all_hebrews if h != heb]
                    distractors = random.sample(other_options, min(3, len(other_options)))
                    opts = [heb] + distractors
                    random.shuffle(opts)
                    task = {"title": "אוצר מילים: תרגום לעברית ותרגול", "q": f"מהו הפירוש המדויק בעברית של המילה: '{word}'?", "a": heb, "options": opts, "hint": hint}
                    
                elif sub == 1:
                    # אוצר מילים: עברית לאנגלית (מסיחים אמיתיים לגמרי מהמאגר)
                    word, heb, hint = random.choice(data["vocab"])
                    other_options = [e for e in all_english if e != word]
                    distractors = random.sample(other_options, min(3, len(other_options)))
                    opts = [word] + distractors
                    random.shuffle(opts)
                    task = {"title": "אוצר מילים: תרגום לאנגלית ותרגול", "q": f"כיצד נכתוב ונבטא באנגלית את המילה המבוקשת: '{heb}'?", "a": word, "options": opts, "hint": f"המילה באנגלית מתחילה באות הראשונה {word[0]}"}
                    
                elif sub == 2:
                    # דקדוק וזמנים
                    g = random.choice(data["grammar"])
                    opts = list(g["opts"])
                    random.shuffle(opts)
                    task = {"title": "דקדוק ואינטואיציה לשונית (Grammar)", "q": f"השלם בצורה נכונה ותקנית את המשפט הבא: \n\n {g['q']}", "a": g["a"], "options": opts, "hint": g["hint"]}
                    
                elif sub == 3:
                    # הבנת הנקרא (Unseen)
                    u = random.choice(data["unseens"])
                    opts = list(u["opts"])
                    random.shuffle(opts)
                    task = {"title": "הבנת הנקרא (Reading Comprehension)", "unseen": u["text"], "q": u["q"], "a": u["a"], "options": opts, "hint": u["hint"]}
                    
                elif sub == 4:
                    # השלמת משפטים מהקשר
                    c = random.choice(data["completions"])
                    opts = list(c["opts"])
                    random.shuffle(opts)
                    task = {"title": "השלמת משפטים מהקשר משמעותי", "q": f"בחר את המילה המתאימה ביותר להשלמת ההיגיון במשפט: \n\n {c['q']}", "a": c["a"], "options": opts, "hint": c["hint"]}
                    
                elif sub == 5:
                    # הפכים ומילים נרדפות
                    o = random.choice(data["opposites"])
                    opts = list(o["opts"])
                    random.shuffle(opts)
                    task = {"title": "עולם המילים: מציאת הפכים (Opposites)", "q": o["q"], "a": o["a"], "options": opts, "hint": o["hint"]}
                    
                elif sub == 6:
                    # יוצא דופן
                    od = random.choice(data["odd_out"])
                    opts = list(od["opts"])
                    random.shuffle(opts)
                    task = {"title": "חשיבה לוגית: יוצא דופן (Odd One Out)", "q": od["q"], "a": od["a"], "options": opts, "hint": od["hint"]}
                    
                elif sub == 7:
                    # משימת בוס השלב (אתגר מורכב וסגירת שלב)
                    b = random.choice(data["boss"])
                    opts = list(b["opts"])
                    random.shuffle(opts)
                    task = {"title": "⚔️ משימת הבוס הגדול ונעילת השלב!", "q": b["q"], "a": b["a"], "options": opts, "hint": b["hint"]}
                
                db[age][str(level)][str(sub)] = task
                
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- טעינת נתונים קיימים באפליקציה ---
users_db = load_json(DB_FILE)
content_db = load_json(CONTENT_FILE)

if "user" not in st.session_state: st.session_state.user = None
if "screen" not in st.session_state: st.session_state.screen = "login"
if "hint_clicked" not in st.session_state: st.session_state.hint_clicked = False

# ==========================================
# מסך 1: מסך כניסה ורישום שחקנים
# ==========================================
if st.session_state.screen == "login":
    st.title("🌌 NEXUS ENGLISH ACADEMY - V11")
    st.write("ברוכים הבאים למערכת המורחבת ללימוד אנגלית ללא סרטונים ובלי מסיחים גנריים. היכנסו לחשבון או צרו שחקן חדש:")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 כניסת שחקן קיים")
        existing_name = st.selectbox("בחר את השם שלך מהרשימה:", list(users_db.keys()) if users_db else ["אין עדיין שחקנים רשומים"])
        if st.button("התחבר והמשך מהנקודה שעצרת 🚀", use_container_width=True):
            if existing_name in users_db:
                curr_user = users_db[existing_name]
                
                # תיקון אוטומטי מובנה למשתמשי עבר למניעת KeyError
                if "group" not in curr_user:
                    age = curr_user.get("age", 11)
                    if age <= 9: curr_user["group"] = "7-9"
                    elif age <= 12: curr_user["group"] = "10-12"
                    else: curr_user["group"] = "13-15"
                    users_db[existing_name] = curr_user
                    save_json(DB_FILE, users_db)
                
                st.session_state.user = curr_user
                st.session_state.screen = "game"
                st.session_state.hint_clicked = False
                st.rerun()
                
    with col2:
        st.subheader("✨ יצירת פרופיל שחקן חדש")
        new_name = st.text_input("הכנס שם מלא או כינוי:")
        new_age = st.number_input("בן כמה אתה? (גילאי 7 עד 15)", 7, 15, 11)
        if st.button("פתח משתמש חדש והתחל מאפס 🎮", use_container_width=True):
            if new_name and new_name not in users_db:
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
    
    completed_stage = user.get('level', 2) - 1
    prize = f"גביע זהב עתידני - דרגת {completed_stage} שלבים 🌟"
    
    st.markdown(f"<h2>כל הכבוד {user.get('name', 'שחקן')}! הפגנת התמדה מטורפת באנגלית!</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#eff6ff; color:#1e40af; padding:25px; border-radius:15px; font-size:26px; font-weight:bold; border:2px solid #3b82f6; margin:25px 0;'>🎁 הפרס שנוסף לכספת שלך: {prize}</div>", unsafe_allow_html=True)
    
    if st.button("אסוף את הפרס לארון והמשך לשלב הבא ➡️", type="primary", use_container_width=True):
        if "rewards" not in user: user["rewards"] = []
        if prize not in user["rewards"]:
            user["rewards"].append(prize)
        users_db[user['name']] = user
        save_json(DB_FILE, users_db)
        st.session_state.screen = "game"
        st.session_state.hint_clicked = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# מסך 3: לוח המשחק והלמידה המרכזי המעודכן
# ==========================================
elif st.session_state.screen == "game" and st.session_state.user is not None:
    user = st.session_state.user
    
    # --- סיידבר ניהול, התקדמות וארון גביעים ---
    with st.sidebar:
        st.markdown(f"## 🕵️‍♂️ פרופיל: {user.get('name', 'שחקן')}")
        st.write(f"**קבוצת לימוד:** גילאי {user.get('group', '10-12')}")
        st.write(f"**ניקוד מצטבר:** {user.get('score', 0)} 🏆")
        st.write(f"**שלב נוכחי:** {user.get('level', 1)} / 50")
        st.progress(user.get('level', 1) / 50)
        
        st.markdown("---")
        st.markdown("### 🎒 כספת ארון הפרסים שלך")
        if not user.get('rewards'):
            st.info("ארון הפרסים ריק כרגע. הגיעו לשלב 10 כדי לפתוח את הגביע הראשון שלכם!")
        else:
            for r in user['rewards']:
                st.success(f"⭐ {r}")
                
        st.markdown("---")
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

    # שליפת המשימה הספציפית מתוך ה-JSON
    lvl_str = str(user.get('level', 1))
    sub_str = str(user.get('sub_level', 0))
    age_group = user.get('group', '10-12')
    
    mission = content_db.get(age_group, {}).get(lvl_str, {}).get(sub_str, {})
    
    if not mission:
        st.balloons()
        st.success("👑 מדהים! השלמתם את כל 50 השלבים באפליקציה בהצלחה ענקית!")
        st.stop()

    # מחווני התקדמות פנימיים
    st.title(f"📍 שלב: {lvl_str} מתוך 50")
    st.subheader(f"🎯 משימה פנימית: {int(sub_str)+1} מתוך 8")
    st.progress((int(sub_str)) / 8.0)
    st.markdown("---")

    # כרטיסיית המשימה המרכזית בעיצוב נקי
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="cyber-title">סוג המשימה: {mission.get("title", "משימה")}</div>', unsafe_allow_html=True)
    
    # במידה ויש קטע קריאה (Unseen)
    if "unseen" in mission:
        st.markdown(f'<div class="english-unseen-box"><strong>📖 Read the story and answer:</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)

    # הצגת השאלה האמיתית
    st.markdown(f'<div class="cyber-text">👉 {mission.get("q", "שאלה")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # הצגת אפשרויות הבחירה (התשובות האמריקאיות)
    options = mission.get("options", ["A", "B", "C", "D"])
    ans = st.radio("בחר את התשובה הנכונה:", options, index=None, key=f"radio_v11_{lvl_str}_{sub_str}")

    # מנגנון הרמזים
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
            
            user['sub_level'] = user.get('sub_level', 0) + 1
            user['score'] = user.get('score', 0) + 10
            
            if user['sub_level'] > 7:
                user['level'] = user.get('level', 1) + 1
                user['sub_level'] = 0
                
                if (user['level'] - 1) % 10 == 0:
                    st.session_state.screen = "milestone"
            
            users_db[user['name']] = user
            save_json(DB_FILE, users_db)
            st.session_state.hint_clicked = False
            st.rerun()
        else:
            st.error("❌ התשובה אינה נכונה. קראו שוב את השאלה או השתמשו ברמז ונסו שנית!")
