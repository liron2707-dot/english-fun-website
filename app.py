import streamlit as st
import streamlit.components.v1 as components
import random

# הגדרת עמוד בסיסית
st.set_page_config(page_title="SmartEnglish Premium 🚀", page_icon="👑", layout="centered")

# --- ניהול זיכרון המשתמש ושמירה ב-URL (Query Params) ---
if "user_name" not in st.session_state:
    st.session_state.user_name = st.query_params.get("name", "")
if "user_age" not in st.session_state:
    try: st.session_state.user_age = int(st.query_params.get("age", 10))
    except: st.session_state.user_age = 10
if "score" not in st.session_state:
    try: st.session_state.score = int(st.query_params.get("score", 0))
    except: st.session_state.score = 0
if "level" not in st.session_state:
    try: st.session_state.level = int(st.query_params.get("level", 1))
    except: st.session_state.level = 1
if "theme" not in st.session_state:
    st.session_state.theme = "🚀 חלל עמוק (Deep Space)"
if "achievements" not in st.session_state:
    st.session_state.achievements = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True if st.session_state.user_name != "" else False

def save_progress():
    st.query_params["name"] = st.session_state.user_name
    st.query_params["age"] = st.session_state.user_age
    st.query_params["score"] = st.session_state.score
    st.query_params["level"] = st.session_state.level

def add_achievement(name, icon):
    if name not in st.session_state.achievements:
        st.session_state.achievements.append(name)
        st.toast(f"🏆 הישג חדש נפתח: {icon} {name}!", icon="🎉")

# --- מנוע הקראה קולית (TTS) ---
def speak_button(text, lang="en-US", label="🔊 השמע"):
    html_code = f"""
    <button onclick="speak()" style="background: linear-gradient(135deg, #0ea5e9, #2563eb); color: white; border: none; padding: 8px 16px; border-radius: 50px; cursor: pointer; font-family: system-ui; font-size: 14px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; margin-bottom: 5px;">{label}</button>
    <script>
    function speak() {{
        var msg = new SpeechSynthesisUtterance({repr(text)});
        msg.lang = '{lang}'; msg.rate = 0.85; window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(html_code, height=45)

# --- מנוע זיהוי דיבור והגייה (Speech Recognition) ---
def speech_recognition_game(target_word):
    html_code = f"""
    <div style="text-align: center; font-family: system-ui; direction: ltr;">
        <button id="rec_btn" onclick="startDictation()" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; border: none; padding: 12px 24px; border-radius: 50px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">🎤 לחץ ואמור: "{target_word}"</button>
        <p id="result_text" style="font-size: 18px; font-weight: bold; margin-top: 15px; color: #475569;">לחץ על המיקרופון ודבר...</p>
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
            btn.innerText = "🎧 מקשיב לך...";
            
            recognition.start();
            
            recognition.onresult = function(e) {{
                recognition.stop();
                var user_said = e.results[0][0].transcript.toLowerCase().trim();
                var target = "{target_word.lower().trim()}";
                var res_p = document.getElementById('result_text');
                
                btn.style.background = "linear-gradient(135deg, #ef4444, #dc2626)";
                btn.innerText = '🎤 נסה שוב';
                
                if(user_said.includes(target) || target.includes(user_said)) {{
                    res_p.innerHTML = "🟢 <span style='color:green;'>מדהים! הגייה מושלמת! ("+user_said+")</span>";
                }} else {{
                    res_p.innerHTML = "🔴 <span style='color:red;'>שמעתי: \\""+user_said+"\\". נסה שוב במבטא ברור יותר!</span>";
                }}
            }};
            recognition.onerror = function(e) {{
                recognition.stop();
                document.getElementById('rec_btn').style.background = "linear-gradient(135deg, #ef4444, #dc2626)";
                document.getElementById('rec_btn').innerText = '🎤 שגיאה, נסה שוב';
            }}
        }} else {{
            document.getElementById('result_text').innerText = "הדפדפן שלך לא תומך בזיהוי קולי. מומלץ להשתמש ב-Google Chrome.";
        }}
    }}
    </script>
    """
    components.html(html_code, height=130)

# --- בחירת ערכות נושא (Themes CSS) ---
themes = {
    "🚀 חלל עמוק (Deep Space)": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)",
    "🍬 ממלכת הסוכריות (Candy Kingdom)": "linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%)",
    "🏆 ליגת האלופות (Champions League)": "linear-gradient(135deg, #022c22 0%, #064e3b 100%)"
}
bg_gradient = themes[st.session_state.theme]
text_color = "#ffffff" if st.session_state.theme != "🍬 ממלכת הסוכריות (Candy Kingdom)" else "#1e293b"
card_bg = "rgba(255,255,255,0.1)" if st.session_state.theme != "🍬 ממלכת הסוכריות (Candy Kingdom)" else "#ffffff"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Heebo', sans-serif;
        background: {bg_gradient};
        color: {text_color} !important;
    }}
    .rtl-box {{ direction: rtl; text-align: right; }}
    .ltr-box {{ 
        direction: ltr; text-align: left; font-size: 20px; 
        background-color: {card_bg}; padding: 20px; 
        border-radius: 15px; border-left: 6px solid #3b82f6; color: {text_color};
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    h1, h2, h3, h4, span, p, label {{ color: {text_color} !important; }}
    .stTabs [data-baseweb="tab"] {{ color: {text_color} !important; font-weight: bold; font-size: 16px; }}
    </style>
""", unsafe_allow_html=True)

