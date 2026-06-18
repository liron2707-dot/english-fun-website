import streamlit as st

# הגדרות עיצוב כלליות של הדף (צריך להיות בשורה הראשונה)
st.set_page_config(page_title="Learn English!", page_icon="🎓", layout="centered")

# כותרת האתר ועיצוב עם אמוג'יס
st.title("🌟 English is Fun! 🌟")
st.subheader("האתר המוביל ללימוד אנגלית חווייתי לילדים")
st.write("---")

# 1. ניהול זיכרון האפליקציה (שמירת נתוני המשתמש שלא יימחקו בריענון)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 10

# 2. מסך כניסה/הרשמה
if not st.session_state.logged_in:
    st.markdown("### 👋 ברוכים הבאים! בואו נתחיל את המסע שלנו")
    
    # תיבות קלט מהמשתמש
    name = st.text_input("מה השם שלך?", value=st.session_state.user_name)
    age = st.slider("בן/בת כמה את/ה?", min_value=10, max_value=15, value=st.session_state.user_age)
    
    if st.button("🚀 כניסה לעולם האנגלית!", use_container_width=True):
        if name.strip() == "":
            st.warning("בבקשה תכתוב את השם שלך כדי שנוכל לשמור את ההתקדמות!")
        else:
            st.session_state.user_name = name
            st.session_state.user_age = age
            st.session_state.logged_in = True
            st.rerun()

# 3. מסך הלמידה הראשי (מופיע רק אחרי התחברות)
else:
    # סרגל עליון עם פרטי הילד והניקוד
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"👤 **תלמיד/ה:** {st.session_state.user_name}")
    with col2:
        # קביעת הרמה לפי הגיל באופן אוטומטי
        if st.session_state.user_age in [10, 11]:
            level = "רמה 1 (מתחילים)"
        elif st.session_state.user_age in [12, 13]:
            level = "רמה 2 (בינוניים)"
        else:
            level = "רמה 3 (מתקדמים)"
        st.markdown(f"📊 **רמה:** {level}")
    with col3:
        st.markdown(f"🏆 **ניקוד צבור:** {st.session_state.score} נקודות")
        
    if st.button("יציאה מהחשבון ↩️"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.write("---")
    
    # יצירת טאבים (לשוניות) לתכנים השונים של האתר
    tab_vocab, tab_games, tab_grammar, tab_unseen = st.tabs([
        "📚 אוצר מילים ומשפטים", 
        "🎮 משחקי למידה", 
        "✍️ דקדוק וקריאה", 
        "📖 אנסין (הבנת הנקרא)"
    ])
    
    # --- טאב 1: אוצר מילים ---
    with tab_vocab:
        st.header("מילון המילים המאויר שלך")
        st.write("לחץ על המילים כדי ללמוד איך אומרים אותן!")
        
        # התאמת התוכן לפי רמת הגיל
        if "רמה 1" in level:
            words = {"Apple": "תפוח 🍎", "Dog": "כלב 🐶", "Book": "ספר 📚", "School": "בית ספר 🏫"}
        elif "רמה 2" in level:
            words = {"Adventure": "הרפתקה 🗺️", "Beautiful": "יפה 🌸", "Challenge": "אתגר 🎯", "Journey": "מסע 🚂"}
        else:
            words = {"Accomplish": "להשיג/להשלים 🏆", "Consequence": "השלכה/תוצאה ⏳", "Hypothesis": "השערה 🔬", "Generous": "נדיב 🤝"}
            
        # הצגת המילים בטבלה מעוצבת
        for eng, heb in words.items():
            col_e, col_h = st.columns(2)
            with col_e:
                st.info(f"**{eng}**")
            with col_h:
                st.success(f"**{heb}**")

    # --- טאב 2: משחקים ---
    with tab_games:
        st.header("משחק הטריוויה הגדול!")
        st.write("ענו נכון וצברו נקודות לפרופיל שלכם!")
        
        if "רמה 1" in level:
            q = "איך אומרים 'חתול' באנגלית?"
            options = ["Dog", "Cat", "Elephant", "Bird"]
            correct = "Cat"
        else:
            q = "מה הפירוש של המילה 'Suddenly'?"
            options = ["פתאום", "תמיד", "בגלל", "בשביל"]
            correct = "פתאום"
            
        answer = st.radio(q, options)
        
        if st.button("בדיקת תשובה ✔️"):
            if answer == correct:
                st.balloons() # אפקט בלונים חגיגי על המסך!
                st.success("כל הכבוד! תשובה נכונה. הרווחת 10 נקודות!")
                st.session_state.score += 10
            else:
                st.error("אופס, לא נכון. נסה שוב!")

    # --- טאב 3: דקדוק ---
    with tab_grammar:
        st.header("חוקי הזהב של הדקדוק")
        if "רמה 1" in level:
            st.markdown("""
            ### מתי משתמשים ב- Am, Is, Are?
            * **I** הולך תמיד עם **Am** ➡️ *I am a student.*
            * **He / She / It** הולכים עם **Is** ➡️ *She is smart.*
            * **You / We / They** הולכים עם **Are** ➡️ *We are jumping.*
            """)
        else:
            st.markdown("""
            ### Past Simple (עבר פשוט)
            משתמשים בו לפעולות שהסתיימו בעבר. 
            * לרוב הפעלים פשוט נוסיף **ed** בסוף: *Walk ➡️ Walked*
            * ישנם פעלים יוצאי דופן (Irregular Verbs) שצריך לזכור בעל פה: *Go ➡️ Went*
            """)

    # --- טאב 4: אנסין ---
    with tab_unseen:
        st.header("סיפור קצר והבנת הנקרא")
        
        if "רמה 1" in level:
            story = "Tom has a little red ball. He plays with the ball in the park every afternoon. One day, the ball went into a river."
            question = "Where does Tom play with his ball?"
            unseen_options = ["In the school", "In the park", "In his bedroom"]
            unseen_correct = "In the park"
        else:
            story = "Danny and Sarah decided to build a treehouse in their backyard. They gathered wood, nails, and a hammer. It took them three days to finish their project, but they were very proud of the result."
            question = "How long did it take to build the treehouse?"
            unseen_options = ["One day", "Two days", "Three days"]
            unseen_correct = "Three days"
            
        st.markdown(f"> {story}")
        st.write("---")
        unseen_ans = st.selectbox(question, unseen_options)
        
        if st.button("בדוק את האנסין 📖"):
            if unseen_ans == unseen_correct:
                st.snow() # אפקט של שלג יורד!
                st.success("תשובה מדויקת! הבנת הנקרא שלך מצוינת. קיבלת עוד 15 נקודות!")
                st.session_state.score += 15
            else:
                st.error("לא מדויק, כדאי לקרוא את הסיפור שוב בעיון.")
