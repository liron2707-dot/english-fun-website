import streamlit as st
import random
import time

st.set_page_config(page_title="Nexus English", page_icon="🎓", layout="centered")

# --- עיצוב נקי, קריא ויפה ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Heebo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8fafc;
    }
    .task-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .unseen-text {
        background-color: #f1f5f9;
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        font-size: 20px;
        direction: ltr !important;
        text-align: left !important;
        color: #1e293b;
        margin: 15px 0;
        line-height: 1.6;
    }
    div[role="radiogroup"] label span {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# בנק התוכן האיכותי והמעניין (מחולק לפי גילאים וסוגי משימות)
# ==========================================
CONTENT_BANK = {
    "7-9": [
        {"type": "vocab", "title": "אוצר מילים: חיות", "q": "איך אומרים 'כלב' באנגלית?", "a": "Dog", "options": ["Dog", "Cat", "Bird", "Fish"]},
        {"type": "grammar", "title": "דקדוק בסיסי: פעלים", "q": "בחר את המילה החסרה: I ____ an apple.", "a": "eat", "options": ["eat", "run", "sleep", "jump"]},
        {"type": "unseen", "title": "הבנת הנקרא: Toby the Dog", 
         "text": "Meet Toby. Toby is a small, brown dog. He loves to run in the park and play with his red ball. Toby has long ears and a happy tail.", 
         "q": "What color is Toby's ball?", "a": "Red", "options": ["Red", "Blue", "Green", "Yellow"]},
        {"type": "video", "title": "הבנת הנשמע: שיר הצבעים", "vid_url": "https://www.youtube.com/watch?v=tRNy2i75tCc", 
         "q": "על איזה נושא השיר מדבר?", "a": "צבעים (Colors)", "options": ["צבעים (Colors)", "חיות (Animals)", "מספרים (Numbers)", "משפחה (Family)"]},
        {"type": "game", "title": "משחקון: פיצוח מילים", "q": "סדר את האותיות הבאות כדי לגלות איזה פרי מסתתר כאן: [ P L P E A ]", "a": "Apple", "options": ["Apple", "Peach", "Plum", "Grape"]}
    ],
    "10-12": [
        {"type": "vocab", "title": "אוצר מילים: תחביבים", "q": "איזה מהמשחקים הבאים מתאר משחק כדורגל?", "a": "Football", "options": ["Football", "Chess", "Swimming", "Reading"]},
        {"type": "grammar", "title": "דקדוק: הווה ממושך", "q": "Look! The cat ____ on your bed right now.", "a": "is sleeping", "options": ["is sleeping", "sleeps", "slept", "sleeping"]},
        {"type": "unseen", "title": "הבנת הנקרא: The Minecraft Castle", 
         "text": "Mia and Liam love playing Minecraft. Yesterday, they built a giant castle with high walls. Suddenly, a creeper appeared and exploded! They laughed and started building again.", 
         "q": "What did Mia and Liam build?", "a": "A giant castle", "options": ["A giant castle", "A small house", "A big boat", "A fast car"]},
        {"type": "game", "title": "יוצא דופן בהיגיון", "q": "איזו מילה אינה שייכת לקבוצת ה'מקצועות בבית הספר'?", "a": "Pizza", "options": ["Pizza", "Math", "History", "Science"]},
        {"type": "vocab", "title": "השלמת משפט", "q": "I was very thirsty, so I drank a glass of ____.", "a": "Water", "options": ["Water", "Bread", "Paper", "Shoes"]}
    ],
    "13-15": [
        {"type": "vocab", "title": "אוצר מילים מתקדם", "q": "מה הפירוש של המילה 'Opportunity'?", "a": "הזדמנות", "options": ["הזדמנות", "בעיה", "מטרה", "סכנה"]},
        {"type": "grammar", "title": "דקדוק: משפטי תנאי", "q": "If it rains tomorrow, we ____ at home.", "a": "will stay", "options": ["will stay", "stayed", "would stay", "staying"]},
        {"type": "unseen", "title": "הבנת הנקרא: Content Creators", 
         "text": "Many teenagers dream of becoming professional content creators. However, behind the cool videos, there are hours of editing, planning, and hard work. It's not just about turning on a camera.", 
         "q": "According to the text, what is behind the cool videos?", "a": "Hours of editing and hard work", "options": ["Hours of editing and hard work", "Only turning on a camera", "A lot of free time", "Playing video games"]},
        {"type": "game", "title": "יוצא דופן בהיגיון מתקדם", "q": "איזו מילה אינה שייכת לקבוצת 'מילים המתארות קושי'?", "a": "Easy", "options": ["Easy", "Difficult", "Hard", "Tough"]},
        {"type": "grammar", "title": "השלמת משפט בהקשר", "q": "She studied all night; ____, she passed the exam with a high grade.", "a": "therefore", "options": ["therefore", "however", "although", "but"]}
    ]
}

# --- ניהול מצב משתמש (Session State) ---
if "user" not in st.session_state:
    st.session_state.user = None
if "screen" not in st.session_state:
    st.session_state.screen = "login"

# ==========================================
# מסך 1: התחברות
# ==========================================
if st.session_state.screen == "login":
    st.title("🎓 ברוכים הבאים לאקדמיה לאנגלית")
    st.write("בואו נלמד אנגלית בצורה מעניינת שמותאמת במיוחד אליכם!")
    
    with st.container():
        st.markdown('<div class="task-card">', unsafe_allow_html=True)
        name = st.text_input("איך קוראים לך?")
        age = st.selectbox("לאיזו קבוצת גיל אתה שייך?", ["7-9", "10-12", "13-15"])
        
        if st.button("התחל לשחק וללמד 🚀", use_container_width=True):
            if name:
                st.session_state.user = {
                    "name": name, 
                    "age_group": age, 
                    "task_index": 0,  # איזה משימה הוא עושה כרגע
                    "score": 0
                }
                st.session_state.screen = "game"
                st.rerun()
            else:
                st.error("אנא הכנס את שמך כדי להתחיל.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# מסך 2: משחק ולמידה
# ==========================================
elif st.session_state.screen == "game" and st.session_state.user:
    u = st.session_state.user
    age_group = u["age_group"]
    tasks = CONTENT_BANK[age_group]
    
    # בדיקה אם סיים את כל המשימות
    if u["task_index"] >= len(tasks):
        st.balloons()
        st.success(f"כל הכבוד {u['name']}! סיימת את כל השלב המרתק הזה! צברת {u['score']} נקודות.")
        if st.button("התחל מחדש 🔄"):
            st.session_state.user["task_index"] = 0
            st.session_state.user["score"] = 0
            st.rerun()
        st.stop()

    # שליפת המשימה הנוכחית
    current_task = tasks[u["task_index"]]
    
    # הצגת התקדמות
    st.progress(u["task_index"] / len(tasks))
    st.write(f"משימה {u['task_index'] + 1} מתוך {len(tasks)} | 🏆 נקודות: {u['score']}")
    
    # כרטיסיית המשימה
    st.markdown('<div class="task-card">', unsafe_allow_html=True)
    st.subheader(f"🎯 {current_task['title']}")
    
    # אם יש טקסט קריאה (Unseen)
    if "text" in current_task:
        st.markdown("קראו את הקטע הבא באנגלית וענו על השאלה:")
        st.markdown(f'<div class="unseen-text">{current_task["text"]}</div>', unsafe_allow_html=True)
        
    # אם יש סרטון
    if "vid_url" in current_task:
        st.video(current_task["vid_url"])
        st.write("צפו בסרטון הקצר וענו:")

    # הצגת השאלה
    st.markdown(f"**{current_task['q']}**")
    
    # בחירת תשובה (אנו מערבבים את האפשרויות כדי שלא תמיד התשובה הראשונה תהיה הנכונה)
    options = current_task["options"].copy()
    # שימוש בזרע אקראי מבוסס על מספר המשימה כדי שהערבוב לא ישתנה בכל לחיצה
    random.Random(u["task_index"]).shuffle(options) 
    
    ans = st.radio("בחר תשובה:", options, index=None, key=f"q_{u['task_index']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("בדוק תשובה ⚡", use_container_width=True):
        if ans == current_task["a"]:
            st.success("מעולה! תשובה נכונה. 🎉")
            time.sleep(1)
            st.session_state.user["task_index"] += 1
            st.session_state.user["score"] += 10
            st.rerun()
        elif ans is not None:
            st.error("לא נורא! נסה לקרוא שוב ולחשוב על תשובה אחרת. 🤔")
