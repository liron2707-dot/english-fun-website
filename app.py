import streamlit as st
import streamlit.components.v1 as components
import random
import re

# הגדרות עמוד
st.set_page_config(page_title="SmartEnglish - המערכת החכמה", page_icon="🎓", layout="wide")

# --- פונקציה לבדיקת אותיות באנגלית בלבד ---
def is_only_english(text):
    # בודק שאין תווים בעברית
    return not bool(re.search(r'[א-ת]', text))

# --- שמירת נתונים ומשימות ---
if "user_name" not in st.session_state:
    st.session_state.user_name = st.query_params.get("name", "")
if "user_age" not in st.session_state:
    st.session_state.user_age = int(st.query_params.get("age", 11))
if "score" not in st.session_state:
    st.session_state.score = int(st.query_params.get("score", 0))
if "level" not in st.session_state:
    st.session_state.level = int(st.query_params.get("level", 1))

# ניהול משימות שהושלמו בשלב הנוכחי
default_tasks = {"vocab": False, "scramble": False, "grammar": False, "story": False, "video": False}
if "completed_tasks" not in st.session_state:
    saved_tasks = st.query_params.get("tasks", "")
    if saved_tasks:
        st.session_state.completed_tasks = {k: (k in saved_tasks.split(",")) for k in default_tasks.keys()}
    else:
        st.session_state.completed_tasks = default_tasks.copy()

if "achievements" not in st.session_state:
    st.session_state.achievements = st.query_params.get_all("ach")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True if st.session_state.user_name != "" else False

def save_progress():
    st.query_params["name"] = st.session_state.user_name
    st.query_params["age"] = str(st.session_state.user_age)
    st.query_params["score"] = str(st.session_state.score)
    st.query_params["level"] = str(st.session_state.level)
    # שמירת משימות שהושלמו (כדי שלא ימחקו ברענון)
    completed = [k for k, v in st.session_state.completed_tasks.items() if v]
    st.query_params["tasks"] = ",".join(completed)
    if st.session_state.achievements:
        st.query_params["ach"] = st.session_state.achievements

def add_score(amount):
    st.session_state.score += amount
    save_progress()
    st.toast(f"🏆 אלופים! זכיתם ב-{amount} נקודות!", icon="⭐")

def mark_task_complete(task_name):
    if not st.session_state.completed_tasks[task_name]:
        st.session_state.completed_tasks[task_name] = True
        add_score(10) # 10 נקודות על כל משימה קטנה
        st.success("✅ משימה הושלמה ונשמרה!")

