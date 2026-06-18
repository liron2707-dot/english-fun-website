import streamlit as st
import streamlit.components.v1 as components

# הגדרת עמוד בסיסית - כותרת ופריסה
st.set_page_config(page_title="SmartEnglish - לומדים אנגלית בכיף", page_icon="🚀", layout="centered")

# --- מנוע הקראה קולית (Text to Speech) מובנה בדפדפן ---
def speak_button(text, lang="en-US", label="🔊 השמע"):
    """פונקציה שמזריקה רכיב HTML קטן המאפשר הקראה בלחיצה ללא חבילות חיצוניות"""
    html_code = f"""
    <button onclick="speak()" style="
        background-color: #0ea5e9; 
        color: white; 
        border: none; 
        padding: 6px 14px; 
        border-radius: 20px; 
        cursor: pointer; 
        font-family: system-ui; 
        font-size: 14px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">{label}</button>
    <script>
    function speak() {{
        var msg = new SpeechSynthesisUtterance({repr(text)});
        msg.lang = '{lang}';
        msg.rate = 0.85; // מהירות מעט איטית לילדים
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(html_code, height=35)

# --- עיצוב קסטום מקיף (CSS) לתמיכה ב-RTL, פונטים גדולים ונראות של משחק ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Heebo', sans-serif;
        background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
    }
    
    .rtl-box {
        direction: rtl;
        text-align: right;
    }
    .ltr-box {
        direction: ltr;
        text-align: left;
        font-size: 18px;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #0ea5e9;
        margin-bottom: 10px;
    }
    .game-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 2px solid #e2e8f0;
    }
    h1, h2, h3 {
        font-weight: 900 !important;
        color: #1e3a8a !important;
    }
    .stButton>button {
        background-color: #22c55e !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        padding: 10px 25px !important;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# --- ניהול זיכרון המשתמש ושמירה ב-URL (Query Params) ---
# טעינה ראשונית מכתובת האתר במידה וקיים
if "user_name" not in st.session_state:
    st.session_state.user_name = st.query_params.get("name", "")
if "user_age" not in st.session_state:
    try:
        st.session_state.user_age = int(st.query_params.get("age", 10))
    except:
        st.session_state.user_age = 10
if "score" not in st.session_state:
    try:
        st.session_state.score = int(st.query_params.get("score", 0))
    except:
        st.session_state.score = 0
if "level" not in st.session_state:
    try:
        st.session_state.level = int(st.query_params.get("level", 1))
    except:
        st.session_state.level = 1
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True if st.session_state.user_name != "" else False

def save_progress():
    """פונקציה השומרת את המצב הנוכחי בפרמטרים של כתובת האתר"""
    st.query_params["name"] = st.session_state.user_name
    st.query_params["age"] = st.session_state.user_age
    st.query_params["score"] = st.session_state.score
    st.query_params["level"] = st.session_state.level

# --- מסך כניסה והרשמה ---
if not st.session_state.logged_in:
    st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
    st.title("🎓 ברוכים הבאים ל-SmartEnglish!")
    st.subheader("האתר שיהפוך את האנגלית שלכם למושלמת באמצעות משחקים!")
    
    with st.container(border=True):
        name_input = st.text_input("מה השם שלך?", placeholder="הקלד שם כאן...")
        age_input = st.slider("בן/בת כמה את/ה?", min_value=10, max_value=15, value=11)
        
        if st.button("🚀 בואו נתחיל לשחק!", use_container_width=True):
            if name_input.strip() == "":
                st.error("אופס! צריך להזין שם כדי שנוכל לשמור את הניקוד שלך.")
            else:
                st.session_state.user_name = name_input
                st.session_state.user_age = age_input
                st.session_state.score = 0
                # קביעת רמה התחלתית לפי גיל
                if age_input in [10, 11]: st.session_state.level = 1
                elif age_input in [12, 13]: st.session_state.level = 2
                else: st.session_state.level = 3
                st.session_state.logged_in = True
                save_progress()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- מסך האפליקציה הראשי (לאחר התחברות) ---
else:
    # סרגל עליון מעוצב (Dashboard)
    st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
    with c1:
        st.markdown(f"🏆 **שלום, {st.session_state.user_name}!**")
    with c2:
        st.markdown(f"⭐ **ניקוד צבור:** `{st.session_state.score}`")
    with c3:
        st.markdown(f"🗺️ **שלב נוכחי:** `רמה {st.session_state.level}`")
    with c4:
        if st.button("יציאה ↩️"):
            st.session_state.logged_in = False
            st.query_params.clear()
            st.rerun()
    
    # מד התקדמות ויזואלי לשלב הבא
    st.progress(min(st.session_state.score % 100 / 100, 1.0), text=f"התקדמות בתוך שלב {st.session_state.level}")
    st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)

    # מאגר תוכן מובנה לכל רמה (אוצר מילים, דקדוק, סיפורים, וידאו, מבחן)
    content_db = {
        1: {
            "title": "עולם היסודות (גילאי 10-11)",
            "vocab": {"Apple": "תפוח 🍎", "Summer": "קיץ ☀️", "Friend": "חבר 🤝", "Family": "משפחה 👨‍👩‍👧‍👦", "Water": "מים 💧"},
            "grammar_title": "מתי נשתמש ב- Am, Is, Are?",
            "grammar_text": "• I הולך עם Am (למשל: I am tall)\n• היחידים He, She, It הולכים עם Is (למשל: She is smart)\n• הרבים We, You, They הולכים עם Are (למשל: They are happy)",
            "grammar_q": "השלם את המשפט: 'The dog ____ barking.'",
            "grammar_options": ["am", "is", "are"],
            "grammar_correct": "is",
            "story_title": "The Magic Red Ball",
            "story_text": "Ben has a magical red ball. Every afternoon, he takes the ball to the park. The ball can bounce very high, straight into the clouds! One day, the ball did not come down. It stayed in the sky and became a new star.",
            "unseen_q": "Where does Ben take his ball every afternoon?",
            "unseen_options": ["To the school", "To the park", "To his bedroom"],
            "unseen_correct": "To the park",
            "video_id": "8wXG7IAnHdQ", # קליפ לימודי קצר באנגלית לילדים
            "exam_q": "איך כותבים את המילה 'חבר' באנגלית?",
            "exam_options": ["Family", "Friend", "Summer"],
            "exam_correct": "Friend"
        },
        2: {
            "title": "יער המשפטים (גילאי 12-13)",
            "vocab": {"Adventure": "הרפתקה 🗺️", "Challenge": "אתגר 🎯", "Discover": "לגלות 🔍", "Celebration": "חגיגה 🎉", "Protect": "להגן 🛡️"},
            "grammar_title": "עבר פשוט - Past Simple",
            "grammar_text": "משתמשים בעבר פשוט לפעולות שהסתיימו בעבר.\n• לפעלים רגילים נוסיף ed בסוף הפועל: Walk -> Walked\n• לפעלים יוצאי דופן (Irregular) הצורה משתנה לחלוטין ויש לזכור אותה: Go -> Went, Buy -> Bought",
            "grammar_q": "מהי צורת העבר הנכונה של הפועל 'Eat'?",
            "grammar_options": ["Eated", "Ate", "Eating"],
            "grammar_correct": "Ate",
            "story_title": "The Treehouse Mystery",
            "story_text": "Maya and Leo decided to build a beautiful treehouse in their backyard. They spent three days collecting wood and hammers. On the fourth day, they found a small wooden box hidden inside the tree trunk. Inside the box, there was an old golden key.",
            "unseen_q": "What did Maya and Leo find inside the tree trunk?",
            "unseen_options": ["A wooden box with a key", "A map", "A lost hammer"],
            "unseen_correct": "A wooden box with a key",
            "video_id": "maM9gNfskS4", # סרטון דקדוק חווייתי
            "exam_q": "איך אומרים 'הרפתקה' באנגלית?",
            "exam_options": ["Discover", "Challenge", "Adventure"],
            "exam_correct": "Adventure"
        },
        3: {
            "title": "מצודת הדיבור וההצלחה (גילאי 14-15)",
            "vocab": {"Accomplish": "להשיג/להשלים 🏆", "Consequence": "השלכה/תוצאה ⏳", "Generous": "נדיב 🤝", "Independent": "עצמאי 🗽", "Influence": "השפעה 🌊"},
            "grammar_title": "הווה מושלם - Present Perfect",
            "grammar_text": "משתמשים בזה לפעולה שקראה בעבר אך משפיעה על ההווה או שאין לה זמן מוגדר.\nמבנה: Have / Has + הפועל בצורה השלישית (V3).\nדוגמה: I have lived in Israel for ten years.",
            "grammar_q": "בחר את המשפט התקני:",
            "grammar_options": ["She has went to London.", "She has gone to London.", "She have gone to London."],
            "grammar_correct": "She has gone to London.",
            "story_title": "The Journey to Mars",
            "story_text": "In the year 2045, Captain Sarah boarded the Ares-5 spacecraft. Her lifelong dream was to accomplish what no human had ever done before: walking on Mars. After an independent journey of seven months through dark space, the red planet finally appeared in the window.",
            "unseen_q": "How long did the journey to Mars take?",
            "unseen_options": ["Three days", "Seven months", "Two years"],
            "unseen_correct": "Seven months",
            "video_id": "d5U7g_sZ09g", # וידאו מתקדם
            "exam_q": "מה הפירוש של המילה 'Independent'?",
            "exam_options": ["עצמאי", "נדיב", "השפעה"],
            "exam_correct": "עצמאי"
        }
    }

    current_data = content_db[st.session_state.level]

    # כותרת הרמה הנוכחית
    st.markdown(f'<div class="rtl-box"><h2>שלב {st.session_state.level}: {current_data["title"]}</h2></div>', unsafe_allow_html=True)

    # יצירת טאבים למשחקים ולמידה
    t_vocab, t_grammar, t_unseen, t_video, t_exam = st.tabs([
        "📚 אוצר מילים", 
        "🎮 משחקי דקדוק", 
        "📖 סיפורים ואנסין", 
        "🎬 סרטוני הסבר", 
        "🎯 מבחן עליית שלב"
    ])

    # --- טאב 1: אוצר מילים ---
    with t_vocab:
        st.markdown('<div class="rtl-box"><h3>מילון הקסם: לחצו כדי לשמוע ולהגות נכון!</h3></div>', unsafe_allow_html=True)
        for eng, heb in current_data["vocab"].items():
            col_box = st.container()
            with col_box:
                col_e, col_h, col_speak = st.columns([2, 2, 1])
                with col_e:
                    st.markdown(f'<div class="ltr-box"><b>{eng}</b></div>', unsafe_allow_html=True)
                with col_h:
                    st.markdown(f'<div class="rtl-box" style="padding:15px; font-size:18px;">{heb}</div>', unsafe_allow_html=True)
                with col_speak:
                    speak_button(eng, label="📢 Listen")
                    speak_button(heb, lang="he-IL", label="🔊 עברית")

    # --- טאב 2: משחקי דקדוק ---
    with t_grammar:
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown(f"### {current_data['grammar_title']}")
        st.info(current_data['grammar_text'])
        st.write("---")
        st.markdown("#### 🎲 משחק אתגר הדקדוק:")
        g_ans = st.radio(current_data['grammar_q'], current_data['grammar_options'], key="grammar_radio")
        
        if st.button("בדיקת תשובה 📝", key="btn_g"):
            if g_ans == current_data['grammar_correct']:
                st.balloons()
                st.success("🤩 מדהים! תשובה נכונה! קיבלת 10 נקודות!")
                st.session_state.score += 10
                save_progress()
            else:
                st.error("😢 אופס, לא מדויק. אל ייאוש, קראו את החוק למעלה ונסו שוב!")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- טאב 3: סיפורים ואנסין ---
    with t_unseen:
        st.markdown('<div class="rtl-box"><h3>📖 קראו, האזינו וענו על השאלות</h3></div>', unsafe_allow_html=True)
        
        # כפתור השמעת כל הסיפור
        st.markdown("👇 לחצו כדי שהאתר יקריא לכם את הסיפור המלא במבטא מושלם:")
        speak_button(current_data['story_text'], label="🔊 הקרא לי את הסיפור המלא (Play Story)")
        
        # הצגת הסיפור משמאל לימין
        st.markdown(f'<div class="ltr-box" style="font-size:20px; line-height:1.8;">{current_data["story_text"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="rtl-box"><h4>❓ שאלת הבנת הנקרא (Unseen):</h4></div>', unsafe_allow_html=True)
        u_ans = st.selectbox(current_data['unseen_q'], current_data['unseen_options'])
        
        if st.button("בדיקת אנסין 🔍"):
            if u_ans == current_data['unseen_correct']:
                st.snow()
                st.success("🎉 כל הכבוד! הבנת הנקרא שלכם מצוינת. זכיתם ב-20 נקודות!")
                st.session_state.score += 20
                save_progress()
            else:
                st.error("❌ תשובה לא נכונה. נסו לקרוא או להקשיב לסיפור פעם נוספת!")

    # --- טאב 4: סרטוני הסבר ---
    with t_video:
        st.markdown('<div class="rtl-box"><h3>🎬 צפו ושירו ביחד כדי ללמוד בקלות!</h3></div>', unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={current_data['video_id']}")
        st.caption("מומלץ להפעיל את הכתוביות (CC) ביוטיוב בשביל תרגום מובנה לעברית!")

    # --- טאב 5: מבחן עליית שלב ---
    with t_exam:
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown("### 🎯 המבחן הגדול לעליית שלב!")
        st.write("ענו נכון על שאלה זו כדי לפתוח את השלב הבא במשחק!")
        
        exam_ans = st.radio(current_data['exam_q'], current_data['exam_options'], key="exam_radio")
        
        if st.button("🏁 הגש מבחן סיום שלב"):
            if exam_ans == current_data['exam_correct']:
                st.balloons()
                st.snow()
                
                if st.session_state.level < 3:
                    st.session_state.level += 1
                    st.success(f"🥳 יששש! עברתם את המבחן בהצלחה! ברוכים הבאים לשלב {st.session_state.level}!")
                else:
                    st.success("👑 אלופים!!! סיימתם את הרמה הגבוהה ביותר באתר והפכתם למאסטרים באנגלית!")
                
                st.session_state.score += 50
                save_progress()
                st.rerun()
            else:
                st.error("😭 התשובה אינה נכונה. חזרו על אוצר המילים ונסו שוב כדי לעלות שלב!")
        st.markdown('</div>', unsafe_allow_html=True)
