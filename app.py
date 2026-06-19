import streamlit as st
import random

# הגדרות עמוד ותמיכה במראה שמח ומותאם לילדים
st.set_page_config(
    page_title="ממלכת האנגלית של המקצוענים!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# עיצוב מתקדם (CSS) - תמיכה בימין לשמאל (RTL), הגדלת פונטים ועיצוב קלפים נדירים
# ==========================================
st.markdown("""
<style>
    /* הגדרת כיוון כללי לימין לשמאל ואלמנטים של האפליקציה */
    .rtl-container {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* העברת הסיידבר לצד ימין ויישור התוכן שלו לימין */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    
    /* הגדלת פונט התשובות (Radio Buttons) בצורה מסיבית לבקשתך */
    div[data-testid="stRadio"] label p {
        font-size: 28px !important;
        font-weight: bold !important;
        color: #1B263B;
        padding: 8px;
    }
    
    /* הגדלת כותרת השאלה */
    .question-box {
        font-size: 34px !important;
        color: #0D1B2A;
        font-weight: 800;
        margin-bottom: 20px;
    }
    
    /* עיצוב ויזואלי מרהיב לקלפי אספנות נדירים בחנות */
    .trading-card-pokemon {
        background: linear-gradient(135deg, #ffcc00, #ff66cc);
        border: 4px solid #fff;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        color: white;
        text-shadow: 1px 1px 2px black;
        margin-bottom: 10px;
    }
    .trading-card-soccer {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        border: 4px solid #e0a96d;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        color: white;
        text-shadow: 1px 1px 2px black;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. בסיס נתונים ומחולל 50 שלבים (400 שאלות)
# ==========================================
if 'initialized_questions' not in st.session_state:
    # רשימת מילים בסיסית עשירה ליצירת עשרות שלבים מגוונים בתבנית קבועה
    vocab_base = [
        {"eng": "Lion", "heb": "אריה", "cat": "חיות 🦁", "hint": "מלך החיות שבועי אגרסיבי"},
        {"eng": "Red", "heb": "אדום", "cat": "צבעים 🎨", "hint": "הצבע של תות שדה ועגבנייה"},
        {"eng": "Apple", "heb": "תפוח", "cat": "אוכל 🍎", "hint": "פרי עגול ומתוק שיש על העץ"},
        {"eng": "Bed", "heb": "מיטה", "cat": "בבית 🏠", "hint": "עליה אנחנו הולכים לישון בלילה"},
        {"eng": "Mother", "heb": "אמא", "cat": "משפחה 👨‍👩‍👦", "hint": "האישה הכי יקרה שדואגת לך"},
        {"eng": "Dog", "heb": "כלב", "cat": "חיות 🦁", "hint": "חבר טוב שהולך על ארבע ונובח"},
        {"eng": "Green", "heb": "ירוק", "cat": "צבעים 🎨", "hint": "הצבע של הדשא והמלפפון"},
        {"eng": "Banana", "heb": "בננה", "cat": "אוכל 🍎", "hint": "פרי צהוב ומתוק שקופים אוהבים"},
        {"eng": "Chair", "heb": "כיסא", "cat": "בבית 🏠", "hint": "עליו אנחנו יושבים ליד השולחן"},
        {"eng": "Father", "heb": "אבא", "cat": "משפחה 👨‍👩‍👦", "hint": "הגבר היקר ששומר עליך ומצחיק אותך"},
        {"eng": "Cat", "heb": "חתול", "cat": "חיות 🦁", "hint": "חיה קטנה שמיללת מיאו ואוהבת חלב"},
        {"eng": "Blue", "heb": "כחול", "cat": "צבעים 🎨", "hint": "הצבע של השמיים ושל הים"},
        {"eng": "Milk", "heb": "חלב", "cat": "אוכל 🍎", "hint": "המשקה הלבן ששמים בקורנפלקס"},
        {"eng": "Table", "heb": "שולחן", "cat": "בבית 🏠", "hint": "עליו שמים את הצלחת כשאוכלים"},
        {"eng": "Sister", "heb": "אחות", "cat": "משפחה 👨‍👩‍👦", "hint": "הבת של אמא ואבא שלך"},
        {"eng": "Elephant", "heb": "פיל", "cat": "חיות 🦁", "hint": "החיה הכי גדולה ביבשה עם חדק ארוך"},
        {"eng": "Yellow", "heb": "צהוב", "cat": "צבעים 🎨", "hint": "הצבע של השמש ושל הלימון"},
        {"eng": "Bread", "heb": "לחם", "cat": "אוכל 🍎", "hint": "ממנו אמא מכינה לך סנדוויץ' לבית הספר"},
        {"eng": "Door", "heb": "דלת", "cat": "בבית 🏠", "hint": "פותחים אותה כדי להיכנס לחדר"},
        {"eng": "Brother", "heb": "אח", "cat": "משפחה 👨‍👩‍👦", "hint": "הבן של אמא ואבא שלך"}
    ]
    
    # מילים נוספות להרחבה אוטומטית ל-50 שלבים (כל שלב יקבל 8 שאלות ייחודיות)
    extra_words = [
        ("Sun", "שמש"), ("Moon", "ירח"), ("Star", "כוכב"), ("Sky", "שמיים"), ("Water", "מים"),
        ("Fire", "אש"), ("Tree", "עץ"), ("Flower", "פרח"), ("Bird", "ציפור"), ("Fish", "דג"),
        ("Book", "ספר"), ("Pen", "עט"), ("School", "בית ספר"), ("Teacher", "מורה"), ("Boy", "ילד"),
        ("Girl", "ילדה"), ("Happy", "שמח"), ("Sad", "עצוב"), ("Big", "גדול"), ("Small", "קטן"),
        ("Hot", "חם"), ("Cold", "קר"), ("Good", "טוב"), ("Bad", "רע"), ("Fast", "מהיר"),
        ("Slow", "איטי"), ("Day", "יום"), ("Night", "לילה"), ("Morning", "בוקר"), ("Evening", "ערב"),
        ("Car", "מכונית"), ("Bike", "אופניים"), ("Ball", "כדור"), ("Game", "משחק"), ("Toy", "צעצוע"),
        ("House", "בית"), ("Room", "חדר"), ("Window", "חלון"), ("Clock", "שעון"), ("Shoes", "נעליים"),
        ("Hat", "כובע"), ("Shirt", "חולצה"), ("Hand", "יד"), ("Foot", "רגל"), ("Head", "ראש"),
        ("Eye", "עין"), ("Ear", "אוזן"), ("Mouth", "פה"), ("Nose", "אף"), ("Hair", "שיער")
    ]
    
    # שכפול וגיוון ליצירת 400 שאלות ייחודיות (50 שלבים * 8 שאלות)
    all_generated = []
    q_id = 1
    
    # שלב ראשון מוזן ידנית מהרשימה העשירה
    for item in vocab_base:
        # מייצרים מסיחים (תשובות שגויות) מתוך מאגר המילים בעברית
        distractors = list(set([x['heb'] for x in vocab_base if x['heb'] != item['heb']]))
        options = [item['heb']] + random.sample(distractors, 3)
        random.shuffle(options)
        
        all_generated.append({
            "id": q_id,
            "q": f"What is the meaning of the word '{item['eng']}'?",
            "options": options,
            "correct": item['heb'],
            "hint": item['hint']
        })
        q_id += 1

    # השלמת שאר השאלות ל-50 שלבים מלאים
    for eng, heb in extra_words * 8:
        if len(all_generated) >= 400:
            break
        distractors = list(set([x[1] for x in extra_words if x[1] != heb]))
        options = [heb] + random.sample(distractors, 3)
        random.shuffle(options)
        
        all_generated.append({
            "id": q_id,
            "q": f"What is the meaning of the word '{eng}'?",
            "options": options,
            "correct": heb,
            "hint": f"מילה נהדרת באנגלית שפירושה בעברית הוא {heb}!"
        })
        q_id += 1
        
    st.session_state.questions_pool = all_generated
    st.session_state.initialized_questions = True


# ==========================================
# 2. ניהול מערכת המשתמשים (התחברות ושמירת התקדמות)
# ==========================================
if 'user_db' not in st.session_state:
    # בסיס נתונים מקומי פיקטיבי ששומר את כל הנתונים של כל משתמש
    st.session_state.user_db = {}

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# פונקציות לסנכרון נתונים
def save_user_progress():
    username = st.session_state.logged_in_user
    if username:
        st.session_state.user_db[username] = {
            "score": st.session_state.score,
            "stars": st.session_state.stars,
            "current_stage": st.session_state.current_stage,
            "current_q_index": st.session_state.current_q_index,
            "streak": st.session_state.streak,
            "max_streak": st.session_state.max_streak,
            "my_prizes": st.session_state.my_prizes,
            "quiz_history": st.session_state.quiz_history
        }

def load_user_progress(username):
    data = st.session_state.user_db[username]
    st.session_state.score = data["score"]
    st.session_state.stars = data["stars"]
    st.session_state.current_stage = data["current_stage"]
    st.session_state.current_q_index = data["current_q_index"]
    st.session_state.streak = data["streak"]
    st.session_state.max_streak = data["max_streak"]
    st.session_state.my_prizes = data["my_prizes"]
    st.session_state.quiz_history = data["quiz_history"]
    st.session_state.answered_current = False
    st.session_state.user_choice = None


# ==========================================
# 3. מסך ראשון: התחברות / הרשמה (Login Screen)
# ==========================================
if st.session_state.logged_in_user is None:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("🔐 ברוכים הבאים לממלכת האנגלית!")
    st.subheader("התחברו או הירשמו כדי לשמור את השלבים והפרסים שלכם תמיד!")
    
    tab_login, tab_register = st.tabs(["👋 משתמש קיים (התחברות)", "✨ משתמש חדש (הרשמה)"])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("שם משתמש:")
            password = st.text_input("סיסמה:", type="password")
            btn_login = st.form_submit_button("היכנס למשחק 🚀")
            
            if btn_login:
                if username in st.session_state.user_db and st.session_state.user_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    load_user_progress(username)
                    st.success(f"איזה כיף שחזרת אלינו, {username}! טוען את השלב שלך...")
                    st.rerun()
                else:
                    st.error("שם משתמש או סיסמה לא נכונים, או שעליך להירשם קודם!")
                    
    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("בחר שם משתמש חדש:")
            new_password = st.text_input("בחר סיסמה:", type="password")
            btn_reg = st.form_submit_button("צור משתמש חדש והתחל לשחק 🎉")
            
            if btn_reg:
                if not new_username or not new_password:
                    st.warning("נא למלא את כל השדות!")
                elif new_username in st.session_state.user_db:
                    st.error("שם המשתמש הזה כבר תפוס, בחר שם אחר.")
                else:
                    # יצירת פרופיל מאופס לחלוטיัน עבור המשתמש החדש
                    st.session_state.user_db[new_username] = {
                        "password": new_password, "score": 0, "stars": 0, "current_stage": 1,
                        "current_q_index": 0, "streak": 0, "max_streak": 0, "my_prizes": [], "quiz_history": []
                    }
                    st.session_state.logged_in_user = new_username
                    load_user_progress(new_username)
                    st.success("החשבון נוצר בהצלחה! ברוך הבא לממלכה!")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop() # עוצר את הרצת המשחק עד להתחברות קודמת


# ==========================================
# 4. תפריט בקרה ימני (Sidebar) - מוזז ומעוצב לימין (RTL)
# ==========================================
with st.sidebar:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.header(f"🎒 שלום, {st.session_state.logged_in_user}!")
    
    # נתונים נוכחיים
    st.markdown(f"### ✨ כוכבי קסם: **{st.session_state.stars}** ⭐")
    st.markdown(f"### 🆙 שלב נוכחי: **{st.session_state.current_stage}** / 50")
    st.markdown(f"### 🔥 רצף נוכחי: **{st.session_state.streak}**")
    st.write("---")
    
    # --- חנות פרסים רגילים וקלפים נדירים נעולים לפי שלבים ---
    st.subheader("🛍️ חנות הפרסים של הממלכה")
    st.write("אסוף מספיק כוכבים ועבור שלבים כדי לפתוח קלפי אספנות יקרים!")
    
    shop_items = [
        {"name": "🍦 גלידת פיסטוק ענקית", "cost": 20, "req_stage": 1, "type": "normal"},
        {"name": "🐉 דרקון מחמד חמוד", "cost": 40, "req_stage": 1, "type": "normal"},
        # קלפים נדירים נעולים לפי שלב
        {"name": "🔥 קלף פוקימון Charizard VMAX נדיר!", "cost": 100, "req_stage": 5, "type": "pokemon"},
        {"name": "⚡ קלף פוקימון Pikachu Gold Star מוזהב", "cost": 150, "req_stage": 5, "type": "pokemon"},
        {"name": "⚽ חפיסת קלפי Adrenalyn XL - מהדורת זהב", "cost": 200, "req_stage": 10, "type": "soccer"},
        {"name": "🏆 קלף פקטורי מוזהב Match Attax - מהדורה מוגבלת", "cost": 300, "req_stage": 20, "type": "soccer"}
    ]
    
    for item in shop_items:
        is_locked = st.session_state.current_stage < item['req_stage']
        is_owned = item['name'] in st.session_state.my_prizes
        
        # חישוב סטטוס הכפתור
        disabled_btn = st.session_state.stars < item['cost'] or is_owned or is_locked
        
        if is_locked:
            btn_text = f"🔒 נפתח בשלב {item['req_stage']}"
        elif is_owned:
            btn_text = "ברשותך! ✅"
        else:
            btn_text = f"קנה ב-{item['cost']} ⭐"
            
        st.write(f"**{item['name']}**")
        
        # תצוגה ויזואלית של הקלפים בתוך החנות אם השלב פתוח
        if not is_locked and item['type'] == 'pokemon':
            st.markdown(f'<div class="trading-card-pokemon">⭐ POKÉMON CARD ⭐<br><b>{item["name"].split("!")[0]}</b></div>', unsafe_allow_html=True)
        elif not is_locked and item['type'] == 'soccer':
            st.markdown(f'<div class="trading-card-soccer">⚽ MATCH ATTAX / ADRENALYN ⚽<br><b>{item["name"]}</b></div>', unsafe_allow_html=True)
            
        if st.button(btn_text, key=f"buy_{item['name']}", disabled=disabled_btn, use_container_width=True):
            st.session_state.stars -= item['cost']
            st.session_state.my_prizes.append(item['name'])
            save_user_progress()
            st.toast(f"איזה כיף! קנית {item['name']}! 🎉")
            st.rerun()
        st.write("")
            
    # אלבום הקלפים והפרסים שהילד קנה
    if st.session_state.my_prizes:
        st.write("---")
        st.subheader("🧸 אוסף הבונוסים שלי:")
        for prize in st.session_state.my_prizes:
            st.markdown(f"• {prize}")
            
    st.write("---")
    if st.button("התנתק ושמור התקדמות 🚪", use_container_width=True):
        save_user_progress()
        st.session_state.logged_in_user = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 5. גוף המערכת הראשי (Main UI Game System)
# ==========================================
st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
st.title("👑 ממלכת האנגלית של הילדים 👑")
st.markdown(f"### שלב נוכחי: **שלב {st.session_state.current_stage}**")
st.markdown('</div>', unsafe_allow_html=True)

# חישוב מיקום השאלה הנוכחית בתוך השלב (8 שאלות לכל שלב)
questions_per_stage = 8
start_idx = (st.session_state.current_stage - 1) * questions_per_stage
current_q_global_idx = start_idx + st.session_state.current_q_index

# בדיקה אם המשתמש סיים את כל 50 השלבים
if st.session_state.current_stage > 50:
    st.snow()
    st.markdown('<div class="rtl-container" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("# 🏆 אלופי העולם והממלכה! סיימתם את כל 50 השלבים! 🏆")
    st.markdown("קניתם את כל קלפי הפוקימון והכדורגל הנדירים ביותר!")
    if st.button("אני רוצה לאפס הכל ולשחק מהתחלה 🔄"):
        st.session_state.current_stage = 1
        st.session_state.current_q_index = 0
        st.session_state.score = 0
        st.session_state.stars = 0
        st.session_state.my_prizes = []
        st.session_state.quiz_history = []
        save_user_progress()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# שליפת נתוני השאלה הנוכחית
q_data = st.session_state.questions_pool[current_q_global_idx]

# סרגל התקדמות בתוך השלב הנוכחי (מתוך 8)
st.progress(st.session_state.current_q_index / questions_per_stage)
st.write(f"✨ שאלה {st.session_state.current_q_index + 1} מתוך {questions_per_stage} בשלב זה")

st.write("")

# הצגת השאלה עצמה ממורכזת ובאנגלית בצורה ברורה (משמאל לימין רק לשאלה)
st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)

# --- מצב א': בחירה והגשת תשובה ---
if not st.session_state.answered_current:
    with st.form(key=f"kids_stage_form_{q_data['id']}"):
        
        # רדיו בטנס עם פונט ענק (מוגדר ב-CSS)
        choice = st.radio(
            "מה הפירוש הנכון של המילה?",
            q_data['options'],
            index=None,
            key=f"radio_comp_{q_data['id']}"
        )
        
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="בדיקת תשובה וקבלת כוכבים! ➔", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit_button:
            if choice is None:
                st.warning("אופס! שכחת לבחור תשובה. לחץ על אחת האפשרויות הגדולות 🎈")
            else:
                st.session_state.user_choice = choice
                st.session_state.answered_current = True
                
                # בדיקת נכונות
                if choice == q_data['correct']:
                    st.session_state.score += 1
                    st.session_state.stars += 25  # הילד מקבל 25 כוכבים על כל תשובה נכונה
                    st.session_state.streak += 1
                    if st.session_state.streak > st.session_state.max_streak:
                        st.session_state.max_streak = st.session_state.streak
                else:
                    st.session_state.streak = 0
                    
                st.session_state.quiz_history.append({
                    "stage": st.session_state.current_stage,
                    "q": q_data['q'],
                    "user": choice,
                    "correct": q_data['correct'],
                    "status": (choice == q_data['correct'])
                })
                save_user_progress()
                st.rerun()
                
    # רמז בעברית מימין לשמאל
    with st.expander("💡 צריך רמז סודי? לחץ כאן כדי לפתוח"):
        st.markdown(f'<div class="rtl-container">{q_data["hint"]}</div>', unsafe_allow_html=True)

# --- מצב ב': הצגת הפידבק ולחצן התקדמות ---
else:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    
    # תצוגה קבועה שלא ניתנת לשינוי לאחר הגשה
    for opt in q_data['options']:
        if opt == q_data['correct']:
            st.success(f"🟢 **{opt} (זו התשובה הנכונה ביותר!)**")
        elif opt == st.session_state.user_choice:
            st.error(f"🔴 **{opt} (הבחירה שלך)**")
        else:
            st.write(f"⚪ {opt}")
            
    st.write("")
    
    if st.session_state.user_choice == q_data['correct']:
        st.balloons()
        st.markdown("## 🎉 מדהים! צדקתם והרווחתם **25 כוכבי קסם!** ⭐")
    else:
        st.markdown(f"## 🌟 לא נורא, בפעם הבאה תצליחו! התשובה הנכונה היא: **{q_data['correct']}**")
        
    st.write("---")
    
    # כפתור מעבר לשאלה הבאה או לשלב הבא
    if st.button("המשך קדימה לשאלה הבאה! 🚀", type="primary", use_container_width=True):
        st.session_state.current_q_index += 1
        
        # אם סיימנו 8 שאלות - עולים שלב!
        if st.session_state.current_q_index >= questions_per_stage:
            st.session_state.current_stage += 1
            st.session_state.current_q_index = 0
            st.session_state.stars += 100  # בונוס מטורף של 100 כוכבים על סיום שלב!
            st.toast(f"🏆 כל הכבוד! סיימתם את שלב {st.session_state.current_stage - 1} ועליתם שלב!")
            
        st.session_state.answered_current = False
        st.session_state.user_choice = None
        save_user_progress()
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