# --- עיצוב ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Heebo', sans-serif; background-color: #f8fafc; color: #1e293b !important; }
    .rtl-container { direction: rtl; text-align: right; padding: 10px; }
    .ltr-card { direction: ltr; text-align: left; background-color: #ffffff; padding: 25px; border-radius: 16px; border: 3px solid #e2e8f0; border-left: 8px solid #3b82f6; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 15px; }
    h1, h2, h3 { font-weight: 900 !important; color: #1e3a8a !important; }
    .stButton>button { background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important; color: white !important; font-size: 18px !important; font-weight: bold !important; border-radius: 12px !important; padding: 10px 20px !important; border: none !important; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# --- פונקציות עזר קוליות ---
def speak_button(text, lang="en-US", label="🔊 השמע מילה"):
    html_code = f"""
    <button onclick="speak()" style="background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{label}</button>
    <script>
    function speak() {{
        var msg = new SpeechSynthesisUtterance({repr(text)});
        msg.lang = '{lang}'; msg.rate = 0.8;
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(html_code, height=45)

def speech_recognition_game(target_word):
    html_code = f"""
    <div style="text-align: center; font-family: system-ui; margin-top: 10px;">
        <button id="rec_btn" onclick="startDictation()" style="background: #ef4444; color: white; border: none; padding: 12px 24px; border-radius: 12px; cursor: pointer; font-size: 18px; font-weight: bold; width: 100%;">🎤 לחצו ואמרו באנגלית: "{target_word}"</button>
        <p id="result_text" style="font-size: 18px; font-weight: bold; margin-top: 12px; color: #475569;">לחצו על המיקרופון ודברו אל המחשב...</p>
    </div>
    <script>
    function startDictation() {{
        if (window.hasOwnProperty('webkitSpeechRecognition')) {{
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false; recognition.interimResults = false; recognition.lang = "en-US";
            var btn = document.getElementById('rec_btn');
            btn.style.background = "#22c55e"; btn.innerText = "🎧 האתר מקשיב לך עכשיו...";
            recognition.start();
            recognition.onresult = function(e) {{
                recognition.stop();
                var user_said = e.results[0][0].transcript.toLowerCase().trim();
                var target = "{target_word}".toLowerCase().trim();
                var res_p = document.getElementById('result_text');
                btn.style.background = "#ef4444"; btn.innerText = '🎤 נסו שוב';
                if(user_said.includes(target) || target.includes(user_said)) {{
                    res_p.innerHTML = "🍏 <span style='color:green; font-size:20px;'>מדהים! ("+user_said+")</span>";
                }} else {{
                    res_p.innerHTML = "🍎 <span style='color:red;'>שמענו: \\""+user_said+"\\". נסו שוב!</span>";
                }}
            }};
            recognition.onerror = function(e) {{ recognition.stop(); document.getElementById('rec_btn').style.background = "#ef4444"; document.getElementById('rec_btn').innerText = '🎤 שגיאה במיקרופון'; }}
        }} else {{ document.getElementById('result_text').innerText = "דפדפן לא תומך."; }}
    }}
    </script>
    """
    components.html(html_code, height=130)

# --- מסד הנתונים (מורחב עם שאלות וידאו ומשימות נוקשות) ---
content_db = {
    1: {
        "title": "שלב 1: צעדים ראשונים באנגלית 🌟",
        "vocab": [
            {"eng": "Apple", "heb": "תפוח", "hint": "פרי אדום מתוק"},
            {"eng": "Book", "heb": "ספר", "hint": "קוראים בו סיפורים"},
            {"eng": "Cat", "heb": "חתול", "hint": "חיה שאומרת מיאו"},
            {"eng": "Dog", "heb": "כלב", "hint": "חיה שאומרת הב הב"}
        ],
        "scramble_word": "BOOK",
        "scramble_hint": "משהו שקוראים בו",
        "grammar_title": "כינויי גוף - I, You, He, She",
        "grammar_desc": "• I = אני\n• You = אתה/את\n• He = הוא\n• She = היא",
        "grammar_q": "איך אומרים 'היא' באנגלית?",
        "grammar_options": ["I", "You", "She", "He"],
        "grammar_correct": "She",
        "story_title": "The Red Cat 🐱",
        "story_text": "Dan has a cat. The cat is red and big. The cat likes to sleep on the bed.",
        "unseen_q": "Where does the cat sleep?",
        "unseen_options": ["On the table", "On the bed", "In the tree"],
        "unseen_correct": "On the bed",
        "video_id": "L89cZYhNjWM", # סרטון מתאים לילדים
        "video_q": "על אילו חיות דיברו בשיר/בסרטון?",
        "video_options": ["פילים ואריות", "חיות חווה (פרה, כבשה)", "דגים בים"],
        "video_correct": "חיות חווה (פרה, כבשה)",
        "exam_q": "איזו מילה באנגלית מתארת חיה שאומרת 'מיאו'?",
        "exam_options": ["Apple", "Cat", "Dog"],
        "exam_correct": "Cat"
    },
    2: {
        "title": "שלב 2: יער הפעלים 🏃‍♂️",
        "vocab": [
            {"eng": "Run", "heb": "לרוץ", "hint": "ללכת מהר מאוד"},
            {"eng": "Jump", "heb": "לקפוץ", "hint": "להתנתק מהרצפה למעלה"},
            {"eng": "Play", "heb": "לשחק", "hint": "לעשות משהו כיפי"},
            {"eng": "Swim", "heb": "לשחות", "hint": "לנוע בתוך המים"}
        ],
        "scramble_word": "JUMP",
        "scramble_hint": "לקפוץ באוויר",
        "grammar_title": "פועל עזר To Be - ההווה",
        "grammar_desc": "I am, He is, She is, They are.",
        "grammar_q": "השלם: They ____ playing outside.",
        "grammar_options": ["am", "is", "are"],
        "grammar_correct": "are",
        "story_title": "Fun at the Park 🌳",
        "story_text": "Tom and Jerry go to the park. Tom likes to run. Jerry likes to jump high. They play all day and then go home.",
        "unseen_q": "What does Jerry like to do?",
        "unseen_options": ["Swim", "Jump high", "Sleep"],
        "unseen_correct": "Jump high",
        "video_id": "hzo9me2fdzg",
        "video_q": "איזה פועל הופיע הכי הרבה בסרטון?",
        "video_options": ["לרוץ (Run)", "לשיר (Sing)", "לאכול (Eat)"],
        "video_correct": "לרוץ (Run)",
        "exam_q": "איך כותבים באנגלית 'לשחות'?",
        "exam_options": ["Play", "Swim", "Run"],
        "exam_correct": "Swim"
    },
    3: {
        "title": "שלב 3: עיר הזמנים וההווה הממושך ⏳",
        "vocab": [
            {"eng": "Watching", "heb": "צופה (עכשיו)", "hint": "לראות משהו שקורה כרגע"},
            {"eng": "Eating", "heb": "אוכל (עכשיו)", "hint": "להכניס אוכל לפה ברגע זה"},
            {"eng": "Writing", "heb": "כותב (עכשיו)", "hint": "להשתמש בעיפרון עכשיו"},
            {"eng": "Listening", "heb": "מקשיב (עכשיו)", "hint": "לשמוע משהו כרגע"}
        ],
        "scramble_word": "EATING",
        "scramble_hint": "מה שאנחנו עושים כשאנחנו רעבים",
        "grammar_title": "הווה ממושך - Present Progressive",
        "grammar_desc": "לפעולות שקורות ממש עכשיו! נוסיף ing לפועל. דוגמה: I am reading.",
        "grammar_q": "איך נכון לומר 'הוא ישן עכשיו'?",
        "grammar_options": ["He is sleep", "He is sleeping", "He sleeping"],
        "grammar_correct": "He is sleeping",
        "story_title": "A Busy Morning ☀️",
        "story_text": "It is morning. Mom is drinking coffee. Dad is reading the newspaper. The kids are eating breakfast. Everyone is very busy today.",
        "unseen_q": "What are the kids doing?",
        "unseen_options": ["Drinking coffee", "Eating breakfast", "Reading"],
        "unseen_correct": "Eating breakfast",
        "video_id": "dNXAq2N7d50",
        "video_q": "באיזה זמן השתמשו כדי לתאר מה הדמויות עושות בסרטון?",
        "video_options": ["עבר פשוט", "הווה ממושך (עם ing)", "עתיד"],
        "video_correct": "הווה ממושך (עם ing)",
        "exam_q": "איזו מילה אומרת 'מקשיב עכשיו'?",
        "exam_options": ["Writing", "Eating", "Listening"],
        "exam_correct": "Listening"
    },
     4: {
        "title": "שלב 4: הרפתקת העבר הפשוט 🦖",
        "vocab": [
            {"eng": "Walked", "heb": "הלך (בעבר)", "hint": "פועל רגיל עם ed"},
            {"eng": "Saw", "heb": "ראה (בעבר)", "hint": "העבר של המילה See"},
            {"eng": "Went", "heb": "הלך/נסע (בעבר)", "hint": "העבר של המילה Go"},
            {"eng": "Ate", "heb": "אכל (בעבר)", "hint": "העבר של Eat"}
        ],
        "scramble_word": "WALKED",
        "scramble_hint": "הלך בעבר",
        "grammar_title": "Past Simple - פעלים יוצאי דופן",
        "grammar_desc": "בעבר, רוב הפעלים מקבלים ED. אבל יש פעלים שמשתנים לגמרי! Go הופך ל- Went.",
        "grammar_q": "מה העבר של הפועל SEE (לראות)?",
        "grammar_options": ["Seed", "Saw", "Seeing"],
        "grammar_correct": "Saw",
        "story_title": "The Dinosaur Museum 🏛️",
        "story_text": "Yesterday, we went to the museum. We saw a big dinosaur skeleton. After that, we ate pizza at the cafe. It was a great day.",
        "unseen_q": "What did they eat after the museum?",
        "unseen_options": ["Apples", "Pizza", "Cake"],
        "unseen_correct": "Pizza",
        "video_id": "z1k8D4xVwG8",
        "video_q": "על איזה זמן באנגלית הוסבר בסרטון?",
        "video_options": ["עתיד", "עבר", "הווה"],
        "video_correct": "עבר",
        "exam_q": "איזו מילה היא פועל בעבר?",
        "exam_options": ["Eating", "Went", "Jump"],
        "exam_correct": "Went"
    }
}

# --- מסך כניסה ---
if not st.session_state.logged_in:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("🥇 פלטפורמת SmartEnglish Premium")
    st.subheader("ברוכים הבאים למערכת הלמידה המקיפה ביותר!")
    
    with st.container(border=True):
        st.markdown("### 📝 כניסה מאובטחת לתלמיד:")
        name_input = st.text_input("מה השם שלך גיבור/ה?", placeholder="הקלידו שם כאן...")
        age_input = st.slider("בן/בת כמה את/ה?", 7, 15, 10)
        
        if st.button("🚀 כניסה למערכת!", use_container_width=True):
            if name_input.strip() == "":
                st.error("חובה להקליד שם כדי שנוכל לשמור את ההתקדמות שלך!")
            else:
                st.session_state.user_name = name_input
                st.session_state.user_age = age_input
                st.session_state.logged_in = True
                save_progress()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- האפליקציה המרכזית ---
else:
    # טיפול בסיום כל השלבים
    if st.session_state.level > max(content_db.keys()):
        st.balloons()
        st.markdown('<div class="rtl-container"><h1 style="color:green;">🎉 סיימת את כל השלבים באתר! את/ה מאסטר אנגלית!</h1></div>', unsafe_allow_html=True)
        st.stop()

    current_data = content_db[st.session_state.level]

    # --- סרגל עליון וסטטוס משימות ---
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    c_user, c_scr, c_lvl, c_out = st.columns([3, 2, 2, 2])
    with c_user:
        st.markdown(f"👤 שחקן: <span style='font-size:20px; color:#2563eb;'><b>{st.session_state.user_name}</b></span>", unsafe_allow_html=True)
    with c_scr:
        st.markdown(f"⭐ ניקוד: <span style='font-size:20px; color:#16a34a;'><b>{st.session_state.score}</b></span>", unsafe_allow_html=True)
    with c_lvl:
        st.markdown(f"👑 שלב: <span style='font-size:20px; color:#b45309;'><b>{st.session_state.level}</b></span>", unsafe_allow_html=True)
    with c_out:
        if st.button("יציאה ↩️"):
            st.session_state.logged_in = False
            st.query_params.clear()
            st.session_state.completed_tasks = default_tasks.copy()
            st.rerun()
            
    st.markdown("### 📋 צ'ק-ליסט לשלב הנוכחי (חובה לסיים הכל כדי לגשת למבחן!):")
    cols = st.columns(5)
    tasks_ui = [
        ("מילים", "vocab"), ("איות", "scramble"), 
        ("דקדוק", "grammar"), ("קריאה", "story"), ("וידאו", "video")
    ]
    for i, (label, key) in enumerate(tasks_ui):
        status = "✅ הושלם" if st.session_state.completed_tasks[key] else "⏳ טרם"
        cols[i].markdown(f"<div style='text-align:center; padding:5px; background-color:{'#dcfce3' if st.session_state.completed_tasks[key] else '#f1f5f9'}; border-radius:8px;'><b>{label}</b><br>{status}</div>", unsafe_allow_html=True)
    st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="rtl-container"><h2 style="text-align:center; color:#1e3a8a;">{current_data["title"]}</h2></div>', unsafe_allow_html=True)

    # טאבים שונו במדויק
    t_vocab, t_scramble, t_grammar, t_story, t_video, t_exam = st.tabs([
        "🃏 אוצר מילים", "🧩 משחק איות", "🎯 דקדוק ודיבור", "📖 אנסין קריאה", "🎬 וידאו ושאלות", "🏁 מבחן נעול"
    ])

    # 1. מילים
    with t_vocab:
        st.markdown('<div class="rtl-container"><h3>🃏 מילים חדשות</h3><p>הקשיבו ולמדו את המילים. לחצו על הכפתור למטה כשתהיו מוכנים!</p></div>', unsafe_allow_html=True)
        for item in current_data["vocab"]:
            with st.container(border=True):
                col_e, col_sp, col_h = st.columns([3, 2, 4])
                with col_e:
                    st.markdown(f"<div class='ltr-card' style='margin:0; padding:10px;'><b>{item['eng']}</b></div>", unsafe_allow_html=True)
                with col_sp: speak_button(item['eng'], label="📢 אנגלית")
                with col_h: st.markdown(f"<div class='rtl-container'><b>{item['heb']}</b> - {item['hint']}</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        if not st.session_state.completed_tasks["vocab"]:
            if st.button("✅ סיימתי ללמוד את המילים! בעל פה!"):
                mark_task_complete("vocab")
                st.rerun()
        else:
            st.success("✅ משימת המילים הושלמה!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. איות ומרוץ אותיות (חסימת עברית)
    with t_scramble:
        st.markdown('<div class="rtl-container"><h3>🧩 מרוץ כתיבה ואיות</h3>', unsafe_allow_html=True)
        target_w = current_data["scramble_word"]
        if f"scrambled_{st.session_state.level}" not in st.session_state:
            l_list = list(target_w)
            random.shuffle(l_list)
            st.session_state[f"scrambled_{st.session_state.level}"] = "".join(l_list)
            
        st.markdown(f"<div class='ltr-card' style='text-align:center; font-size:36px; letter-spacing:8px;'>{st.session_state[f'scrambled_{st.session_state.level}']}</div>", unsafe_allow_html=True)
        st.markdown(f"💡 <b>רמז:</b> {current_data['scramble_hint']}", unsafe_allow_html=True)
        
        u_guess = st.text_input("✍️ הקלידו באנגלית בלבד:", key="scr_input").upper().strip()
        
        if st.button("🎮 בדיקת איות"):
            if not is_only_english(u_guess):
                st.error("❌ שגיאה! עליך להקליד את התשובה באותיות באנגלית בלבד!")
            elif u_guess == target_w:
                mark_task_complete("scramble")
                st.balloons()
            else:
                st.error("❌ טעות. נסו שוב!")
                
        if st.session_state.completed_tasks["scramble"]:
            st.success("✅ משימת האיות הושלמה!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. דקדוק ודיבור
    with t_grammar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown(f"### 🎯 חוק: {current_data['grammar_title']}")
        st.info(current_data['grammar_desc'])
        g_choice = st.radio(current_data['grammar_q'], current_data['grammar_options'])
        
        if st.button("📝 בדוק דקדוק"):
            if g_choice == current_data['grammar_correct']:
                mark_task_complete("grammar")
            else:
                st.error("❌ לא נכון, קראו שוב את החוק!")
                
        if st.session_state.completed_tasks["grammar"]:
            st.success("✅ משימת הדקדוק הושלמה!")
            
        st.write("---")
        st.markdown("### 🎤 מעבדת דיבור (בונוס חובה לתרגול)")
        speech_recognition_game(current_data["vocab"][0]["eng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. אנסין
    with t_story: # <- כאן השגיאה שלך תוקנה (היה t_unseen במקום t_story)
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown(f"### 📖 קריאה והבנה: {current_data['story_title']}")
        speak_button(current_data['story_text'], label="🔊 הקרא לי")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="ltr-card" style="font-size:22px;">{current_data["story_text"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        u_choice = st.radio(current_data['unseen_q'], current_data['unseen_options'])
        if st.button("🔍 בדוק תשובה לסיפור"):
            if u_choice == current_data['unseen_correct']:
                mark_task_complete("story")
            else:
                st.error("❌ טעות, קראו שוב את הסיפור.")
                
        if st.session_state.completed_tasks["story"]:
            st.success("✅ משימת הקריאה הושלמה!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. וידאו ושאלות
    with t_video:
        st.markdown('<div class="rtl-container"><h3>🎬 צפייה והבנה</h3></div>', unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={current_data['video_id']}")
        
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        v_choice = st.radio(current_data['video_q'], current_data['video_options'])
        if st.button("🎥 בדוק את שאלת הווידאו"):
            if v_choice == current_data['video_correct']:
                mark_task_complete("video")
            else:
                st.error("❌ טעות. נסו לצפות שוב ולהקשיב היטב!")
                
        if st.session_state.completed_tasks["video"]:
            st.success("✅ משימת הווידאו הושלמה!")
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. מבחן סיום נעול
    with t_exam:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        
        # בדיקה האם כל המשימות הושלמו (ה"מנעול")
        all_completed = all(st.session_state.completed_tasks.values())
        
        if not all_completed:
            st.error("🔒 המבחן עדיין נעול! עליך להשלים את כל המשימות בכל הלשוניות הקודמות (חפשו איפה חסר לכם וי ירוק בצ'ק-ליסט למעלה) כדי לגשת למבחן.")
        else:
            st.success("🔓 כל הכבוד! פתחת את המבחן הגדול. ענה נכון ותעבור לשלב הבא!")
            e_choice = st.radio(current_data['exam_q'], current_data['exam_options'])
            
            if st.button("🏆 הגש מבחן סיום"):
                if e_choice == current_data['exam_correct']:
                    st.balloons()
                    add_score(50)
                    st.success("🎉 מדהים! עברתם את השלב!!!")
                    
                    # מעבר שלב אוטומטי ואיפוס משימות!
                    st.session_state.level += 1
                    st.session_state.completed_tasks = default_tasks.copy()
                    save_progress()
                    st.rerun() # טעינה מחדש של הדף עם השלב החדש
                else:
                    st.error("😭 התשובה שגויה. נסו שוב!")
        st.markdown('</div>', unsafe_allow_html=True)
