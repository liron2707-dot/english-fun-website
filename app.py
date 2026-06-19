import streamlit as st
import random

# הגדרות עמוד מתקדמות ומראה נקי
st.set_page_config(
    page_title="Premium English Learning Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# עיצוב קל ב-CSS כדי לשפר את הנראות של כרטיסי השאלות והתפריטים
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stRadio p { font-size: 1.1rem !important; font-weight: 500; }
    .css-1kyx60b { gap: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. מאגר שאלות מורחב ומובנה (Database)
# ==========================================
if 'questions_pool' not in st.session_state:
    st.session_state.questions_pool = [
        # --- GRAMMAR ---
        {"id": 1, "category": "Grammar", "difficulty": "Easy", "q": "What is the past tense of the verb 'go'?", "options": ["went", "gone", "goes", "goings"], "correct": "went", "explanation": "The verb 'go' is irregular. Its simple past form is 'went', while 'gone' is the past participle used with perfect tenses."},
        {"id": 2, "category": "Grammar", "difficulty": "Medium", "q": "If I ___ more time, I would travel around the world.", "options": ["have", "had", "would have", "will have"], "correct": "had", "explanation": "This is a Second Conditional sentence (unreal present/future situation). The structure requires 'If + Simple Past, would + base verb'."},
        {"id": 3, "category": "Grammar", "difficulty": "Hard", "q": "By the time the movie started, we ___ our popcorn.", "options": ["already ate", "have already eaten", "had already eaten", "were already eating"], "correct": "had already eaten", "explanation": "We use the Past Perfect ('had eaten') to describe an action that happened before another action in the past (the movie starting)."},
        
        # --- VOCABULARY ---
        {"id": 4, "category": "Vocabulary", "difficulty": "Easy", "q": "Which of the following words is an antonym (opposite) of 'Huge'?", "options": ["Tiny", "Gigantic", "Massive", "Heavy"], "correct": "Tiny", "explanation": "'Huge' means extremely large. 'Tiny' means extremely small, making it the perfect antonym."},
        {"id": 5, "category": "Vocabulary", "difficulty": "Medium", "q": "The CEO's speech was so ___ that many employees fell asleep.", "options": ["inspiring", "tedious", "articulate", "profound"], "correct": "tedious", "explanation": "'Tedious' means too long, slow, or dull; tiresome. This explains why the employees fell asleep."},
        {"id": 6, "category": "Vocabulary", "difficulty": "Hard", "q": "Her ___ handling of the delicate diplomatic situation averted a major international crisis.", "options": ["adroit", "clumsy", "negligent", "impulsive"], "correct": "adroit", "explanation": "'Adroit' means clever or skillful in using the hands or mind. An adroit handling of a situation means it was done skillfully."},
        
        # --- IDIOMS & PHRASES ---
        {"id": 7, "category": "Idioms", "difficulty": "Easy", "q": "What does the idiom 'Piece of cake' mean?", "options": ["Something very delicious", "Something very easy", "A birthday celebration", "To share a secret"], "correct": "Something very easy", "explanation": "When something is a 'piece of cake', it means it requires very little effort to complete successfully."},
        {"id": 8, "category": "Idioms", "difficulty": "Medium", "q": "If someone tells you to 'bite the bullet', what are they asking you to do?", "options": ["To eat something hard", "To face a difficult situation with courage", "To get angry and violent", "To stop talking immediately"], "correct": "To face a difficult situation with courage", "explanation": "'Bite the bullet' means to endure a painful or otherwise difficult situation that is seen as unavoidable."},
        {"id": 9, "category": "Idioms", "difficulty": "Hard", "q": "What is the meaning of the phrase 'to steal someone's thunder'?", "options": ["To predict a storm before anyone else", "To take credit for someone else's achievements or ideas", "To make a lot of noise during a presentation", "To make someone feel deeply sad"], "correct": "To take credit for someone else's achievements or ideas", "explanation": "Stealing someone's thunder means lessening their success or praise by doing or saying what they intended to do or say first."}
    ]

# ==========================================
# 2. אתחול משתני הסטייט (Session State)
# ==========================================
if 'used_questions' not in st.session_state: st.session_state.used_questions = set()
if 'current_question' not in st.session_state: st.session_state.current_question = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'max_streak' not in st.session_state: st.session_state.max_streak = 0
if 'answered_current' not in st.session_state: st.session_state.answered_current = False
if 'user_choice' not in st.session_state: st.session_state.user_choice = None

# שמירת היסטוריית ביצועים לצורך דו"ח סיום מפורט
if 'quiz_history' not in st.session_state: st.session_state.quiz_history = []


# ==========================================
# 3. פונקציות עזר לניהול זרימת המשחק
# ==========================================
def get_filtered_questions(cat_filter, diff_filter):
    """מסננת את מאגר השאלות לפי הבחירות של המשתמש בסיידבר"""
    return [
        q for q in st.session_state.questions_pool
        if (cat_filter == "All" or q['category'] == cat_filter) and
           (diff_filter == "All" or q['difficulty'] == diff_filter)
    ]

def load_next_question(cat_filter, diff_filter):
    """מגרילה את השאלה הבאה מתוך השאלות הזמינות שעוד לא נענו בסינון הנוכחי"""
    all_filtered = get_filtered_questions(cat_filter, diff_filter)
    available = [q for q in all_filtered if q['id'] not in st.session_state.used_questions]
    
    if available:
        st.session_state.current_question = random.choice(available)
        st.session_state.answered_current = False
        st.session_state.user_choice = None
    else:
        st.session_state.current_question = None

def reset_quiz():
    """איפוס מוחלט של כל נתוני המשתמש וההיסטוריה"""
    st.session_state.used_questions.clear()
    st.session_state.quiz_history.clear()
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.current_question = None


# ==========================================
# 4. עיצוב סיידבר (Sidebar) - הגדרות וסטטיסטיקה
# ==========================================
with st.sidebar:
    st.header("⚙️ Quiz Settings")
    
    # מסננים המשפיעים דינמית על המשחק
    category_filter = st.selectbox("Select Category:", ["All", "Grammar", "Vocabulary", "Idioms"])
    difficulty_filter = st.selectbox("Select Difficulty:", ["All", "Easy", "Medium", "Hard"])
    
    st.write("---")
    st.header("📊 Performance Dashboard")
    
    # הצגת נתונים בזמן אמת בצד המסך
    st.metric(label="Total Points", value=st.session_state.score)
    
    # תצוגת רצף תשובות נכונות (Streak) עם אמוג'י אש דינמי
    streak_emoji = "🔥" if st.session_state.streak > 0 else "❄️"
    st.metric(label=f"Current Streak {streak_emoji}", value=st.session_state.streak)
    st.caption(f"Highest Streak this session: {st.session_state.max_streak}")
    
    st.write("---")
    if st.button("Reset All Progress 🔄", use_container_width=True, type="secondary"):
        reset_quiz()
        st.rerun()


# ==========================================
# 5. גוף המערכת הראשי (Main UI)
# ==========================================
st.title("🎓 Smart English Learning Center")
st.write("תרגול אנגלית מתקדם ללא כפילויות וללא קפיצות מסך. בחר קטגוריה בצד והתחל לענות!")
st.write("---")

# שליפת השאלות הרלוונטיות לפי הסינון הנוכחי בסיידבר
filtered_pool = get_filtered_questions(category_filter, difficulty_filter)
total_filtered_count = len(filtered_pool)

# חישוב התקדמות בתוך הסינון הנוכחי
used_in_filtered = [q for q in filtered_pool if q['id'] in st.session_state.used_questions]
progress_count = len(used_in_filtered)

# בדיקה: אם אין שאלה טעונה בסטייט, והמשחק לא נגמר, נטען אחת
if st.session_state.current_question is None and progress_count < total_filtered_count:
    load_next_question(category_filter, difficulty_filter)

# הצגת סרגל התקדמות עילי
if total_filtered_count > 0:
    progress_percentage = progress_count / total_filtered_count
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.progress(progress_percentage)
    with col_b:
        st.write(f"Completed: {progress_count}/{total_filtered_count}")
else:
    st.info("No questions found matching the selected filters. Please adjust your settings in the sidebar.")

st.write("")

# לוגיקת הצגת השאלה
if st.session_state.current_question:
    q_data = st.session_state.current_question
    
    # תגיות מידע מעל השאלה (קטגוריה ורמת קושי)
    col_tag1, col_tag2, _ = st.columns([1, 1, 5])
    with col_tag1:
        st.info(f"📁 {q_data['category']}")
    with col_tag2:
        st.help(f"⚖️ {q_data['difficulty']}")
        
    st.write("")
    st.subheader(f"Question: {q_data['q']}")
    
    # --- מצב א': הגשת תשובה (הטופס נעול ולא זז בלחיצות) ---
    if not st.session_state.answered_current:
        with st.form(key=f"advanced_quiz_form_{q_data['id']}"):
            
            # הבחירה מתחילה ריקה לחלוטין (index=None) כדי למנוע בחירה אוטומטית שגויה
            choice = st.radio(
                "Select the best option from below:",
                q_data['options'],
                index=None,
                key=f"radio_comp_{q_data['id']}"
            )
            
            submit_button = st.form_submit_button(label="Submit Answer ➔", use_container_width=True)
            
            if submit_button:
                if choice is None:
                    st.warning("⚠️ Please select an option before submitting!")
                else:
                    # עדכון מצב הסטייט למצב פידבק
                    st.session_state.user_choice = choice
                    st.session_state.answered_current = True
                    
                    # בדיקת נכונות ועדכון מערכת הניקוד והרצפים
                    is_correct = (choice == q_data['correct'])
                    if is_correct:
                        st.session_state.score += 1
                        st.session_state.streak += 1
                        if st.session_state.streak > st.session_state.max_streak:
                            st.session_state.max_streak = st.session_state.streak
                    else:
                        st.session_state.streak = 0 # איפוס הרצף בטעות
                        
                    # שמירה להיסטוריית המשחק לצורך הדו"ח הסופי
                    st.session_state.quiz_history.append({
                        "question": q_data['q'],
                        "user_answer": choice,
                        "correct_answer": q_data['correct'],
                        "is_correct": is_correct
                    })
                    
                    st.rerun()

    # --- מצב ב': הצגת הפידבק, ההסבר הלימודי וכפתור ההמשך ---
    else:
        # הצגת האפשרויות בצורה סטטית מעוצבת כדי שהמשתמש לא יוכל לשנות את דעתו רגע אחרי הגשה
        for opt in q_data['options']:
            if opt == q_data['correct']:
                st.success(f"🍏 **{opt} (Correct Answer)**")
            elif opt == st.session_state.user_choice:
                st.error(f"🍎 **{opt} (Your Choice)**")
            else:
                st.write(f"⚪ {opt}")
        
        st.write("")
        
        # הודעת סיכום חווייתית לפי ההצלחה
        if st.session_state.user_choice == q_data['correct']:
            st.success(f"🎉 Excellent! You got it right! Current Streak: {st.session_state.streak} consecutive answers.")
        else:
            st.error(f"❌ Unfortunate! The correct answer was: **{q_data['correct']}**")
            
        # הרחבה אקדמית - הסבר מפורט למה התשובה נכונה
        with st.expander("📖 View Educational Explanation & Grammar Rules"):
            st.write(q_data['explanation'])
            
        st.write("---")
        
        # כפתור מעבר יזום לשאלה הבאה
        if st.button("Next Question ➔", type="primary", use_container_width=True):
            st.session_state.used_questions.add(q_data['id'])
            load_next_question(category_filter, difficulty_filter)
            st.rerun()

# --- מסך סיום מורחב: המשתמש סיים את כל השאלות תחת הסינון הנוכחי ---
elif total_filtered_count > 0:
    st.balloons()
    st.success("🏆 Section Completed! You have answered all available questions in this category.")
    
    # הצגת כרטיסי סיכום מעוצבים
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric(label="Final Score", value=f"{st.session_state.score} Points")
    with col_res2:
        st.metric(label="Max Streak Reached", value=f"{st.session_state.max_streak} 🔥")
    with col_res3:
        success_rate = (st.session_state.score / total_filtered_count) * 100 if total_filtered_count > 0 else 0
        st.metric(label="Success Rate", value=f"{success_rate:.1f}%")
        
    st.write("---")
    st.subheader("📋 Detailed Performance Breakdown")
    st.write("סקור את התשובות שלך כדי ללמוד מטעויות:")
    
    # יצירת טבלת דו"ח מפורטת מתוך ההיסטוריה שנשמרה ב-Session State
    if st.session_state.quiz_history:
        for idx, row in enumerate(st.session_state.quiz_history, 1):
            status_icon = "✅" if row['is_correct'] else "❌"
            with st.container():
                st.write(f"**{idx}. {row['question']}**")
                st.write(f"Your Answer: {row['user_answer']} | Correct Answer: {row['correct_answer']} ({status_icon})")
                st.write("---")
                
    if st.button("Restart This Section 🔄", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()
