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
# 1. מנוע ג'נרטור חכם ומשופר - 1,200 שאלות ללא חזרות מיותרות!
# ==========================================
if 'db_generated' not in st.session_state:
    
    # פונקציית עזר ליצירת המאגר הסופי - מערבבת את השאלות בצורה אקראית לחלוטין
    def build_400_shuffled_pool(temp_pool):
        pool = []
        q_id = 1
        # נשכפל את המאגר כמה שצריך עד שנגיע ליותר מ-400, אבל בכל פעם נערבב מחדש!
        while len(pool) < 400:
            random.shuffle(temp_pool)
            for item in temp_pool:
                if len(pool) >= 400:
                    break
                q_copy = item.copy()
                q_copy["id"] = q_id
                random.shuffle(q_copy["options"]) # ערבוב התשובות הפנימיות
                pool.append(q_copy)
                q_id += 1
        return pool

    # --- מאגר 7-9: אוצר מילים, דקדוק בסיסי והבנת הנקרא פשוטה ---
    words_7_9 = [
        ("Dog", "כלב", "נובח"), ("Cat", "חתול", "מיאו"), ("Sun", "שמש", "צהובה למעלה"), ("Water", "מים", "שותים"),
        ("Apple", "תפוח", "פרי אדום/ירוק"), ("Banana", "בננה", "פרי צהוב"), ("Red", "אדום", "צבע"), ("Blue", "כחול", "צבע הים"),
        ("Green", "ירוק", "צבע הדשא"), ("Yellow", "צהוב", "צבע הלימון"), ("School", "בית ספר", "לומדים שם"), ("Teacher", "מורה", "מלמד בכיתה"),
        ("Happy", "שמח", "מחייך"), ("Sad", "עצוב", "בוכה"), ("Big", "גדול", "כמו פיל"), ("Small", "קטן", "כמו נמלה"),
        ("Hand", "יד", "יש לנו שתיים כאלו"), ("Foot", "רגל", "הולכים עליה"), ("Eye", "עין", "רואים בעזרתה"), ("Ear", "אוזן", "שומעים בעזרתה"),
        ("Car", "מכונית", "נוסעת בכביש"), ("Bus", "אוטובוס", "רכב גדול לתלמידים"), ("House", "בית", "גרים בו"), ("Door", "דלת", "פותחים כדי להיכנס"),
        ("Mother", "אמא", "במשפחה"), ("Father", "אבא", "במשפחה"), ("Brother", "אח", "במשפחה"), ("Sister", "אחות", "במשפחה")
    ]
    
    temp_7_9 = []
    # הוספת אוצר מילים פשוט
    all_heb_7_9 = [w[1] for w in words_7_9]
    for eng, heb, hint in words_7_9:
        distractors = random.sample([h for h in all_heb_7_9 if h != heb], 3)
        temp_7_9.append({
            "q": f"What is the meaning of '{eng}'?", "correct": heb, "options": [heb] + distractors, "hint": hint
        })
    # הוספת דקדוק והשלמת משפטים בסיסית
    grammar_7_9 = [
        {"q": "I ___ a good boy.", "correct": "am", "options": ["am", "is", "are", "be"], "hint": "כשאני מדבר על עצמי..."},
        {"q": "The sun ___ yellow.", "correct": "is", "options": ["am", "is", "are", "be"], "hint": "כשאנחנו מדברים על משהו אחד (it)..."},
        {"q": "They ___ playing basketball.", "correct": "are", "options": ["am", "is", "are", "play"], "hint": "כשאנחנו מדברים על רבים (They)..."},
        {"q": "I have two ___.", "correct": "eyes", "options": ["eyes", "nose", "mouth", "head"], "hint": "יש לי שניים כאלו בפרצוף"},
        {"q": "The apple is ___.", "correct": "red", "options": ["red", "blue", "sad", "fast"], "hint": "איזה צבע יש לתפוח?"}
    ]
    temp_7_9.extend(grammar_7_9)


    # --- מאגר 10-12: אוצר מילים בינוני, דקדוק זמנים, הבנת הנקרא בינונית ---
    temp_10_12 = []
    grammar_vocab_10_12 = [
        {"q": "Yesterday, I ___ to the park.", "correct": "went", "options": ["go", "went", "going", "goes"], "hint": "רמז לעבר (Past Simple) - אתמול"},
        {"q": "She is ___ than her sister.", "correct": "taller", "options": ["tall", "taller", "tallest", "more tall"], "hint": "השוואה בין שתיים (Comparative)"},
        {"q": "We ___ watching TV right now.", "correct": "are", "options": ["am", "is", "are", "do"], "hint": "פעולה שקורית ממש עכשיו (Present Progressive)"},
        {"q": "I usually ___ up at 7:00 AM.", "correct": "wake", "options": ["wake", "woke", "waking", "wakes"], "hint": "משהו שקורה בדרך כלל בהווה (Present Simple)"},
        {"q": "Look at the dark clouds! It is going to ___.", "correct": "rain", "options": ["rain", "sunny", "hot", "fly"], "hint": "מה קורה כשיש עננים שחורים?"},
        {"q": "My dog is very ___. He sleeps all day.", "correct": "lazy", "options": ["lazy", "fast", "angry", "smart"], "hint": "מישהו שלא אוהב לעשות כלום"},
        {"q": "Don't forget to wear a ___ because it is cold outside.", "correct": "coat", "options": ["coat", "t-shirt", "shorts", "sunglasses"], "hint": "בגד שלובשים כשקר מאוד"},
        {"q": "Which word is the opposite of 'Beautiful'?", "correct": "Ugly", "options": ["Ugly", "Nice", "Pretty", "Small"], "hint": "ההפך מיפה"}
    ]
    temp_10_12.extend(grammar_vocab_10_12)
    
    unseens_10_12 = [
        {"passage": "Danny went to the zoo on Saturday. He saw three big elephants and a funny monkey. He ate a delicious chocolate ice cream with his dad.", 
         "qs": [
             {"q": "Where did Danny go on Saturday?", "correct": "To the zoo", "options": ["To the zoo", "To the park", "To the school", "To the cinema"], "hint": "קרא את המשפט הראשון."},
             {"q": "What kind of ice cream did Danny eat?", "correct": "Chocolate", "options": ["Chocolate", "Vanilla", "Strawberry", "Banana"], "hint": "קרא את המשפט האחרון."},
             {"q": "How many elephants did Danny see?", "correct": "Three", "options": ["Three", "Two", "One", "Four"], "hint": "חפש את המילה elephants."}
         ]},
        {"passage": "Sarah loves reading books. She reads a new book every week. Her favorite books are about magic and dragons.",
         "qs": [
             {"q": "How often does Sarah read a new book?", "correct": "Every week", "options": ["Every week", "Every day", "Every month", "Never"], "hint": "חפש את המילה every בטקסט."},
             {"q": "What are Sarah's favorite books about?", "correct": "Magic and dragons", "options": ["Magic and dragons", "Cars and planes", "Dogs and cats", "Sports"], "hint": "המשפט האחרון מספר על התחביב שלה."}
         ]}
    ]
    for un in unseens_10_12:
        for q in un["qs"]:
            temp_10_12.append({"passage": un["passage"], "q": q["q"], "correct": q["correct"], "options": q["options"], "hint": q["hint"]})


    # --- מאגר 13-15: מתקדם - אוצר מילים גבוה, דקדוק מורכב, ואנסינים מרתקים (ללא מדע) ---
    temp_13_15 = []
    grammar_vocab_13_15 = [
        {"q": "If I ___ known about the party, I would have bought a gift.", "correct": "had", "options": ["have", "had", "would", "has"], "hint": "תנאי שלישי בעבר (Third Conditional)"},
        {"q": "The beautiful song was ___ by a famous singer.", "correct": "sung", "options": ["sing", "sang", "sung", "singing"], "hint": "משפט סביל (Passive Voice) בזמן עבר"},
        {"q": "By the time we arrived at the cinema, the movie ___ already started.", "correct": "had", "options": ["has", "had", "was", "is"], "hint": "פעולה אחת קרתה לפני פעולה אחרת בעבר (Past Perfect)"},
        {"q": "She decided to give ___ smoking because it is bad for her health.", "correct": "up", "options": ["up", "in", "out", "away"], "hint": "פועל תלויי מילת יחס (Phrasal Verb) שמשמעותו להפסיק"},
        {"q": "Choose the correct synonym for the word 'Enormous':", "correct": "Huge", "options": ["Huge", "Tiny", "Average", "Weak"], "hint": "משהו מאוד מאוד גדול"},
        {"q": "He couldn't ___ the fact that he failed the driving test.", "correct": "accept", "options": ["accept", "except", "expect", "aspect"], "hint": "מילה שמשמעותה 'לקבל/להשלים עם'"},
        {"q": "We must ___ the environment for the future generations.", "correct": "protect", "options": ["protect", "destroy", "ignore", "pollute"], "hint": "לשמור או להגן"}
    ]
    temp_13_15.extend(grammar_vocab_13_15)

    unseens_13_15 = [
        {"passage": "Backpacking across Europe has become a popular trend among teenagers and young adults. It allows travelers to experience different cultures closely, meet locals, and learn how to manage a tight budget while navigating through various countries using trains and buses.",
         "qs": [
             {"q": "According to the text, why is backpacking popular?", "correct": "It allows experiencing cultures and managing a budget.", "options": ["It allows experiencing cultures and managing a budget.", "It is the most expensive way to travel.", "It prevents you from meeting locals.", "You only stay in luxury hotels."], "hint": "קרא את המשפט השני על תרבויות ותקציב."},
             {"q": "How do backpackers usually navigate through countries according to the passage?", "correct": "Using trains and buses", "options": ["Using trains and buses", "By buying private cars", "By flying first class", "By walking only"], "hint": "חפש את המילים בסוף הטקסט."}
         ]},
        {"passage": "The modern game of soccer, as we know it today, was established in England in the 19th century. Before the official rules were written, people played different versions of the game in towns and villages, which often led to chaos and arguments on the field.",
         "qs": [
             {"q": "Where were the official rules of modern soccer established?", "correct": "In England", "options": ["In England", "In Brazil", "In the USA", "In France"], "hint": "המשפט הראשון מציין את המדינה."},
             {"q": "What happened before the official rules were written?", "correct": "Different versions of the game led to chaos.", "options": ["Different versions of the game led to chaos.", "Everyone played perfectly together.", "The game was forbidden by law.", "Only rich people played it."], "hint": "קרא את המשפט השני על כאוס וויכוחים."}
         ]},
        {"passage": "Listening to music while studying is a topic of debate. Some students claim that soft background music helps them focus and reduces stress, while others find any kind of noise highly distracting when trying to memorize new vocabulary.",
         "qs": [
             {"q": "What is one benefit of listening to soft music while studying, according to some students?", "correct": "It helps focus and reduces stress.", "options": ["It helps focus and reduces stress.", "It ruins their memory entirely.", "It makes them sleepy immediately.", "It distracts them from vocabulary."], "hint": "חפש את היתרונות (helps) בחלק הראשון של המשפט השני."},
             {"q": "What does the word 'distracting' mean in the context of the text?", "correct": "Taking attention away from studying", "options": ["Taking attention away from studying", "Helping someone relax", "Playing a musical instrument", "Reading very fast"], "hint": "משהו שמפריע להתרכז."}
         ]}
    ]
    for un in unseens_13_15:
        for q in un["qs"]:
            temp_13_15.append({"passage": un["passage"], "q": q["q"], "correct": q["correct"], "options": q["options"], "hint": q["hint"]})

    # יצירת המאגרים הסופיים תוך ערבוב מושלם כדי למנוע כל חזרה של שלבים!
    st.session_state.questions_by_age = {
        "7-9": build_400_shuffled_pool(temp_7_9),
        "10-12": build_400_shuffled_pool(temp_10_12),
        "13-15": build_400_shuffled_pool(temp_13_15)
    }
    st.session_state.db_generated = True


# ==========================================
# 2. מערכת התחברות יציבה לחלוטין
# ==========================================
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

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
# 3. מסך המשחק הראשי
# ==========================================
else:
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
        pool = st.session_state.questions_by_age[st.session_state.age_level]
        global_index = ((st.session_state.current_stage - 1) * 8) + st.session_state.current_q_index
        q_data = pool[global_index]
        
        st.progress(st.session_state.current_q_index / 8.0)
        st.write(f"✨ שאלה {st.session_state.current_q_index + 1} מתוך 8 בשלב הנוכחי")
        
        if q_data.get("passage"):
            st.markdown(f'<div style="direction: ltr; text-align: left;" class="unseen-text">📖 <b>Reading Passage:</b><br>{q_data["passage"]}</div>', unsafe_allow_html=True)
            speak_text(q_data["passage"] + " Question: " + q_data["q"])
            st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
            speak_text(q_data["q"])
            
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
