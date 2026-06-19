import streamlit as st
import json
import os
import time
import random

# --- הגדרות מערכת ---
st.set_page_config(page_title="Nexus English", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

DB_FILE = "users_db_v4.json"
CONTENT_FILE = "content_v4.json"

# --- CSS עדין לקריאות ולגודל הפונטים (בלי לשבור את תפריט הצד) ---
st.markdown("""
    <style>
    /* הגדלת הטקסט של כפתורי הבחירה האמריקאית */
    div[role="radiogroup"] label span {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    /* עיצוב כרטיסיית האנסין (קטע קריאה) */
    .unseen-box {
        background-color: rgba(100, 116, 139, 0.2);
        border-right: 5px solid #6366f1;
        padding: 20px;
        border-radius: 10px;
        font-size: 20px;
        direction: ltr;
        text-align: left;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- פונקציות מסד נתונים ---
def load_json(filename):
    if not os.path.exists(filename): return {}
    with open(filename, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- מנוע יצירת תוכן מותאם גיל (Unseens, Videos, Grammar) ---
def ensure_content_exists():
    if os.path.exists(CONTENT_FILE): return
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # מאגרי קטעי קריאה מותאמים גיל
    unseens_7_9 = [
        {"text": "Tom has a big red ball. He plays with it in the park. His dog likes the ball too.", "q": "Where does Tom play?", "a": "In the park", "options": ["In the park", "At school", "In the house", "In the pool"]}
    ]
    
    unseens_10_12 = [
        {"text": "Mike bought a new Match Attax 2025 card pack. He was looking for an ultra-rare holographic card to make a great combo for his team. When he opened it, he yelled with joy!", "q": "What was Mike looking for?", "a": "A rare card", "options": ["A rare card", "A football", "A new friend", "A video game"]},
        {"text": "Ben and Sarah are in the school talent show. They learned that teamwork is the secret to success. When they sang their song, everyone clapped loudly.", "q": "What is the secret to success in the story?", "a": "Teamwork", "options": ["Teamwork", "Singing loudly", "Going home", "Being alone"]}
    ]
    
    unseens_13_15 = [
        {"text": "The story 'You've Got Talent' from the Teamwork curriculum emphasizes how collaboration brings out the best in people. By combining individual strengths, a group can achieve extraordinary results.", "q": "What does the text say about combining strengths?", "a": "It achieves extraordinary results", "options": ["It achieves extraordinary results", "It makes people tired", "It is only for talent shows", "It causes arguments"]},
        {"text": "In biology, understanding the hierarchy of living things is crucial. Every complex organism is made of trillions of cells, each performing specific functions to keep the body alive.", "q": "What are complex organisms made of?", "a": "Trillions of cells", "options": ["Trillions of cells", "Only one cell", "Water and air", "Plants"]}
    ]

    # סרטוני יוטיוב לדוגמה
    videos = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=3yXpeBGEqD0"]

    for age_group in db.keys():
        for level in range(1, 100):
            db[age_group][str(level)] = {}
            for sub in range(8):
                task = {}
                # 1. אוצר מילים
                if sub == 0:
                    if age_group == "7-9": task = {"q": "איך אומרים 'צהוב' באנגלית?", "a": "Yellow", "options": ["Yellow", "Green", "Blue", "Red"]}
                    elif age_group == "10-12": task = {"q": "מה הפירוש של 'Discover'?", "a": "לגלות", "options": ["לגלות", "לבנות", "להרוס", "לקנות"]}
                    else: task = {"q": "מה הפירוש של 'Significant'?", "a": "משמעותי", "options": ["משמעותי", "זעיר", "מהיר", "מסוכן"]}
                # 2. דקדוק
                elif sub == 1:
                    if age_group == "7-9": task = {"q": "She ____ a good friend.", "a": "is", "options": ["is", "are", "am", "be"]}
                    elif age_group == "10-12": task = {"q": "They ____ playing football right now.", "a": "are", "options": ["are", "is", "was", "were"]}
                    else: task = {"q": "If I had money, I ____ buy a car.", "a": "would", "options": ["would", "will", "can", "am"]}
                # 3. הבנת הנקרא (Unseen)
                elif sub == 2:
                    if age_group == "7-9": u = random.choice(unseens_7_9)
                    elif age_group == "10-12": u = random.choice(unseens_10_12)
                    else: u = random.choice(unseens_13_15)
                    task = {"unseen": u["text"], "q": u["q"], "a": u["a"], "options": u["options"]}
                # 4. וידאו אינטראקטיבי
                elif sub == 3:
                    task = {"video_url": random.choice(videos), "q": "על סמך הסרטון (או הכללים שלמדת), מה התשובה הנכונה לשלב זה?", "a": "Yes", "options": ["Yes", "No", "Maybe", "Never"]}
                # 5. אמת או שקר
                elif sub == 4:
                    if age_group == "7-9": task = {"q": "Cats can fly. (True/False)", "a": "False", "options": ["True", "False"]}
                    elif age_group == "10-12": task = {"q": "A year has 12 months. (True/False)", "a": "True", "options": ["True", "False"]}
                    else: task = {"q": "Photosynthesis requires oxygen. (True/False)", "a": "False", "options": ["True", "False"]}
                # 6. יוצא דופן
                elif sub == 5:
                    if age_group == "7-9": task = {"q": "מי יוצא דופן?", "a": "Table", "options": ["Dog", "Cat", "Table", "Fish"]}
                    elif age_group == "10-12": task = {"q": "איזו מילה אינה קשורה לזמן?", "a": "Apple", "options": ["Tomorrow", "Yesterday", "Apple", "Soon"]}
                    else: task = {"q": "Find the odd one out:", "a": "Hesitate", "options": ["Run", "Sprint", "Dash", "Hesitate"]}
                # 7. השלמת משפט
                elif sub == 6:
                    if age_group == "7-9": task = {"q": "I eat an ____ every day.", "a": "apple", "options": ["apple", "chair", "sun", "dog"]}
                    elif age_group == "10-12": task = {"q": "You should ____ your homework.", "a": "do", "options": ["do", "make", "have", "take"]}
                    else: task = {"q": "Despite the rain, they decided to ____ the match.", "a": "continue", "options": ["continue", "cancel", "stop", "pause"]}
                # 8. שאלת בוס
                elif sub == 7:
                    task = {"q": f"שאלת הבוס לשלב {level}! בחר בתשובה הנכונה כדי לנצח:", "a": "Victory", "options": ["Victory", "Defeat", "Loss", "Fail"]}

                random.shuffle(task["options"])
                db[age_group][str(level)][str(sub)] = task
    save_json(CONTENT_FILE, db)

ensure_content_exists()

# --- ניהול משתמש ---
if "user" not in st.session_state: st.session_state.user = None
db = load_json(DB_FILE)
content = load_json(CONTENT_FILE)

# ==========================================
# מסך התחברות
# ==========================================
if st.session_state.user is None:
    st.title("🌌 NEXUS ACADEMY - אנגלית חווייתית")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔑 שחקן חוזר")
        name = st.selectbox("בחר את השם שלך מתוך הרשימה:", list(db.keys()) if db else ["אין משתמשים רשומים"])
        if st.button("התחבר והמשך 🚀", use_container_width=True):
            if name in db:
                st.session_state.user = db[name]
                st.rerun()
                
    with col2:
        st.subheader("✨ שחקן חדש")
        new_name = st.text_input("הכנס שם משתמש חדש:")
        new_age = st.number_input("בן כמה אתה?", 7, 15, 12)
        if st.button("צור משתמש והתחל 🎮", use_container_width=True):
            if new_name and new_name not in db:
                db[new_name] = {"name": new_name, "age": new_age, "level": 1, "sub_level": 0, "rewards": []}
                save_json(DB_FILE, db)
                st.session_state.user = db[new_name]
                st.rerun()
            elif new_name in db:
                st.error("השם כבר תפוס! בחר שם אחר.")

# ==========================================
# מסך המשחק הראשי
# ==========================================
else:
    user = st.session_state.user
    
    # תפריט צד (מוצג בבירור בזכות העיצוב המובנה)
    with st.sidebar:
        st.header(f"🕵️‍♂️ {user['name']}")
        st.write(f"**גיל מוגדר:** {user['age']}")
        st.write(f"**שלב נוכחי:** {user['level']} מתוך 99")
        st.progress(user['level'] / 99)
        
        st.markdown("---")
        st.subheader("🎒 ארון הפרסים שלי")
        st.caption("מרוויחים פרס אגדי בכל 10 שלבים!")
        if not user.get('rewards'):
            st.info("עדיין אין פרסים. המשך לשחק!")
        else:
            for r in user['rewards']:
                st.success(f"🎁 {r}")
        
        st.markdown("---")
        if st.button("התנתק 🚪", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # שליפת המשימה בהתאם לגיל ולשלב (הגדרת רמות קושי)
    if user['age'] <= 9: age_group = "7-9"
    elif user['age'] <= 12: age_group = "10-12"
    else: age_group = "13-15"
    
    lvl = str(user['level'])
    sub = str(user['sub_level'])
    
    try: mission = content[age_group][lvl][sub]
    except KeyError:
        st.error("שגיאה בטעינת השלב.")
        st.stop()

    # תצוגת התקדמות במשימות בתוך השלב (1 עד 8)
    st.subheader(f"שלב {lvl} • משימה {int(sub)+1} מתוך 8")
    progress_val = (int(sub)) / 8.0
    st.progress(progress_val)
    st.markdown("---")

    # אזור התוכן הראשי (אינטראקטיבי ותלוי סוג משימה)
    st.markdown(f"<h2>{mission['q']}</h2>", unsafe_allow_html=True)
    st.write("") # מרווח
    
    # אם יש קטע קריאה (Unseen)
    if "unseen" in mission:
        st.markdown(f'<div class="unseen-box"><strong>📖 Reading Text:</strong><br><br>{mission["unseen"]}</div>', unsafe_allow_html=True)
        
    # אם יש וידאו
    if "video_url" in mission:
        st.video(mission["video_url"])
        st.caption("צפה בווידאו ולאחר מכן ענה על השאלה.")

    # בחירת התשובה
    ans = st.radio("בחר את התשובה הנכונה:", mission["options"], index=None, key=f"q_{lvl}_{sub}")

    st.write("") # מרווח
    st.write("")

    # כפתור בדיקה
    if st.button("בצע בדיקה ✔️", type="primary", use_container_width=True):
        if ans == mission["a"]:
            st.success("✅ מעולה! תשובה נכונה.")
            time.sleep(1)
            
            user['sub_level'] += 1
            
            # אם סיים 8 משימות ועובר שלב
            if user['sub_level'] > 7:
                # מתן פרס כל 10 שלבים
                if user['level'] % 10 == 0:
                    st.balloons()
                    reward = f"גביע מיוחד של שלב {user['level']}! 🏆"
                    if "rewards" not in user: user["rewards"] = []
                    user["rewards"].append(reward)
                    st.success(f"🎉 כל הכבוד! השלמת 10 שלבים ברצף וזכית ב: {reward}")
                    time.sleep(3)
                    
                user['level'] += 1
                user['sub_level'] = 0
                
                # סיום המשחק (99 שלבים) - עליה בקבוצת גיל
                if user['level'] > 99:
                    st.balloons()
                    if user['age'] <= 9: user['age'] = 11
                    elif user['age'] <= 12: user['age'] = 14
                    st.success("👑 מדהים! סיימת את כל 99 השלבים! עלית אוטומטית לקבוצת הגיל ולרמת הקושי הבאה!")
                    user['level'] = 1
                    time.sleep(4)

            # שמירה במסד הנתונים ורענון
            db[user['name']] = user
            save_json(DB_FILE, db)
            st.rerun()
            
        elif ans is not None:
            st.error("❌ התשובה לא מדויקת, נסה שוב!")
