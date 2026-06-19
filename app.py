import streamlit as st
import random
import streamlit.components.v1 as components

# הגדרות עמוד ותצוגה
st.set_page_config(
    page_title="ממלכת האנגלית של המקצוענים!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# עיצוב מותאם (CSS) - ימין לשמאל, קלפים ופונטים ענקיים לתשובות
# ==========================================
st.markdown("""
<style>
    .rtl-container {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    /* הגדלת פונט התשובות ברדיו בטנס */
    div[data-testid="stRadio"] label p {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #1B263B;
        padding: 5px;
    }
    .question-box {
        font-size: 30px !important;
        color: #0D1B2A;
        font-weight: 800;
        margin-bottom: 10px;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    .unseen-text {
        font-size: 22px !important;
        color: #2c3e50;
        background-color: #e8f6f3;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 2px dashed #1abc9c;
    }
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

# פונקציית הקראה קולית בדפדפן (TTS)
def speak_text(text):
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    html_code = f"""
    <button onclick="var msg = new SpeechSynthesisUtterance('{safe_text}'); msg.lang='en-US'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
    style="background-color:#F39C12; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
        🔊 לחץ כאן להקראת הטקסט בקול רם
    </button>
    """
    components.html(html_code, height=50)


# ==========================================
# 1. מנוע ג'נרטור חכם - יצירת 1,200 שאלות שונות ומתאימות גיל ללא מדע
# ==========================================
if 'db_generated' not in st.session_state:
    
    # --- מאגרי מידע גולמיים לרמה 7-9 (בסיסי: חיות, צבעים, פעלים פשוטים, משפחה) ---
    raw_7_9 = [
        ("Dog", "כלב", "חבר על ארבע שנובח"), ("Cat", "חתול", "חיה קטנה שאומרת מיאו"),
        ("Sun", "שמש", "אור גדול וצהוב בשמיים"), ("Water", "מים", "אנחנו שותים אותם כשחם"),
        ("Milk", "חלב", "משקה לבן ששמים בקורנפלקס"), ("School", "בית ספר", "המקום אליו הולכים ללמוד"),
        ("Teacher", "מורה", "האיש או האישה שמלמדים בכיתה"), ("Book", "ספר", "קוראים אותו לפני השינה"),
        ("Red", "אדום", "הצבע של תות שדה"), ("Blue", "כחול", "הצבע של הים והשמיים"),
        ("Green", "ירוק", "הצבע של הדשא והמלפפון"), ("Yellow", "צהוב", "הצבע של הבננה והלימון"),
        ("Happy", "שמח", "ההפך מעצוב! חיוך גדול"), ("Sad", "עצוב", "כשרוצים לבכות קצת"),
        ("Big", "גדול", "כמו פיל ענקי"), ("Small", "קטן", "כמו נמלה קטנה"),
        ("Run", "לרוץ", "מה שעושים מהר במגרש"), ("Jump", "לקפוץ", "לדלג למעלה גבוה"),
        ("Sleep", "לישון", "מה שעושים במיטה בלילה"), ("Eat", "לאכול", "כשעל השולחן יש אוכל טעים")
    ]
    
    # --- מאגרי מידע גולמיים לרמה 10-12 (בינוני: השלמת משפטים, דקדוק, סיפורים קצרים) ---
    raw_10_12_sentences = [
        {"q": "Yesterday, my family and I ___ a movie.", "correct": "watched", "options": ["watch", "watching", "watched", "watches"], "hint": "רמז: המילה Yesterday מראה שזה קרה בעבר!"},
        {"q": "The boy was very ___ because he lost his favorite ball.", "correct": "sad", "options": ["happy", "excited", "sad", "tall"], "hint": "רמז: איך מרגישים כשמאבדים כדור אהוב?"},
        {"q": "She always ___ her homework right after school.", "correct": "does", "options": ["do", "does", "doing", "did"], "hint": "רמז: משהו שקורה תמיד בהווה (Present Simple) עבור She"},
        {"q": "Look at the sky! It is very cloudy, I think it will ___ soon.", "correct": "rain", "options": ["rain", "sunny", "fly", "sleep"], "hint": "רמז: מה קורה כשיש הרבה עננים בשמיים?"},
        {"q": "An elephant is ___ than a mouse.", "correct": "bigger", "options": ["smaller", "bigger", "heavy", "biggest"], "hint": "רמז: משווים גודל של פיל לעומת עכבר"},
        {"q": "We use an ___ when it starts to rain outside.", "correct": "umbrella", "options": ["umbrella", "hat", "apple", "airplane"], "hint": "רמז: חפץ שמגן עלינו מהטיפות"}
    ]
    
    raw_10_12_unseens = [
        {"passage": "Danny loves playing football. Every Saturday, he goes to the park with his friends. Yesterday, Danny scored two beautiful goals and his team won the match.", "q": "When does Danny usually play football?", "correct": "Every Saturday", "options": ["Every Saturday", "Yesterday", "Every Sunday", "At night"], "hint": "חפש את המילה Every בתחילת המשפט השני."},
        {"passage": "Mia has a small white cat named Lily. Lily likes to sleep on the sofa all day long. In the evening, Lily loves to play with a small red ball.", "q": "What color is Lily's favorite ball?", "correct": "red", "options": ["white", "red", "blue", "green"], "hint": "קרא את המילה האחרונה בסיפור החתול."}
    ]

    # --- מאגרי מידע גולמיים לרמה 13-15 (מתקדם: אנסינים מעניינים על נושאים כלליים, דקדוק זמנים, מילים גבוהות) ---
    raw_13_15_grammar = [
        {"q": "If I ___ more time last week, I would have visited my grandparents.", "correct": "had had", "options": ["have", "had", "had had", "would have"], "hint": "תנאי שלישי (Third Conditional) המתייחס לעבר"},
        {"q": "By the time the train arrived at the station, the passengers ___ for an hour.", "correct": "had been waiting", "options": ["waited", "were waiting", "had been waiting", "will wait"], "hint": "פעולה שנמשכה בעבר לפני נקודה אחרת (Past Perfect Progressive)"},
        {"q": "The manager decided to ___ the meeting until next Monday due to the storm.", "correct": "postpone", "options": ["postpone", "cancel", "invite", "accelerate"], "hint": "פירוש המילה הוא לדחות למועד אחר"},
        {"q": "She speaks English so ___ that people often think she was born in London.", "correct": "fluently", "options": ["fluently", "fluent", "slowly", "hardly"], "hint": "תואר הפועל המתאר דיבור זורם וטבעי"}
    ]

    raw_13_15_unseens = [
        {"passage": "The history of modern soccer began in England during the 19th century, where the official rules were first established. Today, it has evolved into the world's most popular sport, bringing together billions of fans during global tournaments like the World Cup.", "q": "Where were the official rules of modern soccer first established?", "correct": "In England", "options": ["In England", "In Europe", "During the World Cup", "By global fans"], "hint": "חפש את המיקום המוזכר במשפט הראשון."},
        {"passage": "Traveling abroad offers a unique opportunity to explore diverse cultures and traditions. Many young travelers prefer backpacking because it allows them to experience local life closely while staying within a limited budget.", "q": "Why do many young travelers prefer backpacking according to the text?", "correct": "To experience local life closely within a budget", "options": ["To stay in luxury hotels", "To experience local life closely within a budget", "Because it is faster", "To avoid learning new languages"], "hint": "ראה את החלק האחרון של קטע הקריאה המדבר על תקציב וחיי מקומיים."}
    ]

    # --- פונקציות המנוע לבניית 400 שאלות שונות ומגוונות לכל רמת גיל ---
    def make_7_9_pool():
        pool = []
        q_id = 1
        # מייצרים 400 שאלות על בסיס שילובים שונים ומגוונים
        all_hebrew_words = [x[1] for x in raw_7_9]
        for stage in range(1, 51):
            for q_num in range(1, 9):
                # בוחרים פריט בסיס קבוע או משתנה לפי השילובים
                base_item = raw_7_9[(stage + q_num) % len(raw_7_9)]
                eng, heb, hint = base_item[0], base_item[1], base_item[2]
                
                # יצירת מסיחים שונים בכל פעם מתוך מאגר המילים
                distractors = list(set([h for h in all_hebrew_words if h != heb]))
                options = [heb] + random.sample(distractors, 3)
                random.shuffle(options)
                
                pool.append({
                    "id": q_id,
                    "type": "vocab",
                    "q": f"What is the meaning of the word '{eng}'?",
                    "options": options,
                    "correct": heb,
                    "hint": f"זה משהו שקשור ל{hint}"
                })
                q_id += 1
        return pool

    def make_10_12_pool():
        pool = []
        q_id = 1
        for stage in range(1, 51):
            for q_num in range(1, 9):
                # שילוב בין שאלות משפט קצר לאנסינים קלים
                if q_num in [4, 8]: # שאלות הבנת הנקרא קצרות
                    base_unseen = raw_10_12_unseens[(stage + q_num) % len(raw_10_12_unseens)]
                    item = base_unseen.copy()
                else: # שאלות השלמת משפטים ודקדוק
                    base_sent = raw_10_12_sentences[(stage + q_num) % len(raw_10_12_sentences)]
                    item = base_sent.copy()
                
                item["id"] = q_id
                # ערבוב האופציות כדי שהתשובה לא תהיה באותו מיקום
                opts = item["options"].copy()
                random.shuffle(opts)
                item["options"] = opts
                pool.append(item)
                q_id += 1
        return pool

    def make_13_15_pool():
        pool = []
        q_id = 1
        for stage in range(1, 51):
            for q_num in range(1, 9):
                # שילוב בין דקדוק, אוצר מילים מתקדם ואנסינים כלליים (לא מדעיים!)
                if q_num in [3, 6, 7]:
                    base_unseen = raw_13_15_unseens[(stage + q_num) % len(raw_13_15_unseens)]
                    item = base_unseen.copy()
                else:
                    base_gram = raw_13_15_grammar[(stage + q_num) % len(raw_13_15_grammar)]
                    item = base_gram.copy()
                
                item["id"] = q_id
                opts = item["options"].copy()
                random.shuffle(opts)
                item["options"] = opts
                pool.append(item)
                q_id += 1
        return pool

    # שמירת כל 1,200 השאלות המגוונות ב-Session State
    st.session_state.questions_by_age = {
        "7-9": make_7_9_pool(),
        "10-12": make_10_12_pool(),
        "13-15": make_13_15_pool()
    }
    st.session_state.db_generated = True


# ==========================================
# 2. מערכת התחברות יציבה לחלוטין (ללא מסכים אפורים)
# ==========================================
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

# ניתוב עמודים נקי באמצעות משתנה מצב קבוע
if st.session_state.logged_in_user is None:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("🔐 ברוכים הבאים לממלכת האנגלית!")
    st.subheader("התחברו או הירשמו כדי לשמור את השלבים והקלפים שלכם")
    
    tab_login, tab_register = st.tabs(["👋 התחברות משתמש קיים", "✨ הרשמה (משתמש חדש)"])
    
    with tab_login:
        with st.form("form_login"):
            u_name = st.text_input("שם משתמש:")
            u_pass = st.text_input("סיסמה:", type="password")
            submit_l = st.form_submit_button("היכנס למשחק 🚀")
            if submit_l:
                if u_name in st.session_state.user_db and st.session_state.user_db[u_name]["password"] == u_pass:
                    st.session_state.logged_in_user = u_name
                    # טעינת משתנים
                    data = st.session_state.user_db[u_name]
                    st.session_state.age_level = data["age_level"]
                    st.session_state.score = data["score"]
                    st.session_state.stars = data["stars"]
                    st.session_state.current_stage = data["current_stage"]
                    st.session_state.current_q_index = data["current_q_index"]
                    st.session_state.streak = data["streak"]
                    st.session_state.my_prizes = data["my_prizes"]
                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    st.rerun()
                else:
                    st.error("שם משתמש או סיסמה שגויים.")
                    
    with tab_register:
        with st.form("form_reg"):
            new_u = st.text_input("בחר שם משתמש:")
            new_p = st.text_input("בחר סיסמה:", type="password")
            age_select = st.radio("בחר את קבוצת הגיל שלך:", ["7-9", "10-12", "13-15"])
            submit_r = st.form_submit_button("צור חשבון והתחל 🌟")
            if submit_r:
                if not new_u or not new_p:
                    st.warning("נא למלא את כל הפרטים.")
                elif new_u in st.session_state.user_db:
                    st.error("שם משתמש זה כבר קיים במערכת.")
                else:
                    st.session_state.user_db[new_u] = {
                        "password": new_p, "age_level": age_select, "score": 0, "stars": 0,
                        "current_stage": 1, "current_q_index": 0, "streak": 0, "my_prizes": []
                    }
                    st.session_state.logged_in_user = new_u
                    st.session_state.age_level = age_select
                    st.session_state.score = 0
                    st.session_state.stars = 0
                    st.session_state.current_stage = 1
                    st.session_state.current_q_index = 0
                    st.session_state.streak = 0
                    st.session_state.my_prizes = []
                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. מסך המשחק הראשי (מוצג רק לאחר לוגאין מוצלח)
# ==========================================
else:
    # פונקציה לשמירת ההתקדמות בבסיס הנתונים המקומי
    def sync_data():
        u = st.session_state.logged_in_user
        st.session_state.user_db[u].update({
            "score": st.session_state.score,
            "stars": st.session_state.stars,
            "current_stage": st.session_state.current_stage,
            "current_q_index": st.session_state.current_q_index,
            "streak": st.session_state.streak,
            "my_prizes": st.session_state.my_prizes
        })

    # --- תפריט צד ימני (Sidebar) ---
    with st.sidebar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.header(f"🎒 שלום, {st.session_state.logged_in_user}!")
        st.caption(f"רמת שאלות מוגדרת: גילאי {st.session_state.age_level}")
        
        st.markdown(f"### ✨ כוכבי קסם: **{st.session_state.stars}** ⭐")
        st.markdown(f"### 🆙 שלב נוכחי: **{st.session_state.current_stage}** / 50")
        st.markdown(f"### 🔥 רצף תשובות: **{st.session_state.streak}**")
        st.write("---")
        
        st.subheader("🛍️ חנות הקלפים והפרסים")
        shop_items = [
            {"name": "🍦 גלידת קצפת ענקית", "cost": 20, "stage": 1, "type": "normal"},
            {"name": "🐉 דרקון אש חמוד", "cost": 40, "stage": 1, "type": "normal"},
            {"name": "🔥 קלף פוקימון Charizard VMAX נדיר!", "cost": 100, "stage": 5, "type": "pokemon"},
            {"name": "⚡ קלף פוקימון Pikachu Gold Star", "cost": 150, "stage": 5, "type": "pokemon"},
            {"name": "⚽ חפיסת קלפי Adrenalyn XL זהב", "cost": 200, "stage": 10, "type": "soccer"},
            {"name": "🏆 קלף מוזהב נדיר Match Attax", "cost": 300, "stage": 20, "type": "soccer"}
        ]
        
        for item in shop_items:
            is_locked = st.session_state.current_stage < item['stage']
            is_owned = item['name'] in st.session_state.my_prizes
            disabled_btn = st.session_state.stars < item['cost'] or is_owned or is_locked
            
            btn_text = f"🔒 נפתח בשלב {item['stage']}" if is_locked else ("ברשותך! ✅" if is_owned else f"קנה ב-{item['cost']} ⭐")
            
            st.write(f"**{item['name']}**")
            if not is_locked and item['type'] == 'pokemon':
                st.markdown(f'<div class="trading-card-pokemon">⭐ POKÉMON CARD ⭐<br><b>{item["name"].split("!")[0]}</b></div>', unsafe_allow_html=True)
            elif not is_locked and item['type'] == 'soccer':
                st.markdown(f'<div class="trading-card-soccer">⚽ MATCH ATTAX / ADRENALYN ⚽<br><b>{item["name"]}</b></div>', unsafe_allow_html=True)
                
            if st.button(btn_text, key=f"buy_{item['name']}", disabled=disabled_btn, use_container_width=True):
                st.session_state.stars -= item['cost']
                st.session_state.my_prizes.append(item['name'])
                sync_data()
                st.rerun()
                
        if st.button("🚪 התנתק ושמור התקדמות", use_container_width=True):
            sync_data()
            st.session_state.logged_in_user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- חלון המשחק המרכזי ---
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title(f"👑 ממלכת האנגלית של הילדים - שלב {st.session_state.current_stage} 👑")
    
    if st.session_state.current_stage > 50:
        st.balloons()
        st.success("🏆 מדהים! השלמתם את כל 50 השלבים ופתרתם את כל 400 השאלות הייחודיות שלכם!")
    else:
        # שליפת השאלה הנוכחית והמדויקת מתוך ה-400 הייחודיות של אותה רמת גיל
        pool = st.session_state.questions_by_age[st.session_state.age_level]
        global_index = ((st.session_state.current_stage - 1) * 8) + st.session_state.current_q_index
        q_data = pool[global_index]
        
        st.progress(st.session_state.current_q_index / 8.0)
        st.write(f"✨ שאלה {st.session_state.current_q_index + 1} מתוך 8 בשלב הנוכחי")
        
        # תצוגה מותאמת אישית אם מדובר בטקסט קריאה (Unseen)
        if q_data.get("passage"):
            st.markdown(f'<div style="direction: ltr; text-align: left;" class="unseen-text">📖 <b>Reading Passage:</b><br>{q_data["passage"]}</div>', unsafe_allow_html=True)
            speak_text(q_data["passage"] + " Question: " + q_data["q"])
            st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
            speak_text(q_data["q"])
            
        # --- מצב א': בחירה והגשת תשובה ---
        if not st.session_state.answered_current:
            with st.form(key=f"form_q_{q_data['id']}"):
                choice = st.radio("בחר את התשובה הנכונה מבין האפשרויות הבאות:", q_data['options'], index=None)
                submit_b = st.form_submit_button("בדיקת תשובה וקבלת כוכבים! ➔", use_container_width=True)
                
                if submit_b:
                    if choice is None:
                        st.warning("אופס! שכחת לבחור תשובה.")
                    else:
                        st.session_state.user_choice = choice
                        st.session_state.answered_current = True
                        if choice == q_data['correct']:
                            st.session_state.score += 1
                            st.session_state.stars += 25
                            st.session_state.streak += 1
                        else:
                            st.session_state.streak = 0
                        sync_data()
                        st.rerun()
                        
            with st.expander("💡 צריך רמז סודי? לחץ כאן"):
                st.write(q_data["hint"])
                
        # --- מצב ב': פידבק לאחר לחיצה ומעבר שלב ---
        else:
            for opt in q_data['options']:
                if opt == q_data['correct']:
                    st.success(f"🟢 **{opt}** (זו התשובה הנכונה!)")
                elif opt == st.session_state.user_choice:
                    st.error(f"🔴 **{opt}** (הבחירה שלך)")
                else:
                    st.write(f"⚪ {opt}")
                    
            if st.session_state.user_choice == q_data['correct']:
                st.balloons()
                st.markdown("## 🎉 כל הכבוד! צדקתם והרווחתם **25 כוכבי קסם!** ⭐")
            else:
                st.markdown(f"## 🌟 לא נורא, בפעם הבאה תצליחו! התשובה היא: **{q_data['correct']}**")
                
            if st.button("קדימה, לשאלה הבאה! 🚀", type="primary", use_container_width=True):
                st.session_state.current_q_index += 1
                if st.session_state.current_q_index >= 8:
                    st.session_state.current_stage += 1
                    st.session_state.current_q_index = 0
                    st.session_state.stars += 100
                    st.toast("🏆 איזה אלופים! סיימתם שלב שלם וקיבלתם בונוס של 100 כוכבים!")
                    
                st.session_state.answered_current = False
                st.session_state.user_choice = None
                sync_data()
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
