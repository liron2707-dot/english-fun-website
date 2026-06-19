import streamlit as st
import random

# הגדרת עמוד מותאמת לילדים עם אמוג'י שמח
st.set_page_config(
    page_title="ממלכת האנגלית של המקצוענים!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# עיצוב מותאם לילדים (CSS) - הגדלת פונטים ותמיכה בימין לשמאל (RTL)
# ==========================================
st.markdown("""
<style>
    /* הגדרת כיוון כללי לימין לשמאל עבור טקסטים בעברית */
    .rtl-text {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* הגדלת פונט התשובות (Radio Buttons) בצורה משמעותית */
    div[data-testid="stRadio"] label p {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #2E4053;
        padding: 5px;
    }
    
    /* הגדלת כותרות השאלות */
    .question-title {
        font-size: 32px !important;
        color: #1A5276;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    /* קופסת פרסים חמודה */
    .prize-box {
        background-color: #FEF9E7;
        border: 2px dashed #F4D03F;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. מאגר השאלות המורחב לילדים (Database)
# ==========================================
if 'questions_pool' not in st.session_state:
    st.session_state.questions_pool = [
        {"id": 1, "category": "חיות 🦁", "q": "What animal is a 'Lion'?", "options": ["אריה", "פיל", "קוף", "חתול"], "correct": "אריה", "hint": "הוא מלך החיות!"},
        {"id": 2, "category": "צבעים 🎨", "q": "Which color is 'Red'?", "options": ["כחול", "ירוק", "צהוב", "אדום"], "correct": "אדום", "hint": "זה הצבע של עגבנייה ותות שדה 🍓"},
        {"id": 3, "category": "מספרים 🔢", "q": "How much is 'One' + 'Two'?", "options": ["Five (5)", "Three (3)", "Four (4)", "Six (6)"], "correct": "Three (3)", "hint": "ספור על האצבעות: 1 ועוד 2"},
        {"id": 4, "category": "אוכל 🍎", "q": "What fruit is an 'Apple'?", "options": ["בננה", "תפוז", "תפוח", "ענבים"], "correct": "תפוח", "hint": "היה לפרי הזה תפקיד חשוב בסיפור של שלגיה!"},
        {"id": 5, "category": "הפכים ↕️", "q": "What is the opposite of 'Big'?", "options": ["Small", "Tall", "Happy", "Strong"], "correct": "Small", "hint": "ההפך מגדול הוא... קטן!"},
        {"id": 6, "category": "בבית 🏠", "q": "Where do you sleep? In a ___", "options": ["Table", "Bed", "Kitchen", "Car"], "correct": "Bed", "hint": "היא נמצאת בחדר השינה שלך ונעים לישון עליה"},
        {"id": 7, "category": "משפחה 👨‍👩‍👦", "q": "Who is your 'Mother'?", "options": ["אבא", "אח", "אמא", "סבתא"], "correct": "אמא", "hint": "האישה הכי יקרה בעולם שדואגת לך"},
        {"id": 8, "category": "ברכות 👋", "q": "What do you say when you meet a friend in the morning?", "options": ["Good night", "Goodbye", "Good morning", "Thank you"], "correct": "Good morning", "hint": "בוקר טוב!"}
    ]

# ==========================================
# 2. אתחול משתני הזיכרון (Session State)
# ==========================================
if 'used_questions' not in st.session_state: st.session_state.used_questions = set()
if 'current_question' not in st.session_state: st.session_state.current_question = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'stars' not in st.session_state: st.session_state.stars = 0  # המטבע של המשחק לקניית פרסים
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'max_streak' not in st.session_state: st.session_state.max_streak = 0
if 'answered_current' not in st.session_state: st.session_state.answered_current = False
if 'user_choice' not in st.session_state: st.session_state.user_choice = None
if 'quiz_history' not in st.session_state: st.session_state.quiz_history = []

# רשימת פרסים שהילד קנה בחנות
if 'my_prizes' not in st.session_state: st.session_state.my_prizes = []


# ==========================================
# 3. פונקציות ניהול המשחק והגרלה
# ==========================================
def load_next_question():
    """בחירת שאלה חדשה באופן אקראי שעוד לא הופיעה"""
    available = [q for q in st.session_state.questions_pool if q['id'] not in st.session_state.used_questions]
    if available:
        st.session_state.current_question = random.choice(available)
        st.session_state.answered_current = False
        st.session_state.user_choice = None
    else:
        st.session_state.current_question = None

# טעינת השאלה הראשונה בריצה הראשונה של האתר
if st.session_state.current_question is None and len(st.session_state.used_questions) == 0:
    load_next_question()


# ==========================================
# 4. תפריט צד (Sidebar) - כוכבים, הישגים וחנות פרסים
# ==========================================
with st.sidebar:
    st.markdown('<div class="rtl-text">', unsafe_allow_html=True)
    st.header("🎒 מרכז הבקרה שלך")
    
    # הצגת כוכבים ונקודות בצורה בולטת לילדים
    st.markdown(f"### ✨ כוכבי קסם שצברת: **{st.session_state.stars}** ⭐")
    st.markdown(f"### 🎯 תשובות נכונות: **{st.session_state.score}**")
    st.markdown(f"### 🔥 רצף נוכחי: **{st.session_state.streak}**")
    st.markdown("---")
    
    # --- לוח הישגים דינמי (Achievements) ---
    st.subheader("🏆 מדף הגביעים שלי")
    if st.session_state.score >= 1:
        st.success("🥇 גביע הניצחון הראשון! (ענית נכון)")
    if st.session_state.max_streak >= 3:
        st.warning("🔥 אלוף הרצפים! (3 תשובות נכונות ברצף)")
    if len(st.session_state.used_questions) >= 5:
        st.info("🧠 המדען המתמיד! (פתרת כבר 5 שאלות)")
    if len(st.session_state.my_prizes) >= 1:
        st.error("🛍️ קונה מיומן! (קנית פרס ראשון בחנות)")
    if st.session_state.score == 0 and st.session_state.max_streak < 3:
        st.caption("כאן יופיעו הגביעים שלך ככל שתענה נכון! 🏆")
        
    st.write("---")
    
    # --- חנות פרסים וירטואלית ---
    st.subheader("🛍️ חנות הפרסים של הממלכה")
    st.write("החלף את כוכבי הקסם שלך בפרסים אמיתיים באתר!")
    
    shop_items = [
        {"name": "🍦 גלידת פיסטוק ענקית", "cost": 20},
        {"name": "🐉 דרקון מחמד חמוד", "cost": 40},
        {"name": "🚀 חללית טסלה לירח", "cost": 60},
        {"name": "👑 כתר של מלך האנגלית", "cost": 100}
    ]
    
    for item in shop_items:
        disabled_btn = st.session_state.stars < item['cost'] or item['name'] in st.session_state.my_prizes
        btn_text = f"קנה ב-{item['cost']} ⭐" if item['name'] not in st.session_state.my_prizes else "ברשותך! ✅"
        
        col_item, col_btn = st.columns([1.5, 1])
        with col_item:
            st.write(f"**{item['name']}**")
        with col_btn:
            if st.button(btn_text, key=f"buy_{item['name']}", disabled=disabled_btn):
                st.session_state.stars -= item['cost']
                st.session_state.my_prizes.append(item['name'])
                st.toast(f"איזה כיף! קנית {item['name']}! 🎉")
                st.rerun()
                
    # תצוגת הצעצועים שהילד כבר קנה
    if st.session_state.my_prizes:
        st.write("---")
        st.subheader("🧸 תיבת הצעצועים שלי:")
        prizes_html = "".join([f"<span style='font-size:25px;'>{p.split()[0]}</span> " for p in st.session_state.my_prizes])
        st.markdown(prizes_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 5. גוף המערכת הראשי (Main UI)
# ==========================================
st.markdown('<div class="rtl-text">', unsafe_allow_html=True)
st.title("👑 ממלכת האנגלית של הילדים 👑")
st.markdown("### בואו נשחק, נצבור כוכבי קסם ⭐ ונזכה בפרסים מדהימים!")
st.markdown("---")
st.markdown('</div>', unsafe_allow_html=True)

# חישוב התקדמות כללי
total_q = len(st.session_state.questions_pool)
current_progress = len(st.session_state.used_questions)

# סרגל התקדמות צבעוני
st.progress(current_progress / total_q)
st.write(f"✨ שאלה {min(current_progress + 1, total_q)} מתוך {total_q}")

st.write("")

# הצגת המשחק או מסך הסיום קצה
if st.session_state.current_question:
    q_data = st.session_state.current_question
    
    # כותרת השאלה וקטגוריה (מתחיל מימין)
    st.markdown(f'<div class="rtl-text"><span style="background-color:#D4E6F1; padding:5px 15px; border-radius:10px; font-weight:bold;">{q_data["category"]}</span></div>', unsafe_allow_html=True)
    st.write("")
    
    # השאלה עצמה באנגלית - מוצגת בנפרד בצורה ברורה
    st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-title">{q_data["q"]}</div>', unsafe_allow_html=True)
    
    # --- מצב א': בחירת תשובה (נעול בתוך טופס קבוע שלא זז) ---
    if not st.session_state.answered_current:
        with st.form(key=f"kids_form_{q_data['id']}"):
            
            # רדיו בטנס עם פונט מוגדל (הגדרנו ב-CSS למעלה)
            choice = st.radio(
                "מה התשובה הנכונה לדעתך?",
                q_data['options'],
                index=None,
                key=f"radio_kids_{q_data['id']}"
            )
            
            # כפתור הגשה מעוצב וגדול
            st.markdown('<div class="rtl-text">', unsafe_allow_html=True)
            submit_button = st.form_submit_button(label="בדיקה! הבא לי כוכבים ➔", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit_button:
                if choice is None:
                    st.warning("אופס! שכחת לבחור תשובה. לחץ על אחת האפשרויות קודם 🎈")
                else:
                    st.session_state.user_choice = choice
                    st.session_state.answered_current = True
                    
                    # בדיקה אם צדק
                    if choice == q_data['correct']:
                        st.session_state.score += 1
                        st.session_state.stars += 20  # פרס של 20 כוכבים על תשובה נכונה!
                        st.session_state.streak += 1
                        if st.session_state.streak > st.session_state.max_streak:
                            st.session_state.max_streak = st.session_state.streak
                    else:
                        st.session_state.streak = 0  # איפוס הרצף בטעות
                        
                    st.session_state.quiz_history.append({
                        "q": q_data['q'],
                        "user": choice,
                        "correct": q_data['correct'],
                        "status": (choice == q_data['correct'])
                    })
                    st.rerun()
                    
        # רמז חמוד לילד אם הוא מתקשה
        with st.expander("💡 צריך רמז סודי? לחץ כאן!"):
            st.markdown(f'<div class="rtl-text">{q_data["hint"]}</div>', unsafe_allow_html=True)

    # --- מצב ב': פידבק סטטי קבוע + לחצן מעבר שאלה ---
    else:
        st.markdown('<div class="rtl-text">', unsafe_allow_html=True)
        
        # הצגת האפשרויות בצורה ויזואלית קבועה מבלי שיוכל לשנות
        for opt in q_data['options']:
            if opt == q_data['correct']:
                st.success(f"🟢 **{opt} (זו התשובה הנכונה והמדויקת!)**")
            elif opt == st.session_state.user_choice:
                st.error(f"🔴 **{opt} (הבחירה שלך)**")
            else:
                st.write(f"⚪ {opt}")
                
        st.write("")
        
        # אפקטים והודעות שמחה לפי התוצאה
        if st.session_state.user_choice == q_data['correct']:
            st.balloons()  # בלוני שמחה עפים במסך!
            st.markdown("## 🎉 כל הכבוד! צדקת והרווחת **20 כוכבי קסם!** ⭐")
        else:
            st.markdown(f"## 🌟 לא נורא, בפעם הבאה בטוח תצליח! התשובה הנכונה היא: **{q_data['correct']}**")
            
        st.write("---")
        
        # כפתור מעבר יזום לשאלה הבאה (בולט וגדול)
        if st.button("קדימה, לשאלה הבאה! 🚀", type="primary", use_container_width=True):
            st.session_state.used_questions.add(q_data['id'])
            load_next_question()
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- מסך סיום המשחק: נגמרו השאלות במאגר ---
else:
    st.snow()  # אפקט של פתיתי שלג חגיגיים
    st.markdown('<div class="rtl-text" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("# 🏆 אלופי הממלכה! סיימתם את כל השאלות! 🏆")
    st.markdown(f"## הצלחתם לצבור **{st.session_state.score}** נקודות מתוך **{total_q}**!")
    st.markdown(f"## סך הכל יש לכם **{st.session_state.stars}** כוכבי קסם לקניות בחנות! ⭐")
    
    # הצגת הפרסים המפוארים שהילד השיג
    if st.session_state.my_prizes:
        st.markdown("### 🧸 הנה הפרסים שהצלחת להשיג בתיבת הצעצועים שלך:")
        prizes_list_str = " | ".join(st.session_state.my_prizes)
        st.markdown(f"#### **{prizes_list_str}**")
        
    st.write("---")
    st.subheader("📋 סיכום המשחק שלך (כדי ללמוד ולהשתפר):")
    
    for idx, hist in enumerate(st.session_state.quiz_history, 1):
        icon = "✅" if hist['status'] else "❌"
        st.markdown(f"**{idx}. השאלה:** {hist['q']}")
        st.write(f"התשובה שלך: {hist['user']} | התשובה הנכונה: {hist['correct']} ({icon})")
        st.write("---")
        
    if st.button("אני רוצה לשחק שוב מהתחלה! 🔄", type="primary", use_container_width=True):
        st.session_state.used_questions.clear()
        st.session_state.quiz_history.clear()
        st.session_state.my_prizes.clear()
        st.session_state.score = 0
        st.session_state.stars = 0
        st.session_state.streak = 0
        st.session_state.max_streak = 0
        st.session_state.current_question = None
        load_next_question()
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
