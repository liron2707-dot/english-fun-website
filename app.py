import streamlit as st
import streamlit.components.v1 as components
import random

# הגדרות עמוד - פריסה רחבה ונקייה
st.set_page_config(page_title="SmartEnglish - אנגלית בכיף", page_icon="🎓", layout="wide")

# --- שמירת נתונים קבועה בכתובת האתר (URL) ---
if "user_name" not in st.session_state:
    st.session_state.user_name = st.query_params.get("name", "")
if "user_age" not in st.session_state:
    try: st.session_state.user_age = int(st.query_params.get("age", 11))
    except: st.session_state.user_age = 11
if "score" not in st.session_state:
    try: st.session_state.score = int(st.query_params.get("score", 0))
    except: st.session_state.score = 0
if "level" not in st.session_state:
    try: st.session_state.level = int(st.query_params.get("level", 1))
    except: st.session_state.level = 1
if "achievements" not in st.session_state:
    st.session_state.achievements = st.query_params.get_all("ach")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True if st.session_state.user_name != "" else False

def save_progress():
    """שמירת המצב הנוכחי ב-URL כדי שהילד יוכל לחזור מאותה נקודה"""
    st.query_params["name"] = st.session_state.user_name
    st.query_params["age"] = st.session_state.user_age
    st.query_params["score"] = st.session_state.score
    st.query_params["level"] = st.session_state.level
    # שמירת הישגים במידה ויש
    if st.session_state.achievements:
        st.query_params["ach"] = st.session_state.achievements

def add_score(amount):
    st.session_state.score += amount
    save_progress()
    st.toast(f"🏆 כל הכבוד! זכית ב-{amount} נקודות!", icon="⭐")

