import streamlit as st
import random
import time

# הגדרות עמוד
st.set_page_config(page_title="SmartEnglish - Adventure", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# --- מסד הנתונים המעוצב ---
# כל שלב עכשיו מכיל פרס מיוחד!
content_db = {
    1: {
        "title": "שלב 1: You've Got Talent 🌟",
        "vocab": [
            {"eng": "Talent", "heb": "כישרון", "options": ["כישרון", "שולחן", "ספר"]},
            {"eng": "Stage", "heb": "במה", "options": ["במה", "כיסא", "חלון"]},
            {"eng": "Sing", "heb": "לשיר", "options": ["לרוץ", "לשיר", "לקפוץ"]},
            {"eng": "Teamwork", "heb": "עבודת צוות", "options": ["עבודת צוות", "משחק כדור", "שיעורי בית"]}
        ],
        "scramble_word": "STAGE",
        "scramble_hint": "המקום שעליו מופיעים",
        "grammar_q": "בחר את המילה הנכונה: I _____ singing on the stage right now.",
        "grammar_options": ["am", "is", "are"],
        "grammar_correct": "am",
        "story_title": "The School Talent Show 🎤",
        "story_text": "Today is the school talent show. Ben and Sarah have great teamwork. Ben plays the guitar and Sarah sings. They are on the stage now. Everyone claps their hands!",
        "unseen_q": "What does Ben do in the talent show?",
        "unseen_options": ["He sings", "He plays the guitar", "He dances"],
        "unseen_correct": "He plays the guitar",
        "video_url": "https://www.youtube.com/watch?v=dNXAq2N7d50",
        "video_q": "על איזה זמן דקדוקי שמעת בסרטון?",
        "video_options": ["Present Progressive", "Past Simple", "Future"],
        "video_correct": "Present Progressive",
        "exam_q": "איך אומרים 'כישרון' באנגלית?",
        "exam_options": ["Stage", "Talent", "Teamwork"],
        "exam_correct": "Talent",
        "reward": "🏆 גביע כוכב נולד"
    },
    2: {
        "title": "שלב 2: The Trading Cards Master ⚽",
        "vocab": [
            {"eng": "Rare", "heb": "נדיר", "options": ["רגיל", "נדיר", "משעמם"]},
            {"eng": "Trade", "heb": "להחליף / לסחור", "options": ["לקנות", "להחליף / לסחור", "לזרוק"]},
            {"eng": "Collection", "heb": "אוסף", "options": ["אוסף", "משחק", "תמונה"]},
            {"eng": "Combo", "heb": "שילוב", "options": ["שילוב", "תחרות", "הפסד"]}
        ],
        "scramble_word": "RARE",
        "scramble_hint": "משהו שקשה מאוד למצוא",
        "grammar_q": "איך נגיד 'יש לי קלף נדיר'?",
        "grammar_options": ["I have a rare card", "I has a rare card", "I having a rare card"],
        "grammar_correct": "I have a rare card",
        "story_title": "The Golden Card ✨",
        "story_text": "Mike loves collecting football cards. Yesterday, he opened a new pack of Match Attax. He found an ultra-rare golden card! He wants to trade it to complete his collection.",
        "unseen_q": "What did Mike find in the pack?",
        "unseen_options": ["A silver coin", "An ultra-rare golden card", "A normal card"],
        "unseen_correct": "An ultra-rare golden card",
        "video_url": "https://www.youtube.com/watch?v=z1k8D4xVwG8",
        "video_q": "איזה זמן מתאר דברים שקרו אתמול (כמו בסיפור)?",
        "video_options": ["Present Simple", "Past Simple", "Present Progressive"],
        "video_correct": "Past Simple",
        "exam_q": "מה הפירוש של המילה Collection?",
        "exam_options": ["אוסף", "להחליף", "נדיר"],
        "exam_correct": "אוסף",
        "reward": "⚽ קלף Match Attax זוהר 100!"
    },
    3: {
        "title": "שלב 3: Catch Them All ⚡",
        "vocab": [
            {"eng": "Electric", "heb": "חשמלי", "options": ["אש", "חשמלי", "מים"]},
            {"eng": "Battle", "heb": "קרב", "options": ["קרב", "חברות", "אוכל"]},
            {"eng": "Trainer", "heb": "מאמן", "options": ["שחקן", "מאמן", "צופה"]},
            {"eng": "Evolve", "heb": "להתפתח", "options": ["להתפתח", "לישון", "לברוח"]}
        ],
        "scramble_word": "BATTLE",
        "scramble_hint": "כששניים נלחמים אחד בשני זה...",
        "grammar_q": "She ______ (to train) her pet every day.",
        "grammar_options": ["trains", "training", "train"],
        "grammar_correct": "trains",
        "story_title": "The Forest Adventure 🌲",
        "story_text": "Ash is a great trainer. He walks in the forest with his electric friend. Suddenly, a wild creature appears! They start a battle. His friend uses a thunder shock and they win.",
        "unseen_q": "Where does Ash walk?",
        "unseen_options": ["In the city", "In the forest", "At school"],
        "unseen_correct": "In the forest",
        "video_url": "https://www.youtube.com/watch?v=L89cZYhNjWM",
        "video_q": "הסרטון מראה חיות, מי מביניהן לא הופיעה?",
        "video_options": ["אריה", "כלב", "תנין"],
        "video_correct": "תנין",
        "exam_q": "מה זה Trainer?",
        "exam_options": ["חשמלי", "מאמן", "קרב"],
        "exam_correct": "מאמן",
        "reward": "⚡ מדבקת פוקימון הולוגרפית"
    },
    4: {
        "title": "שלב 4: The Upside Down Mystery 🔦",
        "vocab": [
            {"eng": "Strange", "heb": "מוזר", "options": ["רגיל", "מוזר", "שמח"]},
            {"eng": "Flashlight", "heb": "פנס", "options": ["פנס", "טלפון", "מחשב"]},
            {"eng": "Friends", "heb": "חברים", "options": ["אויבים", "חברים", "מורים"]},
            {"eng": "Danger", "heb": "סכנה", "options": ["סכנה", "ביטחון", "משחק"]}
        ],
        "scramble_word": "STRANGE",
        "scramble_hint": "משהו לא רגיל... קצת משונה",
        "grammar_q": "What ______ you doing yesterday at 8 PM?",
        "grammar_options": ["was", "were", "are"],
        "grammar_correct": "were",
        "story_title": "Missing Bikes 🚲",
        "story_text": "Four friends ride their bikes at night. It is dark, so they use flashlights. Suddenly, they see something strange in the sky. They know they are in danger, so they pedal fast to get home.",
        "unseen_q": "Why do the friends use flashlights?",
        "unseen_options": ["Because they are cold", "Because it is dark", "Because it looks cool"],
        "unseen_correct": "Because it is dark",
        "video_url": "https://www.youtube.com/watch?v=hzo9me2fdzg",
        "video_q": "מה הפועל הנכון ל-לרכוב על אופניים?",
        "video_options": ["Drive", "Ride", "Fly"],
        "video_correct": "Ride",
        "exam_q": "איך כותבים 'סכנה' באנגלית?",
        "exam_options": ["Strange", "Danger", "Friends"],
        "exam_correct": "Danger",
        "reward": "🚲 מדבקת מועדון Hellfire"
    }
}

# --- ניהול הסטייט (State Management) ---
if "level" not in st.session_state:
    st.session_state.level = 1
if "current_step" not in st.session_state:
    st.session_state.current_step = 1 # 1:vocab, 2:scramble, 3:grammar, 4:story, 5:video, 6:exam
if "score" not in st.session_state:
    st.session_state.score = 0
if "rewards" not in st.session_state:
    st.session_state.rewards = []
if "vocab_progress" not in st.session_state:
    st.session_state.vocab_progress = {}

# --- CSS מרהיב וחוויית משתמש ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap');
    
    /* הסתרת כותרות Streamlit ברירת מחדל */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Heebo', sans-serif; 
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
        color: #0f172a !important; 
    }
    .rtl-container { direction: rtl; text-align: right; }
    
    /* עיצוב כרטיסיות ענקיות */
    .big-card { 
        background: white; 
        padding: 40px; 
        border-radius: 24px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); 
        margin-bottom: 20px;
        border: 2px solid #bae6fd;
        text-align: center;
    }
    
    h1, h2, h3 { color: #0369a1 !important; font-weight: 900 !important; }
    h1 { font-size: 3rem !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }
    
    .stButton>button { 
        background: linear-gradient(to right, #3b82f6, #2563eb) !important; 
        color: white !important; 
        font-size: 22px !important; 
        font-weight: 900 !important; 
        border-radius: 16px !important; 
        padding: 15px 30px !important; 
        border: none !important; 
        width: 100%; 
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease; 
    }
    .stButton>button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.3);
    }
    
    .stRadio>div { direction: rtl; font-size: 20px; background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; }
    
    /* בר התקדמות עליון */
    .progress-container {
        display: flex;
        justify-content: space-between;
        background: white;
        padding: 15px 30px;
        border-radius: 50px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #3b82f6;
    }
    .step-active { color: #2563eb; font-weight: 900; }
    .step-done { color: #16a34a; }
    .step-lock { color: #94a3b8; }
    </style>
""", unsafe_allow_html=True)

# פונקציות עזר
def next_step():
    st.session_state.current_step += 1
    st.session_state.score += 20
    st.rerun()

def complete_level(reward):
    st.balloons()
    st.session_state.rewards.append(reward)
    st.session_state.level += 1
    st.session_state.current_step = 1
    st.session_state.vocab_progress = {}
    time.sleep(3)
    st.rerun()

# בדיקת סיום המשחק
if st.session_state.level > max(content_db.keys()):
    st.snow()
    st.markdown("""
        <div class="big-card">
            <h1>🏆 סיימת את כל השלבים! 🏆</h1>
            <h3>אתה פשוט אלוף העולם באנגלית!</h3>
        </div>
    """, unsafe_allow_html=True)
    st.write("### האוסף המטורף שלך:")
    for r in st.session_state.rewards:
        st.markdown(f"<h2>{r}</h2>", unsafe_allow_html=True)
    st.stop()

current_data = content_db[st.session_state.level]

# --- סרגל התקדמות עליון ---
steps_names = ["1. מילים", "2. איות", "3. דקדוק", "4. סיפור", "5. וידאו", "6. בוס!"]
progress_html = '<div class="rtl-container progress-container">'
for i, name in enumerate(steps_names, 1):
    if i < st.session_state.current_step:
        progress_html += f'<span class="step-done">✅ {name}</span>'
    elif i == st.session_state.current_step:
        progress_html += f'<span class="step-active">👉 {name}</span>'
    else:
        progress_html += f'<span class="step-lock">🔒 {name}</span>'
progress_html += '</div>'
st.markdown(progress_html, unsafe_allow_html=True)

# תצוגת ניקוד ופרסים שנאספו בצד
with st.sidebar:
    st.markdown(f"<h1>⭐ {st.session_state.score}</h1>", unsafe_allow_html=True)
    st.markdown("### 🎒 התיק שלי:")
    if not st.session_state.rewards:
        st.write("עדיין אין פרסים, תסיים שלב כדי לקבל!")
    for r in st.session_state.rewards:
        st.markdown(f"<h4>{r}</h4>", unsafe_allow_html=True)

st.markdown(f'<div class="rtl-container"><h1 style="text-align:center;">{current_data["title"]}</h1></div>', unsafe_allow_html=True)

# ==========================================
# המסכים (רק מסך אחד מופיע בכל פעם)
# ==========================================

# מסך 1: לימוד מילים אקטיבי (מבחן אמריקאי לכל מילה)
if st.session_state.current_step == 1:
    st.markdown('<div class="big-card rtl-container"><h2>🎯 משימה 1: אימון מילים</h2><p style="font-size:20px;">בחר את הפירוש הנכון לכל מילה כדי להתקדם!</p></div>', unsafe_allow_html=True)
    
    all_correct = True
    for idx, item in enumerate(current_data["vocab"]):
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align:center; color:#e11d48 !important; font-size:40px;'>{item['eng']}</h3>", unsafe_allow_html=True)
            
            # מערבב את האפשרויות רק פעם אחת לכל מילה
            if f"opts_{st.session_state.level}_{idx}" not in st.session_state:
                shuffled = item["options"].copy()
                random.shuffle(shuffled)
                st.session_state[f"opts_{st.session_state.level}_{idx}"] = shuffled
                
            choice = st.radio("מה הפירוש?", st.session_state[f"opts_{st.session_state.level}_{idx}"], key=f"v_{idx}", index=None)
            
            if choice == item["heb"]:
                st.success("✅ מצוין!")
            elif choice is not None:
                st.error("❌ נסה שוב...")
                all_correct = False
            else:
                all_correct = False

    if all_correct:
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("🚀 כל הכבוד! המשך למשימה הבאה"):
            next_step()

# מסך 2: משחק איות
elif st.session_state.current_step == 2:
    st.markdown('<div class="big-card rtl-container"><h2>🧩 משימה 2: פיצוח הכספת</h2><p style="font-size:20px;">סדרו את האותיות למילה הנכונה באנגלית.</p></div>', unsafe_allow_html=True)
    
    target_w = current_data["scramble_word"]
    if f"scr_{st.session_state.level}" not in st.session_state:
        l = list(target_w)
        random.shuffle(l)
        st.session_state[f"scr_{st.session_state.level}"] = " - ".join(l)
        
    st.markdown(f"<h1 style='text-align:center; font-size:60px; color:#c026d3 !important; letter-spacing:10px;'>{st.session_state[f'scr_{st.session_state.level}']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; direction:rtl;'>💡 רמז: {current_data['scramble_hint']}</h3>", unsafe_allow_html=True)
    
    user_guess = st.text_input("הקלד את המילה כאן (באנגלית בלבד):").strip().upper()
    
    if st.button("פתח את הכספת 🔓"):
        if user_guess == target_w:
            st.success("✅ מדהים! הכספת נפתחה.")
            time.sleep(1)
            next_step()
        else:
            st.error("❌ טעות... נסה שוב.")

# מסך 3: דקדוק
elif st.session_state.current_step == 3:
    st.markdown('<div class="big-card rtl-container"><h2>⚖️ משימה 3: אתגר הדקדוק</h2></div>', unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='direction:ltr; text-align:left;'>{current_data['grammar_q']}</h3>", unsafe_allow_html=True)
    ans = st.radio("בחר את התשובה הנכונה:", current_data['grammar_options'], index=None)
    
    if st.button("בדוק תשובה ✅"):
        if ans == current_data['grammar_correct']:
            st.success("✅ בול! אתה שולט בדקדוק.")
            time.sleep(1)
            next_step()
        elif ans is not None:
            st.error("❌ טעות. נסה אפשרות אחרת.")

# מסך 4: סיפור / אנסין
elif st.session_state.current_step == 4:
    st.markdown(f'<div class="big-card rtl-container"><h2>📖 משימה 4: {current_data["story_title"]}</h2></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:16px; border-left:10px solid #f59e0b; font-size:24px; direction:ltr; text-align:left; margin-bottom:20px; line-height:1.6;">
            {current_data['story_text']}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='direction:ltr; text-align:left;'>❓ {current_data['unseen_q']}</h3>", unsafe_allow_html=True)
    story_ans = st.radio("בחר את התשובה:", current_data['unseen_options'], index=None)
    
    if st.button("הגש תשובה לסיפור 📝"):
        if story_ans == current_data['unseen_correct']:
            st.success("✅ אלוף! הבנת הנקרא מושלמת.")
            time.sleep(1)
            next_step()
        elif story_ans is not None:
            st.error("❌ זה לא מדויק, קרא את הסיפור שוב.")

# מסך 5: סרטון וידאו
elif st.session_state.current_step == 5:
    st.markdown('<div class="big-card rtl-container"><h2>🎬 משימה 5: הקשבה וצפייה</h2></div>', unsafe_allow_html=True)
    
    st.video(current_data['video_url'])
    
    st.markdown(f"<h3 style='direction:rtl; text-align:right;'>{current_data['video_q']}</h3>", unsafe_allow_html=True)
    vid_ans = st.radio("בחר תשובה:", current_data['video_options'], index=None)
    
    if st.button("עברתי את משימת הוידאו? 🎥"):
        if vid_ans == current_data['video_correct']:
            st.success("✅ מעולה! הקשבת מצוין.")
            time.sleep(1)
            next_step()
        elif vid_ans is not None:
            st.error("❌ תשובה לא נכונה. תצפה שוב בקטע הרלוונטי.")

# מסך 6: הבוס הגדול!
elif st.session_state.current_step == 6:
    st.markdown("""
        <div class="big-card rtl-container" style="border:4px solid #ef4444; background: #fef2f2;">
            <h1 style="color:#ef4444 !important;">🐉 שאלת הבוס!</h1>
            <p style="font-size:22px;">זה המבחן האחרון לשלב זה. ענה נכון וקבל את הפרס!</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='direction:rtl; text-align:right;'>{current_data['exam_q']}</h3>", unsafe_allow_html=True)
    boss_ans = st.radio("התשובה הסופית שלך:", current_data['exam_options'], index=None)
    
    if st.button("💥 נצח את הבוס!"):
        if boss_ans == current_data['exam_correct']:
            st.success(f"🎉 ניצחון!!! השגת: {current_data['reward']}")
            complete_level(current_data['reward'])
        elif boss_ans is not None:
            st.error("❌ הבוס פגע בך! נסה שוב את השאלה.")