# --- מאגר מידע מקיף מובנה לכל הרמות ---
content_db = {
    1: {
        "title": "עולם היסודות 🌟 (גילאי 10-11)",
        "vocab": [("Apple", "תפוח 🍎", "A-P-P-L-E"), ("Summer", "קיץ ☀️", "S-U-M-M-E-R"), ("Friend", "חבר 🤝", "F-R-I-E-N-D"), ("School", "בית ספר 🏫", "S-C-H-O-O-L")],
        "scramble_word": "FRIEND", "scramble_hint": "מישהו שאתה אוהב לשחק איתו בהפסקה",
        "grammar_title": "חוק ה- Am, Is, Are",
        "grammar_text": "I ➔ Am | He/She/It ➔ Is | We/You/They ➔ Are",
        "grammar_q": "בחר את המילה הנכונה: 'We ____ learning English right now!'",
        "grammar_options": ["am", "is", "are"], "grammar_correct": "are",
        "story_title": "The Happy Puppy 🐶",
        "story_text": "Max is a small brown puppy. He lives in a big green yard. Every morning, Max runs after yellow butterflies. He is very fast, but he never catches them. At night, he sleeps next to his best friend, Leo.",
        "unseen_q": "What color are the butterflies Max runs after?",
        "unseen_options": ["Brown", "Green", "Yellow"], "unseen_correct": "Yellow",
        "video_id": "8wXG7IAnHdQ",
        "exam_q": "איך אומרים 'קיץ' באנגלית?",
        "exam_options": ["Winter", "Summer", "Spring"], "exam_correct": "Summer"
    },
    2: {
        "title": "יער ההרפתקאות 🗺️ (גילאי 12-13)",
        "vocab": [("Adventure", "הרפתקה 🗺️", "A-D-V-E-N-T-U-R-E"), ("Challenge", "אתגר 🎯", "C-H-A-L-L-E-N-G-E"), ("Discover", "לגלות 🔍", "D-I-S-C-O-V-E-R"), ("Protect", "להגן 🛡️", "P-R-O-T-E-C-T")],
        "scramble_word": "DISCOVER", "scramble_hint": "למצוא משהו חדש שלא הכרנו קודם",
        "grammar_title": "חוק ה- Past Simple (עבר פשוט)",
        "grammar_text": "לפעלים רגילים נוסיף ed בסוף (Walk ➔ Walked). לפעלים מיוחדים הצורה משתנה (Go ➔ Went).",
        "grammar_q": "בחר את הצורה הנכונה לעבר: 'Yesterday, I ____ a beautiful movie.'",
        "grammar_options": ["watch", "watched", "watching"], "grammar_correct": "watched",
        "story_title": "The Secret Map 🗺️",
        "story_text": "Oliver found an old, dusty book in his grandfather's attic. When he opened it, a secret map dropped onto the floor. The map showed a path leading to a hidden treasure near the blue river. Oliver decided to start his journey tomorrow.",
        "unseen_q": "Where did Oliver find the old book?",
        "unseen_options": ["In the school library", "In his grandfather's attic", "Near the blue river"], "unseen_correct": "In his grandfather's attic",
        "video_id": "maM9gNfskS4",
        "exam_q": "מה הפירוש של Challenge?",
        "exam_options": ["הרפתקה", "אתגר", "פתרון"], "exam_correct": "אתגר"
    },
    3: {
        "title": "מצודת המאסטרים 👑 (גילאי 14-15)",
        "vocab": [("Accomplish", "להשיג/להשלים 🏆", "A-C-C-O-M-P-L-I-S-H"), ("Independent", "עצמאי 🗽", "I-N-D-E-P-E-N-D-E-N-T"), ("Generous", "נדיב 🤝", "G-E-N-E-R-O-U-S"), ("Influence", "להשפעה 🌊", "I-N-F-L-U-E-N-C-E")],
        "scramble_word": "GENEROUS", "scramble_hint": "אדם שאוהב לתת ולתרום לאחרים",
        "grammar_title": "חוק ה- Present Perfect (הווה מושלם)",
        "grammar_text": "מבנה: Have/Has + פועל בצורה שלישית (V3). משמש לפעולה מהעבר שרלוונטית לעכשיו.",
        "grammar_q": "השלם את המשפט: 'They ____ already finished their project.'",
        "grammar_options": ["has", "have", "are"], "grammar_correct": "have",
        "story_title": "The Quantum Computer 💻",
        "story_text": "Dr. Sophia has successfully developed the world's first independent quantum computer. This incredible machine can solve global problems in seconds. Sophia believes her creation will have a positive influence on science and help accomplish a cleaner planet.",
        "unseen_q": "What kind of computer did Dr. Sophia develop?",
        "unseen_options": ["A gaming computer", "A quantum computer", "A social network"], "unseen_correct": "A quantum computer",
        "video_id": "d5U7g_sZ09g",
        "exam_q": "איזו מילה פירושה 'עצמאי'?",
        "exam_options": ["Independent", "Influence", "Accomplish"], "exam_correct": "Independent"
    }
}