# --- מנוע עיצוב מקיף לקריאות מקסימלית ותמיכה ב-RTL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    /* רקע בהיר ונוח לעיניים */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Heebo', sans-serif;
        background-color: #f8fafc;
        color: #1e293b !important;
    }
    
    /* תיבות טקסט בעברית - מימין לשמאל */
    .rtl-container {
        direction: rtl;
        text-align: right;
        padding: 10px;
    }
    
    /* תיבות קוד וכרטיסיות באנגלית - משמאל לימין */
    .ltr-card {
        direction: ltr;
        text-align: left;
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px;
        border: 3px solid #e2e8f0;
        border-left: 8px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    
    /* כותרות גדולות ובולטות */
    h1, h2, h3 {
        font-weight: 900 !important;
        color: #1e3a8a !important;
    }
    
    /* כפתורים גדולים, צבעוניים וקריאים */
    .stButton>button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(22, 163, 74, 0.2) !important;
        width: 100%;
    }
    
    /* כפתורי משנה (בדיקה/רמז) */
    .hint-btn>button {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
        color: #334155 !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- מנוע הקראה קולית (TTS) מובנה בדפדפן ---
def speak_button(text, lang="en-US", label="🔊 השמע מילה"):
    html_code = f"""
    <button onclick="speak()" style="background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{label}</button>
    <script>
    function speak() {{
        var msg = new SpeechSynthesisUtterance({repr(text)});
        msg.lang = '{lang}';
        msg.rate = 0.8;
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(html_code, height=45)

# --- מנוע זיהוי דיבור (Speech Recognition) מתוקן ויציב ללא שגיאות פייתון ---
def speech_recognition_game(target_word):
    # התיקון ההנדסי הגדול: הביטוי מנוהל כעת לחלוטין בצד הלקוח (JS) כדי למנוע קריסה בפייתון
    html_code = f"""
    <div style="text-align: center; font-family: system-ui; margin-top: 10px;">
        <button id="rec_btn" onclick="startDictation()" style="background: #ef4444; color: white; border: none; padding: 12px 24px; border-radius: 12px; cursor: pointer; font-size: 18px; font-weight: bold; width: 100%;">🎤 לחצו ואמרו באנגלית: "{target_word}"</button>
        <p id="result_text" style="font-size: 18px; font-weight: bold; margin-top: 12px; color: #475569;">לחצו על המיקרופון ודברו אל המחשב...</p>
    </div>
    <script>
    function startDictation() {{
        if (window.hasOwnProperty('webkitSpeechRecognition')) {{
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "en-US";
            
            var btn = document.getElementById('rec_btn');
            btn.style.background = "#22c55e";
            btn.innerText = "🎧 האתר מקשיב לך עכשיו...";
            
            recognition.start();
            
            recognition.onresult = function(e) {{
                recognition.stop();
                var user_said = e.results[0][0].transcript.toLowerCase().trim();
                var target = "{target_word}".toLowerCase().trim();
                var res_p = document.getElementById('result_text');
                
                btn.style.background = "#ef4444";
                btn.innerText = '🎤 נסו שוב';
                
                if(user_said.includes(target) || target.includes(user_said)) {{
                    res_p.innerHTML = "🍏 <span style='color:green; font-size:20px;'>מדהים! אמרתם מעולה! ("+user_said+")</span>";
                }} else {{
                    res_p.innerHTML = "🍎 <span style='color:red;'>האתר שמע: \\""+user_said+"\\". נסו להגיד שוב חזק וברור!</span>";
                }}
            }};
            recognition.onerror = function(e) {{
                recognition.stop();
                document.getElementById('rec_btn').style.background = "#ef4444";
                document.getElementById('rec_btn').innerText = '🎤 שגיאה במיקרופון, נסו שוב';
            }}
        }} else {{
            document.getElementById('result_text').innerText = "הדפדפן לא תומך במיקרופון. מומלץ להשתמש בגוגל כרום במחשב.";
        }}
    }}
    </script>
    """
    components.html(html_code, height=130)

# --- מאגר תוכן ענק ומורחב לכל השלבים (מילים, משחקים, סיפורים, מבחנים) ---
content_db = {
    1: {
        "title": "שלב 1: אי היסודות הקסום 🌟",
        "vocab": [
            {"eng": "Apple", "heb": "תפוח 🍎", "hint": "פרי מתוק בצבע אדום או ירוק"},
            {"eng": "Summer", "heb": "קיץ ☀️", "hint": "העונה החמה ביותר בשנה, הולכים לים"},
            {"eng": "Friend", "heb": "חבר 🤝", "hint": "מישהו שאוהבים לשחק ולדבר איתו"},
            {"eng": "School", "heb": "בית ספר 🏫", "hint": "המקום אליו הולכים בבוקר כדי ללמוד ולראות חברים"},
            {"eng": "Family", "heb": "משפחה 👨‍👩‍👧‍👦", "hint": "אבא, אמא, אחים ואחיות שאוהבים אותנו"},
            {"eng": "Water", "heb": "מים 💧", "hint": "מה שאנחנו שותים כשחם לנו"}
        ],
        "scramble_word": "SCHOOL",
        "scramble_hint": "המקום שבו לומדים ופוגשים את המורה והחברים",
        "grammar_title": "מתי נשתמש ב- Am, Is, Are?",
        "grammar_desc": "• I תמיד מקבל Am (למשל: I am a student)\n• He, She, It (יחיד) מקבלים Is (למשל: He is smart)\n• We, You, They (רבים) מקבלים Are (למשל: They are playing)",
        "grammar_q": "השלם את המשפט: 'The cat ____ sleeping on the sofa.'",
        "grammar_options": ["am", "is", "are"],
        "grammar_correct": "is",
        "story_title": "The Magic Red Ball ⚽",
        "story_text": "Ben has a magical red ball. Every afternoon, he takes the ball to the green park. The ball can bounce very high, straight into the white clouds! One day, the ball did not come down. It stayed in the sky and became a beautiful new star.",
        "unseen_q": "Where does Ben take his ball every afternoon?",
        "unseen_options": ["To the school", "To the park", "To his bedroom"],
        "unseen_correct": "To the park",
        "video_id": "8wXG7IAnHdQ",
        "exam_q": "איך כותבים באנגלית את המילה 'משפחה'?",
        "exam_options": ["Friend", "Family", "Summer"],
        "exam_correct": "Family"
    },
    2: {
        "title": "שלב 2: יער המשפטים וההרפתקאות 🗺️",
        "vocab": [
            {"eng": "Adventure", "heb": "הרפתקה 🗺️", "hint": "מסע מעניין ומותח למקום חדש"},
            {"eng": "Challenge", "heb": "אתגר 🎯", "hint": "משימה קשה אבל מעניינת שכיף להצליח בה"},
            {"eng": "Discover", "heb": "לגלות 🔍", "hint": "למצוא משהו חדש שלא ידענו עליו קודם"},
            {"eng": "Protect", "heb": "להגן 🛡️", "hint": "לשמור על מישהו או משהו מפני סכנה"},
            {"eng": "Celebration", "heb": "חגיגה 🎉", "hint": "מסיבה גדולה ושמחה עם מוזיקה ואוכל"},
            {"eng": "Beautiful", "heb": "יפה ✨", "hint": "משהו שממש נעים להסתכל עליו"}
        ],
        "scramble_word": "ADVENTURE",
        "scramble_hint": "מסע מרתק ומלא הפתעות",
        "grammar_title": "העבר הפשוט - Past Simple",
        "grammar_desc": "משתמשים בעבר לפעולות שהסתיימו אתמול או בעבר.\n• לפעלים רגילים נוסיף ed בסוף: Walk -> Walked\n• לפעלים יוצאי דופן הצורה משתנה: Go -> Went, Eat -> Ate",
        "grammar_q": "מהי צורת העבר הנכונה של הפועל 'Go'?",
        "grammar_options": ["Goed", "Went", "Going"],
        "grammar_correct": "Went",
        "story_title": "The Treehouse Mystery 🌳",
        "story_text": "Maya and Leo decided to build a beautiful treehouse in their big backyard. They spent three days collecting wood and tools. On the fourth day, they discovered a small wooden box hidden inside the tree. Inside the box, there was an old golden key.",
        "unseen_q": "What did Maya and Leo find inside the tree?",
        "unseen_options": ["A lost hammer", "A small wooden box with a key", "A green bird"],
        "unseen_correct": "A small wooden box with a key",
        "video_id": "maM9gNfskS4",
        "exam_q": "איך אומרים 'לגלות' באנגלית?",
        "exam_options": ["Protect", "Discover", "Challenge"],
        "exam_correct": "Discover"
    },
    3: {
        "title": "שלב 3: מצודת המאסטרים הגבוהה 👑",
        "vocab": [
            {"eng": "Accomplish", "heb": "להשיג/להשלים 🏆", "hint": "להצליח לסיים משימה גדולה או מטרה"},
            {"eng": "Independent", "heb": "עצמאי 🗽", "hint": "מישהו שעושה דברים לבד בלי צורך בעזרה"},
            {"eng": "Generous", "heb": "נדיב 🤝", "hint": "אדם שאוהב לתת, לעזור ולתרום לאחרים"},
            {"eng": "Influence", "heb": "השפעה 🌊", "hint": "היכולת לשנות או לגרום למישהו לפעול בדרך מסוימת"},
            {"eng": "Consequence", "heb": "תוצאה/השלכה ⏳", "hint": "מה שקורה בגלל מעשה שעשינו"},
            {"eng": "Environment", "heb": "סביבה 🌱", "hint": "הטבע, העולם והעצים שמסביבנו"}
        ],
        "scramble_word": "INDEPENDENT",
        "scramble_hint": "מישהו שלא תלוי באחרים ועושה דברים בכוחות עצמו",
        "grammar_title": "ההווה המושלם - Present Perfect",
        "grammar_desc": "משתמשים למעשים שקרו בעבר ומשפיעים על ההווה, ללא זמן מדויק.\nמבנה: Have / Has + הפועל בצורה השלישית (V3).\nדוגמה: I have lived here for five years.",
        "grammar_q": "בחר את המשפט התקני והנכון ביותר באנגלית:",
        "grammar_options": ["She has gone to London.", "She have gone to London.", "She has went to London."],
        "grammar_correct": "She has gone to London.",
        "story_title": "The Journey to Mars 🚀",
        "story_text": "In the year 2046, Captain Sarah boarded the advanced Ares-5 spacecraft. Her lifelong dream was to accomplish what no human had ever done before: walking on Mars. After an independent journey of seven long months through dark space, the red planet finally appeared in the circular window.",
        "unseen_q": "How long did the journey to Mars take?",
        "unseen_options": ["Three weeks", "Seven months", "One year"],
        "unseen_correct": "Seven months",
        "video_id": "d5U7g_sZ09g",
        "exam_q": "איזו מילה פירושה 'נדיב'?",
        "exam_options": ["Generous", "Independent", "Influence"],
        "exam_correct": "Generous"
    }
}

# --- מסך כניסה / הרשמה ---
if not st.session_state.logged_in:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("🥇 פלטפורמת SmartEnglish Premium")
    st.subheader("ברוכים הבאים! אתר משחקי האנגלית הגדול והמתקדם ביותר.")
    
    with st.container(border=True):
        st.markdown("### 📝 כניסה מהירה לתלמיד:")
        name_input = st.text_input("מה השם שלך גיבור/ה?", placeholder="הקלידו שם כאן...")
        age_input = st.slider("בן/בת כמה את/ה? (כדי שנתאים לך את המשחקים)", 10, 15, 11)
        
        if st.button("🚀 כניסה לעולם המשחקים!", use_container_width=True):
            if name_input.strip() == "":
                st.error("חובה להקליד שם כדי שנוכל לשמור את כל הנקודות והשלבים שלך!")
            else:
                st.session_state.user_name = name_input
                st.session_state.user_age = age_input
                st.session_state.score = 0
                if age_input in [10, 11]: st.session_state.level = 1
                elif age_input in [12, 13]: st.session_state.level = 2
                else: st.session_state.level = 3
                st.session_state.logged_in = True
                save_progress()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- האפליקציה המרכזית (אחרי התחברות) ---
else:
    current_data = content_db[st.session_state.level]
    
    # הצגת הודעה מיוחדת במידה והיוזר נטען אוטומטית מקישור שמור
    if st.query_params.get("name") and "welcome_shown" not in st.session_state:
        st.toast(f"👋 ברוך הבא חזרה, {st.session_state.user_name}! כל ההתקדמות שלך נשמרה!", icon="💾")
        st.session_state.welcome_shown = True

    # --- סרגל כלים עליון (Dashboard) סופר מעוצב וקריא ---
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    c_user, c_scr, c_lvl, c_out = st.columns([3, 2, 2, 2])
    with c_user:
        st.markdown(f"👤 **שחקן פעיל:** <span style='font-size:22px; color:#2563eb;'><b>{st.session_state.user_name}</b></span>", unsafe_allow_html=True)
    with c_scr:
        st.markdown(f"⭐ **מדליות ונקודות:** <span style='font-size:22px; color:#16a34a;'><b>{st.session_state.score}</b></span>", unsafe_allow_html=True)
    with c_lvl:
        st.markdown(f"👑 **דרגה נוכחית:** <span style='font-size:22px; color:#b45309;'><b>שלב {st.session_state.level}</b></span>", unsafe_allow_html=True)
    with c_out:
        if st.button("יציאה והחלפת משתמש ↩️"):
            st.session_state.logged_in = False
            st.query_params.clear()
            st.rerun()
            
    # מד התקדמות ויזואלי לעליית שלב
    progress_val = min((st.session_state.score % 100) / 100.0, 1.0)
    st.progress(progress_val, text=f"התקדמות לעליית שלב הבא ({int(progress_val*100)}%)")
    st.markdown(f"💡 *טיפ: כדי לעלות שלב באופן אוטומטי צבור 100 נקודות או עבור בהצלחה את 'מבחן השלב' בלשונית האחרונה!*")
    st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)

    # בדיקת עליית שלב אוטומטית לפי ניקוד
    if st.session_state.score >= 100 and st.session_state.level == 1:
        st.session_state.level = 2
        st.balloons()
        st.success("💥 וואו! הגעת ל-100 נקודות ועלית אוטומטית לשלב 2!")
        save_progress()
    elif st.session_state.score >= 200 and st.session_state.level == 2:
        st.session_state.level = 3
        st.balloons()
        st.success("💥 מדהים! הגעת ל-200 נקודות ועלית אוטומטית לשלב 3 - שלב המאסטרים!")
        save_progress()

    # כותרת השלב
    st.markdown(f'<div class="rtl-container"><h2 style="text-align:center; color:#1e3a8a;">{current_data["title"]}</h2></div>', unsafe_allow_html=True)

    # --- טאבים (לשוניות) למשחקים ולמידה ---
    t_vocab, t_scramble, t_grammar, t_story, t_video, t_exam = st.tabs([
        "🃏 כרטיסיות מילים מדברות", 
        "🧩 משחק סדר האותיות", 
        "🎯 אתגר הדקדוק וההגייה", 
        "📖 סיפורים ואנסין קולי", 
        "🎬 סרטוני הסבר", 
        "🏁 מבחן עליית שלב"
    ])

    # 1. כרטיסיות מילים מורחבות
    with t_vocab:
        st.markdown('<div class="rtl-container"><h3>🃏 כרטיסיות מילים אינטראקטיביות</h3><p>לחצו על כפתור השמע כדי לשמוע את המילה, ופתחו את התיבה כדי לראות את התרגום והרמז!</p></div>', unsafe_allow_html=True)
        
        for item in current_data["vocab"]:
            with st.container(border=True):
                col_e, col_sp, col_h = st.columns([3, 2, 4])
                with col_e:
                    st.markdown(f"<div class='ltr-card' style='margin:0; padding:10px;'><b style='font-size:24px; color:#1e293b;'>{item['eng']}</b></div>", unsafe_allow_html=True)
                with col_sp:
                    speak_button(item['eng'], label="📢 Listen (אנגלית)")
                with col_h:
                    with st.expander("👁️ לחצו לחשיפת פירוש בעברית ורמז"):
                        st.markdown(f"<div class='rtl-container'><b>פירוש:</b> {item['heb']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='rtl-container'>💡 {item['hint']}</div>", unsafe_allow_html=True)
                        speak_button(item['heb'], lang="he-IL", label="🔊 השמע בעברית")

    # 2. משחק אותיות מבולבלות (Word Scramble)
    with t_scramble:
        st.markdown('<div class="rtl-container"><h3>🧩 משחק חילוץ אותיות ומרוץ זיכרון</h3>', unsafe_allow_html=True)
        target_w = current_data["scramble_word"]
        
        # ערבוב אותיות קבוע לכל שלב כדי שלא ישתנה בכל קליק
        if f"scrambled_letters_{st.session_state.level}" not in st.session_state:
            l_list = list(target_w)
            random.shuffle(l_list)
            st.session_state[f"scrambled_letters_{st.session_state.level}"] = "".join(l_list)
            
        st.markdown("#### סדרו את האותיות המבולבלות כדי להרכיב מילה נכונה:")
        st.markdown(f"<div class='ltr-card' style='text-align:center; font-size:36px; letter-spacing:8px; font-weight:bold; color:#d97706;'>{st.session_state[f'scrambled_letters_{st.session_state.level}']}</div>", unsafe_allow_html=True)
        
        # שימוש במערכת רמזים מובנית
        with st.expander("🔍 צריך רמז למשחק? לחצו כאן"):
            st.markdown(f"<div class='rtl-container'>💡 <b>רמז:</b> {current_data['scramble_hint']}</div>", unsafe_allow_html=True)
            
        u_guess = st.text_input("✍️ הקלידו את המילה שלכם באותיות גדולות (English):", key="scr_input").upper().strip()
        
        if st.button("🎮 בדקו אם צדקתי במשחק האותיות"):
            if u_guess == target_w:
                st.balloons()
                st.success("🎉 מדהים!!! הצלחתם לפצח את המילה המבולבלת!")
                add_score(25)
            else:
                st.error("❌ אופס, האותיות עדיין לא בסדר הנכון. נסו שוב או היעזרו ברמז למעלה!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. אתגר דקדוק ומעבדת דיבור מתוקנת
    with t_grammar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown(f"### 🎯 חוק חובה: {current_data['grammar_title']}")
        st.info(current_data['grammar_desc'])
        st.write("---")
        
        st.markdown("#### 🎲 משימת הדקדוק שלכם:")
        g_choice = st.radio(current_data['grammar_q'], current_data['grammar_options'])
        
        if st.button("📝 בדקו את תשובת הדקדוק שלי"):
            if g_choice == current_data['grammar_correct']:
                st.balloons()
                st.success("🤩 נכון מאוד! אתם מבינים את חוקי האנגלית מעולה!")
                add_score(20)
            else:
                st.error("😢 לא מדויק. קראו את חוק הדקדוק בתיבה הכחולה למעלה ונסו שוב!")
                
        st.write("---")
        st.markdown("### 🎤 מעבדת הגייה אינטראקטיבית עם המחשב")
        st.markdown("בואו נבדוק את המבטא שלכם! לחצו על המיקרופון ואמרו את המילה הבאה בקול רם:")
        speech_recognition_game(current_data["vocab"][0]["eng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. סיפור מקריא ואנסין
    with t_unseen:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown(f"### 📖 הסיפור האינטראקטיבי: {current_data['story_title']}")
        st.markdown("רוצים שהאתר יקריא לכם את כל הסיפור במבטא מושלם וברור? לחצו על הכפתור:")
        speak_button(current_data['story_text'], label="🔊 הפעל הקראת סיפור מלאה באנגלית")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # הצגת האנסין משמאל לימין בצורה נקייה וגדולה
        st.markdown(f'<div class="ltr-card" style="font-size:22px; line-height:1.8; color:#0f172a;">{current_data["story_text"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown("#### 🧠 מבחן הבנת הנקרא על הסיפור (Unseen):")
        u_choice = st.radio(current_data['unseen_q'], current_data['unseen_options'])
        
        if st.button("🔍 בדקו את תשובת הסיפור שלי"):
            if u_choice == current_data['unseen_correct']:
                st.snow()
                st.success("🎉 כל הכבוד! עניתם נכון על שאלת הבנת הנקרא!")
                add_score(20)
            else:
                st.error("❌ התשובה לא נכונה. הקשיבו לסיפור פעם נוספת ונסו שוב!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. וידאו
    with t_video:
        st.markdown('<div class="rtl-container"><h3>🎬 מרכז הווידאו הלימודי</h3><p>צפו בסרטון החינוכי כדי ללמוד ולתרגל אנגלית בכיף. מומלץ להפעיל כתוביות (CC) בנגן!</p></div>', unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={current_data['video_id']}")

    # 6. מבחן עליית שלב ותעודה סופית
    with t_exam:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown("### 🏁 המבחן הגדול לעליית שלב!")
        st.write("ענו נכון על השאלה המסכמת כדי לעלות מיד לשלב הבא במשחק ולקבל פרס גדול!")
        
        e_choice = st.radio(current_data['exam_q'], current_data['exam_options'])
        
        if st.button("🏆 הגש מבחן סיום שלב רשמי"):
            if e_choice == current_data['exam_correct']:
                st.balloons()
                st.snow()
                add_score(50)
                
                if st.session_state.level < 3:
                    st.session_state.level += 1
                    st.success(f"🥳 יששש! עברתם את המבחן! ברוכים הבאים לשלב {st.session_state.level} החדש!")
                else:
                    if "מאסטר אנגלית" not in st.session_state.achievements:
                        st.session_state.achievements.append("מאסטר אנגלית")
                    st.success("👑 מדהים!!! סיימתם את כל הרמות באתר והפכתם למאסטרים רשמיים באנגלית!")
                save_progress()
                st.rerun()
            else:
                st.error("😭 תשובה לא נכונה במבחן. עברו שוב על לשונית המילים והסיפורים ונסו שוב!")
                
        # הפקת תעודת הצטיינות חגיגית למי שמסיים את שלב 3
        if st.session_state.level == 3 and "מאסטר אנגלית" in st.session_state.achievements:
            st.write("---")
            st.markdown("### 📜 תעודת ההצטיינות האישית שלך המוכנה להדפסה!")
            cert_code = f"""
            <div style="border: 10px double #gold; background-color: #ffffff; padding: 30px; text-align: center; font-family: 'Heebo', sans-serif; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); direction: rtl; color:#1e293b;">
                <h1 style="color: #1e3a8a; margin: 0;">📜 תעודת הצטיינות באנגלית 📜</h1>
                <p style="font-size: 20px; color: #475569; margin-top: 15px;">כל הכבוד לתלמיד/ה המצטיין/ת</p>
                <h2 style="color: #b45309; font-size: 34px; margin: 10px 0;">{st.session_state.user_name}</h2>
                <p style="font-size: 18px; color: #475569;">אשר סיים/ה בהצלחה את כל השלבים, המשחקים, אתגרי ההגייה והאנסין באתר <b>SmartEnglish</b>!</p>
                <p style="font-size: 24px; font-weight: bold; color: #16a34a;">ניקוד סופי ענק: {st.session_state.score} נקודות! 🏆</p>
            </div>
            """
            components.html(cert_code, height=330)
            
        st.markdown('</div>', unsafe_allow_html=True)
