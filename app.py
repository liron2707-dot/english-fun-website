import streamlit as st
import random
import time
import streamlit.components.v1 as components

# הגדרות עמוד (חובה להיות שורה ראשונה)
st.set_page_config(page_title="SmartEnglish Pro", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- CSS מתקדם - פונטים ענקיים, יישור לימין ואנימציות ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Heebo', sans-serif; 
        background: #f8fafc; 
        color: #0f172a !important; 
    }
    
    .rtl-container { direction: rtl; text-align: right; }
    .ltr-container { direction: ltr; text-align: left; }
    
    h1 { font-size: 3.5rem !important; color: #1e3a8a !important; font-weight: 900 !important; text-shadow: 1px 1px 2px #cbd5e1; }
    h2 { font-size: 2.5rem !important; color: #2563eb !important; font-weight: 800 !important; }
    h3 { font-size: 2rem !important; color: #334155 !important; }
    p, span, div { font-size: 1.3rem; }
    
    .big-card { 
        background: white; padding: 40px; border-radius: 20px; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-bottom: 25px; border: 2px solid #e2e8f0;
    }
    
    /* עיצוב כפתורי תשובות - הופך אותם למשחק */
    .stButton>button { 
        background: white !important; 
        color: #1e40af !important; 
        font-size: 24px !important; 
        font-weight: bold !important; 
        border-radius: 16px !important; 
        padding: 20px !important; 
        border: 3px solid #bfdbfe !important; 
        width: 100%; transition: 0.2s; 
    }
    .stButton>button:hover { 
        background: #eff6ff !important; border-color: #3b82f6 !important; transform: scale(1.02); 
    }
    
    /* כפתור אישור מיוחד */
    .action-btn>button { background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important; color: white !important; border: none !important; }
    .action-btn>button:hover { transform: scale(1.05); box-shadow: 0 10px 15px rgba(16, 185, 129, 0.3); }

    /* התקדמות שלבים */
    .progress-bar { display: flex; justify-content: space-between; background: white; padding: 15px 20px; border-radius: 50px; border: 2px solid #3b82f6; margin-bottom: 30px; font-weight: bold; overflow-x: auto;}
    .step-done { color: #10b981; font-size: 1.2rem; }
    .step-active { color: #2563eb; font-size: 1.3rem; text-decoration: underline; }
    .step-lock { color: #94a3b8; font-size: 1.1rem; }
    
    /* ארנק פרסים */
    .reward-card { background: linear-gradient(45deg, #fbbf24, #f59e0b); color: white; padding: 10px; border-radius: 10px; font-weight: bold; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #fff; }
    .reward-rare { background: linear-gradient(45deg, #8b5cf6, #6d28d9); }
    .reward-legend { background: linear-gradient(45deg, #ef4444, #b91c1c); }
    </style>
""", unsafe_allow_html=True)

# --- ניהול הסטייט ושמירת נתונים ---
def init_state():
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "user" not in st.session_state: st.session_state.user = {"name": "", "age": 10, "gender": ""}
    if "level" not in st.session_state: st.session_state.level = 1
    if "step" not in st.session_state: st.session_state.step = 1
    if "score" not in st.session_state: st.session_state.score = 0
    if "inventory" not in st.session_state: st.session_state.inventory = []
init_state()

# --- מסד הנתונים: רמות, נושאים ופרסים ---
content_db = {
    1: {
        "title": "שלב 1: Teamwork & Talent 🎤",
        "vocab": [
            {"eng": "Audience", "heb": "קהל", "options": ["קהל", "במה", "כישרון"]},
            {"eng": "Nervous", "heb": "לחוץ/עצבני", "options": ["שמח", "לחוץ/עצבני", "רגוע"]},
            {"eng": "Perform", "heb": "להופיע", "options": ["לישון", "לאכול", "להופיע"]},
            {"eng": "Together", "heb": "ביחד", "options": ["ביחד", "לבד", "רחוק"]}
        ],
        "scramble_word": "TOGETHER",
        "scramble_hint": "כשאנחנו לא לבד (עבודת צוות)",
        "grammar_q": "בחר את הזמן הנכון: Right now, she _____ a song on stage.",
        "grammar_options": ["is singing", "sings", "sang"],
        "grammar_correct": "is singing",
        "tf_statement": "The word 'Perform' means to sleep.",
        "tf_correct": "False",
        "story_title": "You've Got Talent 🌟",
        "story_text": "It is the night of the school show. Tom is very nervous. He needs to perform in front of a big audience. His friends tell him, 'We have great teamwork, we will do it together!'.",
        "unseen_q": "How does Tom feel before the show?",
        "unseen_options": ["He is very hungry", "He is very nervous", "He is bored"],
        "unseen_correct": "He is very nervous",
        "video_embed": "https://www.youtube.com/embed/dNXAq2N7d50", 
        "video_q": "לפי הסרטון, איזה משפט נכון לגבי Present Progressive?",
        "video_options": ["מוסיפים ED לפועל", "מוסיפים ING לפועל", "לא משנים את הפועל"],
        "video_correct": "מוסיפים ING לפועל",
        "exam_q": "מה הפירוש של המילה 'Audience'?",
        "exam_options": ["להופיע", "קהל", "לחוץ"],
        "exam_correct": "קהל",
        "reward_name": "Match Attax 2025: Base Card ⚽",
        "reward_type": "normal" # normal, rare, legend
    },
    2: {
        "title": "שלב 2: The Collector's Mystery 🔍",
        "vocab": [
            {"eng": "Valuable", "heb": "בעל ערך", "options": ["זול", "בעל ערך", "שבור"]},
            {"eng": "Search", "heb": "לחפש", "options": ["לחפש", "למצוא", "לשכוח"]},
            {"eng": "Hidden", "heb": "מוסתר", "options": ["גלוי", "מוסתר", "גדול"]},
            {"eng": "Binder", "heb": "קלסר", "options": ["קלסר", "תיק", "כיס"]}
        ],
        "scramble_word": "HIDDEN",
        "scramble_hint": "משהו שלא רואים אותו מיד...",
        "grammar_q": "Where _____ you yesterday?",
        "grammar_options": ["was", "were", "are"],
        "grammar_correct": "were",
        "tf_statement": "If a card is 'Valuable', it means it costs a lot of money or points.",
        "tf_correct": "True",
        "story_title": "The Lost Card",
        "story_text": "Dan lost his most valuable Adrenalyn XL card. He looked in his backpack and his binder, but it was hidden. Finally, he searched under his bed and found it!",
        "unseen_q": "Where did Dan finally find his card?",
        "unseen_options": ["In his binder", "Under his bed", "In his backpack"],
        "unseen_correct": "Under his bed",
        "video_embed": "https://www.youtube.com/embed/z1k8D4xVwG8",
        "video_q": "על איזה זמן דיברו?",
        "video_options": ["עבר", "הווה", "עתיד"],
        "video_correct": "עבר",
        "exam_q": "איך אומרים 'לחפש' באנגלית?",
        "exam_options": ["Hidden", "Search", "Binder"],
        "exam_correct": "Search",
        "reward_name": "Pokémon: Holographic Pikachu ⚡",
        "reward_type": "rare"
    },
    3: {
        "title": "שלב 3: Into the Unknown 🚲",
        "vocab": [
            {"eng": "Disappear", "heb": "להיעלם", "options": ["להופיע", "להיעלם", "לרוץ"]},
            {"eng": "Shadow", "heb": "צל", "options": ["אור", "צל", "צבע"]},
            {"eng": "Promise", "heb": "להבטיח", "options": ["לשקר", "להבטיח", "לבקש"]},
            {"eng": "Dimension", "heb": "מימד", "options": ["מימד", "עיר", "חדר"]}
        ],
        "scramble_word": "PROMISE",
        "scramble_hint": "כשנותנים מילה למישהו שלא נאכזב אותו...",
        "grammar_q": "They _____ going to the cinema tomorrow.",
        "grammar_options": ["is", "am", "are"],
        "grammar_correct": "are",
        "tf_statement": "Shadow is a bright light in the sky.",
        "tf_correct": "False",
        "story_title": "The Upside Down",
        "story_text": "Will was riding his bike when he saw a strange shadow. Suddenly, he seemed to disappear into another dimension. His friends promise to find him, no matter what.",
        "unseen_q": "What did Will see before he disappeared?",
        "unseen_options": ["A dog", "A strange shadow", "A car"],
        "unseen_correct": "A strange shadow",
        "video_embed": "https://www.youtube.com/embed/hzo9me2fdzg",
        "video_q": "מה הפועל ששמעת?",
        "video_options": ["Ride", "Jump", "Fly"],
        "video_correct": "Ride",
        "exam_q": "איך כותבים 'להיעלם'?",
        "exam_options": ["Promise", "Disappear", "Dimension"],
        "exam_correct": "Disappear",
        "reward_name": "Adrenalyn XL: Invincible Legend 🏆",
        "reward_type": "legend"
    }
}

# --- פונקציות עזר ---
def next_step():
    st.session_state.step += 1
    st.session_state.score += 50
    st.rerun()

def give_reward(reward_name, reward_type):
    st.balloons()
    st.session_state.inventory.append({"name": reward_name, "type": reward_type})
    st.session_state.level += 1
    st.session_state.step = 1
    time.sleep(3)
    st.rerun()

# ==========================================
# מסך כניסה ויצירת פרופיל
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div class="rtl-container big-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>🚀 ברוכים הבאים למשחק אנגלית!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>בואו ניצור את השחקן שלכם...</h3><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col2:
        name_input = st.text_input("איך קוראים לך?")
        gender_input = st.selectbox("הדמות שלי היא:", ["בן 👦", "בת 👧"])
    with col1:
        age_input = st.slider("בן / בת כמה את/ה?", 7, 16, 12)
        
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("התחל לשחק! 🎮"):
        if name_input.strip() == "":
            st.error("חובה להקליד שם!")
        else:
            st.session_state.user = {"name": name_input, "age": age_input, "gender": gender_input}
            st.session_state.logged_in = True
            
            # התאמת קושי בסיסי - אם גיל גדול מ10, אפשר להתחיל מרמה קצת יותר קשה (לצורך ההדגמה נשאיר 1)
            st.session_state.level = 1 
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# בניית התפריט הצדדי (סטטוס וארנק הפרסים)
# ==========================================
with st.sidebar:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.markdown(f"<h2>👤 {st.session_state.user['name']}</h2>", unsafe_allow_html=True)
    st.markdown(f"**גיל:** {st.session_state.user['age']} | **רמה:** {st.session_state.level}")
    st.markdown(f"<h3>⭐ ניקוד: {st.session_state.score}</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3>🎒 הארנק שלי:</h3>", unsafe_allow_html=True)
    
    if not st.session_state.inventory:
        st.info("עדיין אין לך פרסים. סיים שלב כדי לזכות!")
    else:
        for item in reversed(st.session_state.inventory):
            if item["type"] == "normal":
                st.markdown(f'<div class="reward-card">{item["name"]}</div>', unsafe_allow_html=True)
            elif item["type"] == "rare":
                st.markdown(f'<div class="reward-card reward-rare">✨ {item["name"]} ✨</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="reward-card reward-legend">🔥 {item["name"]} 🔥</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# בדיקת סיום כל השלבים
if st.session_state.level > max(content_db.keys()):
    st.markdown('<div class="rtl-container big-card"><h1 style="color:#10b981 !important;">👑 אלופי העולם!</h1><h3>סיימתם את קבוצת הגיל הזו!</h3><p>כל הכבוד, השגתם את כל הקלפים האפשריים.</p></div>', unsafe_allow_html=True)
    st.snow()
    st.stop()

current = content_db[st.session_state.level]

# ==========================================
# סרגל התקדמות ראשי (7 משימות)
# ==========================================
st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
steps_names = ["1. מילים", "2. איות", "3. דקדוק", "4. נכון/לא נכון", "5. אנסין", "6. וידאו", "7. בוס!"]
prog_html = '<div class="progress-bar">'
for i, name in enumerate(steps_names, 1):
    if i < st.session_state.step: prog_html += f'<span class="step-done">✅ {name}</span>'
    elif i == st.session_state.step: prog_html += f'<span class="step-active">👉 {name}</span>'
    else: prog_html += f'<span class="step-lock">🔒 {name}</span>'
prog_html += '</div></div>'
st.markdown(prog_html, unsafe_allow_html=True)

st.markdown(f'<div class="rtl-container"><h1 style="text-align:center; margin-bottom: 20px;">{current["title"]}</h1></div>', unsafe_allow_html=True)

# ==========================================
# המסכים / המשימות
# ==========================================

# --- משימה 1: אוצר מילים (כפתורים לחיצים) ---
if st.session_state.step == 1:
    st.markdown('<div class="rtl-container big-card"><h2>🎯 משימה 1: אימון מילים</h2><p>לחצו על הפירוש הנכון לכל מילה. אי אפשר להתקדם עד שהכל נכון!</p></div>', unsafe_allow_html=True)
    
    if "v_correct" not in st.session_state: 
        st.session_state.v_correct = {i: False for i in range(len(current["vocab"]))}

    all_done = True
    for idx, item in enumerate(current["vocab"]):
        st.markdown(f"<h3 style='text-align:center; font-size: 3rem;'>{item['eng']}</h3>", unsafe_allow_html=True)
        if not st.session_state.v_correct[idx]:
            all_done = False
            cols = st.columns(3)
            # ערבוב התשובות
            if f"opts_{st.session_state.level}_{idx}" not in st.session_state:
                shuf = item["options"].copy()
                random.shuffle(shuf)
                st.session_state[f"opts_{st.session_state.level}_{idx}"] = shuf
            
            for i, opt in enumerate(st.session_state[f"opts_{st.session_state.level}_{idx}"]):
                with cols[i]:
                    if st.button(opt, key=f"btn_{idx}_{i}"):
                        if opt == item["heb"]:
                            st.session_state.v_correct[idx] = True
                            st.rerun()
                        else:
                            st.toast("❌ טעות, נסו שוב!", icon="🚨")
        else:
            st.success(f"✅ מצוין! התשובה היא: {item['heb']}")
        st.markdown("---")

    if all_done:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("🚀 המשך למשימה הבאה"):
            del st.session_state.v_correct
            next_step()
        st.markdown('</div>', unsafe_allow_html=True)

# --- משימה 2: איות ---
elif st.session_state.step == 2:
    st.markdown('<div class="rtl-container big-card"><h2>🧩 משימה 2: פצח את הקוד</h2></div>', unsafe_allow_html=True)
    
    word = current["scramble_word"]
    if f"scr_{st.session_state.level}" not in st.session_state:
        l = list(word)
        random.shuffle(l)
        st.session_state[f"scr_{st.session_state.level}"] = "   ".join(l)
        
    st.markdown(f"<h1 style='text-align:center; letter-spacing: 15px; color:#c026d3 !important;'>{st.session_state[f'scr_{st.session_state.level}']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; direction:rtl;'>💡 רמז: {current['scramble_hint']}</h3><br>", unsafe_allow_html=True)
    
    # שימוש בתיבת טקסט אבל עם כפתור גדול מתחת
    guess = st.text_input("הקלידו את המילה באנגלית:", key="scr_in").strip().upper()
    
    st.markdown('<div class="action-btn">', unsafe_allow_html=True)
    if st.button("פתח את המנעול 🔓"):
        if guess == word:
            st.success("✅ מדהים! פיצחת את הקוד.")
            time.sleep(1)
            next_step()
        else:
            st.error("❌ טעות. נסו שוב.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- משימה 3: דקדוק ---
elif st.session_state.step == 3:
    st.markdown('<div class="rtl-container big-card"><h2>⚖️ משימה 3: אתגר הדקדוק</h2></div>', unsafe_allow_html=True)
    st.markdown(f"<h2 style='direction:ltr; text-align:left; font-size:35px;'>{current['grammar_q']}</h2><br>", unsafe_allow_html=True)
    
    cols = st.columns(len(current['grammar_options']))
    for i, opt in enumerate(current['grammar_options']):
        with cols[i]:
            if st.button(opt, key=f"g_btn_{i}"):
                if opt == current['grammar_correct']:
                    st.success("✅ בול!")
                    time.sleep(1)
                    next_step()
                else:
                    st.error("❌ לא נכון.")

# --- משימה 4: נכון או לא נכון (משימה חדשה) ---
elif st.session_state.step == 4:
    st.markdown('<div class="rtl-container big-card"><h2>🤔 משימה 4: נכון או לא נכון?</h2></div>', unsafe_allow_html=True)
    st.markdown(f"<div class='big-card ltr-container' style='font-size:30px; font-weight:bold; text-align:center; background:#fef08a;'>{current['tf_statement']}</div><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ True (נכון)"):
            if current['tf_correct'] == "True":
                st.success("✅ אלופים!")
                time.sleep(1)
                next_step()
            else:
                st.error("❌ טעות.")
    with col2:
        if st.button("❌ False (לא נכון)"):
             if current['tf_correct'] == "False":
                st.success("✅ אלופים!")
                time.sleep(1)
                next_step()
             else:
                st.error("❌ טעות.")

# --- משימה 5: אנסין (הסיפור המיוחד) ---
elif st.session_state.step == 5:
    st.markdown(f'<div class="rtl-container big-card"><h2>📖 משימה 5: {current["story_title"]}</h2></div>', unsafe_allow_html=True)
    st.markdown(f"<div class='ltr-container big-card' style='font-size: 26px; line-height:1.6; border-left:8px solid #f59e0b;'>{current['story_text']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"<h3 class='ltr-container'>❓ {current['unseen_q']}</h3><br>", unsafe_allow_html=True)
    
    for i, opt in enumerate(current['unseen_options']):
        if st.button(opt, key=f"u_btn_{i}"):
            if opt == current['unseen_correct']:
                st.success("✅ הבנת הנקרא מושלמת!")
                time.sleep(1)
                next_step()
            else:
                st.error("❌ קראו שוב את הטקסט.")

# --- משימה 6: וידאו (מתוקן עם Iframe) ---
elif st.session_state.step == 6:
    st.markdown('<div class="rtl-container big-card"><h2>🎬 משימה 6: צפייה והבנה</h2></div>', unsafe_allow_html=True)
    
    # שימוש ב-iframe פותר כמעט כל בעיית הצגת וידאו ב-Streamlit
    components.iframe(current['video_embed'], height=450)
    
    st.markdown(f"<h3 class='rtl-container'>{current['video_q']}</h3><br>", unsafe_allow_html=True)
    for i, opt in enumerate(current['video_options']):
        if st.button(opt, key=f"v_btn_{i}"):
            if opt == current['video_correct']:
                st.success("✅ תשובה נכונה!")
                time.sleep(1)
                next_step()
            else:
                st.error("❌ טעות, צפו שוב.")

# --- משימה 7: שאלת הבוס ופרס ---
elif st.session_state.step == 7:
    st.markdown('<div class="rtl-container big-card" style="border: 4px solid #ef4444; background: #fef2f2;"><h1 style="color:#ef4444 !important;">🐉 קרב הבוס!</h1><p>ענו נכון כדי לסיים את השלב ולקבל את הקלף!</p></div>', unsafe_allow_html=True)
    
    st.markdown(f"<h2 class='rtl-container'>{current['exam_q']}</h2><br>", unsafe_allow_html=True)
    for i, opt in enumerate(current['exam_options']):
        if st.button(opt, key=f"boss_btn_{i}"):
            if opt == current['exam_correct']:
                st.success(f"🎉 ניצחתם! זכיתם ב: {current['reward_name']}")
                give_reward(current['reward_name'], current['reward_type'])
            else:
                st.error("❌ הבוס פגע בכם! נסו שוב.")