# --- מסך הרשמה וכניסה ---
if not st.session_state.logged_in:
    st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
    st.title("🥇 SmartEnglish Premium Edition")
    st.subheader("ברוכים הבאים לפלטפורמת המשחקים המתקדמת ביותר ללימוד אנגלית!")
    
    with st.container(border=True):
        name_input = st.text_input("📝 מה השם שלך גיבור/ה?", placeholder="הקלד שם פה...")
        age_input = st.slider("🎂 גיל (להתאמת רמת המשחקים)", 10, 15, 11)
        
        if st.button("🚀 כניסה לעולם המשחקים!", use_container_width=True):
            if name_input.strip() == "":
                st.error("חובה לכתוב שם כדי שנוכל לשמור את הגביעים והניקוד שלך!")
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

# --- האפליקציה הראשית ---
else:
    current_data = content_db[st.session_state.level]
    
    # סרגל כלים עליון ומחליף עיצובים
    st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
    col_user, col_scr, col_lvl, col_th = st.columns([2, 1.5, 1.5, 2])
    with col_user: st.markdown(f"👤 **שחקן:** {st.session_state.user_name}")
    with col_scr: st.markdown(f"⭐ **ניקוד:** `{st.session_state.score}`")
    with col_lvl: st.markdown(f"👑 **רמה:** `{st.session_state.level}`")
    with col_th:
        st.session_state.theme = st.selectbox("🎨 עיצוב האתר", list(themes.keys()), index=list(themes.keys()).index(st.session_state.theme))
        
    st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)

    # לשוניות האתר המרכזיות
    tab_vocab, tab_games, tab_grammar, tab_unseen, tab_video, tab_exam = st.tabs([
        "🃏 כרטיסיות מילים", "🧩 משחק אותיות", "🎯 אתגר הדקדוק", "📖 סיפור מקריא", "🎬 וידאו", "🏁 מבחן שלב"
    ])

    # 1. כרטיסיות מילים אינטראקטיביות
    with tab_vocab:
        st.markdown('<div class="rtl-box"><h3>💡 מילון הכרטיסיות המדבר</h3><p>לחצו על הרמקול כדי לשמוע, ופתחו את הכרטיסייה כדי לראות את התרגום!</p></div>', unsafe_allow_html=True)
        for eng, heb, spell in current_data["vocab"]:
            with st.container(border=True):
                c_e, c_sp, c_h = st.columns([2, 1, 2])
                with c_e:
                    st.markdown(f"<h3 style='margin:0;'>{eng}</h3>", unsafe_allow_html=True)
                    st.caption(f"איוש: {spell}")
                with c_sp:
                    speak_button(eng, label="📢")
                with c_h:
                    with st.expander("👁️ לחץ לחשיפת התרגום"):
                        st.markdown(f"<h4 style='text-align:right; margin:0;'>{heb}</h4>", unsafe_allow_html=True)
                        speak_button(heb, lang="he-IL", label="🔊 עברית")

    # 2. משחק חילוץ אותיות (Word Scramble)
    with tab_games:
        st.markdown('<div class="rtl-box"><h3>🧩 משחק מרוץ האותיות (Word Scramble)</h3>', unsafe_allow_html=True)
        word_to_scramble = current_data["scramble_word"]
        
        # בלגון האותיות
        if f"scrambled_{st.session_state.level}" not in st.session_state:
            letter_list = list(word_to_scramble)
            random.shuffle(letter_list)
            st.session_state[f"scrambled_{st.session_state.level}"] = "".join(letter_list)
            
        st.markdown(f"#### סדר את האותיות הבאות כדי ליצור מילה תקינה:")
        st.markdown(f"<div class='ltr-box' style='text-align:center; font-size:32px; letter-spacing: 10px; font-weight:bold; color:#f97316;'>{st.session_state[f'scrambled_{st.session_state.level}']}</div>", unsafe_allow_html=True)
        st.markdown(f"💡 **רמז בעברית:** {current_data['scramble_hint']}")
        
        user_guess = st.text_input("✍️ הקלד את המילה המסודרת שלך באנגלית:", key="scramble_guess").upper().strip()
        if st.button("🎮 בדוק את המילה שלי"):
            if user_guess == word_to_scramble:
                st.balloons()
                st.success("🏆 מדהים! פיצחת את המילה! זכית ב-25 נקודות!")
                st.session_state.score += 25
                add_achievement("מאסטר פאזלים", "🧩")
                save_progress()
            else:
                st.error("❌ אופס, האותיות לא בסדר הנכון. נסה שוב!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. אתגר הדקדוק ומעבדת הדיבור
    with tab_grammar:
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown(f"### 🎯 חוק דקדוק: {current_data['grammar_title']}")
        st.info(current_data['grammar_text'])
        
        st.markdown("#### ❓ בחן את עצמך:")
        g_ans = st.radio(current_data['grammar_q'], current_data['grammar_options'])
        if st.button("בצע בדיקת דקדוק"):
            if g_ans == current_data['grammar_correct']:
                st.balloons()
                st.success("כל הכבוד! תשובה נכונה. +15 נקודות!")
                st.session_state.score += 15
                save_progress()
            else:
                st.error("התשובה לא נכונה, קרא את הכלל הכחול למעלה שוב!")
                
        st.write("---")
        st.markdown("### 🎤 מעבדת הגייה חיווה עם בינה מלאכותית")
        st.markdown("לחצו על המיקרופון, ואמרו את המילה הבאה בקול רם כדי לבדוק אם המחשב מבין אתכם:")
        speech_recognition_game(current_data["vocab"][0][0])
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. סיפור מקריא ואנסין אינטראקטיבי
    with tab_unseen:
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown(f"### 📖 סיפור השלב: {current_data['story_title']}")
        st.write("לחצו כדי שהאתר יקריא לכם את כל הסיפור בקול רם:")
        speak_button(current_data['story_text'], label="🔊 הפעל הקראת סיפור מלאה (Play Audio Story)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="ltr-box">{current_data["story_text"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown("#### 🧠 משימת הבנת הנקרא:")
        u_ans = st.radio(current_data['unseen_q'], current_data['unseen_options'])
        if st.button("שלח תשובת אנסין"):
            if u_ans == current_data['unseen_correct']:
                st.snow()
                st.success("מצוין! הבנתם את הסיפור בצורה מושלמת. +20 נקודות!")
                st.session_state.score += 20
                add_achievement("חוקר סיפורים", "📖")
                save_progress()
            else:
                st.error("❌ לא מדויק, כדאי להאזין לסיפור שוב פעם.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. סרטוני יוטיוב
    with tab_video:
        st.markdown('<div class="rtl-box"><h3>🎬 מרכז הווידאו המוזיקלי</h3><p>צפו בסרטון והפעילו כתוביות כדי לשפר את השמיעה שלכם באנגלית!</p></div>', unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={current_data['video_id']}")

    # 6. מבחן עליית שלב ותעודה
    with tab_exam:
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown("### 🏁 המבחן המסכם לעליית שלב")
        st.write("ענו נכון כדי לפתוח את השלב הבא או לסיים את המשחק בהצטיינות!")
        
        e_ans = st.radio(current_data['exam_q'], current_data['exam_options'])
        if st.button("🏆 הגש מבחן סופי"):
            if e_ans == current_data['exam_correct']:
                st.balloons()
                st.snow()
                st.session_state.score += 50
                
                if st.session_state.level < 3:
                    st.session_state.level += 1
                    st.success(f"💥 מזל טוב!!! עליתם לרמה {st.session_state.level}! שלבים חדשים נפתחו עבורכם!")
                else:
                    add_achievement("מאסטר אנגלית מוחלט", "👑")
                    st.success("👑 מדהים!!! השלמתם את כל השלבים באתר!")
                save_progress()
                st.rerun()
            else:
                st.error("❌ אווץ', טעות במבחן. חזרו על המילים והכרטיסיות ונסו שנית!")
        
        # תצוגת הישגים וגביעים
        if st.session_state.achievements:
            st.write("---")
            st.markdown("### 🏆 חדר הגביעים שלך:")
            cols = st.columns(len(st.session_state.achievements))
            for i, ach in enumerate(st.session_state.achievements):
                cols[i].button(f"🏅 {ach}", disabled=True, key=f"ach_{i}")
                
        # הפקת תעודה בסיום רמה 3
        if st.session_state.level == 3 and "מאסטר אנגלית מוחלט" in st.session_state.achievements:
            st.write("---")
            st.markdown("### 📜 תעודת ההצטיינות הרשמית שלך!")
            cert_html = f"""
            <div style="border: 10px double #gold; background-color: #f8fafc; padding: 30px; text-align: center; font-family: 'Heebo', sans-serif; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); direction: rtl;">
                <h1 style="color: #1e3a8a; margin: 0;">📜 תעודת מאסטר באנגלית 📜</h1>
                <p style="font-size: 20px; color: #475569; margin-top: 15px;">כל הכבוד לתלמיד/ה המצטיין/ת</p>
                <h2 style="color: #b45309; font-size: 32px; margin: 10px 0;">{st.session_state.user_name}</h2>
                <p style="font-size: 18px; color: #475569;">אשר סיים/ה בהצלחה את כל הרמות, המשחקים ואתגרי הדיבור באתר <b>SmartEnglish</b>!</p>
                <p style="font-size: 24px; font-weight: bold; color: #16a34a;">ניקוד סופי מנצח: {st.session_state.score} נקודות! 🏆</p>
            </div>
            """
            st.components.v1.html(cert_html, height=320)
            
        st.markdown('</div>', unsafe_allow_html=True)
