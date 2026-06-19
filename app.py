import streamlit as st
import random
import streamlit.components.v1 as components

# הגדרות עמוד מותאמות
st.set_page_config(
    page_title="ממלכת האנגלית של המקצוענים!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# עיצוב מותאם (CSS) - ימין לשמאל, קלפים ופונטים ענקיים
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

# פונקציית הקראה קולית חכמה (TTS) באמצעות דפדפן
def speak_text(text):
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    html_code = f"""
    <button onclick="var msg = new SpeechSynthesisUtterance('{safe_text}'); msg.lang='en-US'; msg.rate=0.9; window.speechSynthesis.speak(msg);" 
    style="background-color:#F39C12; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
        🔊 הקרא את הטקסט באנגלית
    </button>
    """
    components.html(html_code, height=50)

# ==========================================
# 1. בסיס נתונים - 3 רמות גיל ומחולל 1,200 שאלות
# ==========================================
if 'db_generated' not in st.session_state:
    
    # רמה 1: גילאי 7-9 (אוצר מילים בסיסי, צבעים, חיות, משפטים פשוטים)
    level_1_base = [
        {"type": "vocab", "q": "What animal is a 'Lion'?", "options": ["אריה", "פיל", "קוף", "נמר"], "correct": "אריה", "hint": "מלך החיות!"},
        {"type": "vocab", "q": "Which color is 'Red'?", "options": ["אדום", "כחול", "ירוק", "צהוב"], "correct": "אדום", "hint": "צבע של עגבנייה"},
        {"type": "grammar", "q": "I ___ a boy.", "options": ["am", "is", "are", "be"], "correct": "am", "hint": "כשאני מדבר על עצמי..."},
        {"type": "vocab", "q": "What is 'Apple'?", "options": ["תפוח", "בננה", "תפוז", "ענבים"], "correct": "תפוח", "hint": "פרי אדום או ירוק"}
    ]
    
    # רמה 2: גילאי 10-12 (דקדוק בינוני, השלמת משפטים, הבנת הנקרא קלה)
    level_2_base = [
        {"type": "grammar", "q": "Yesterday, we ___ to the park.", "options": ["went", "go", "going", "goes"], "correct": "went", "hint": "פעל בעבר (Past Simple)"},
        {"type": "completion", "q": "It is raining outside. Don't forget to take your ___.", "options": ["umbrella", "shoes", "sunglasses", "computer"], "correct": "umbrella", "hint": "משהו שמגן מפני הגשם"},
        {"type": "grammar", "q": "She is ___ than her brother.", "options": ["taller", "tall", "tallest", "more tall"], "correct": "taller", "hint": "השוואה בין שניים (Comparative)"},
        {"type": "unseen", "passage": "Tom has a big dog named Rex. Every morning, Tom and Rex go for a walk in the forest. Rex loves to chase small birds.", "q": "What does Rex love to chase?", "options": ["small birds", "cats", "cars", "butterflies"], "correct": "small birds", "hint": "קרא את המשפט האחרון בטקסט."}
    ]
    
    # רמה 3: גילאי 13-15 (דקדוק מתקדם, אוצר מילים גבוה, Unseens מורכבים בנושאי מדע והיסטוריה)
    level_3_base = [
        {"type": "grammar", "q": "If I ___ known you were coming, I would have baked a cake.", "options": ["had", "have", "would", "will"], "correct": "had", "hint": "Conditionals (Third Conditional)"},
        {"type": "unseen", "passage": "The biological hierarchy describes the organization of life. It starts from atoms, building up to molecules, and then cells. Inside the cell, organelles like the mitochondria function as powerhouses, generating energy for cellular processes.", "q": "According to the text, what is the main function of the mitochondria?", "options": ["Generating energy", "Storing DNA", "Absorbing water", "Destroying viruses"], "correct": "Generating energy", "hint": "חפש את המילה powerhouses בטקסט."},
        {"type": "unseen", "passage": "Traditional courtyard games in Italy and Poland were passed down through generations. Before the digital age, children spent hours outside playing simple physical games, relying heavily on chalk, stones, and sheer imagination rather than technology.", "q": "What did children rely on for their courtyard games?", "options": ["Imagination and simple objects", "Electricity and screens", "Expensive toys", "Teachers' instructions"], "correct": "Imagination and simple objects", "hint": "הסתכל על המשפט השני: chalk, stones, imagination."},
        {"type": "vocab", "q": "Which word is a synonym for 'Inevitably'?", "options": ["Unavoidably", "Quickly", "Rarely", "Happily"], "correct": "Unavoidably", "hint": "משהו שאי אפשר למנוע אותו"}
    ]

    # פונקציית עזר להרחבת המאגר כדי להגיע ל-400 שאלות פר רמה (50 שלבים * 8 שאלות)
    def generate_full_pool(base_list):
        full_pool = []
        q_id = 1
        while len(full_pool) < 400:
            for item in base_list:
                if len(full_pool) >= 400: break
                new_item = item.copy()
                new_item["id"] = q_id
                # ערבוב התשובות כדי שזה לא יהיה זהה
                random.shuffle(new_item["options"])
                full_pool.append(new_item)
                q_id += 1
        return full_pool

    st.session_state.questions_by_age = {
        "7-9": generate_full_pool(level_1_base),
        "10-12": generate_full_pool(level_2_base),
        "13-15": generate_full_pool(level_3_base)
    }
    st.session_state.db_generated = True

# ==========================================
# 2. ניהול מערכת המשתמשים הנתונים
# ==========================================
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

def save_user_progress():
    user = st.session_state.logged_in_user
    if user:
        st.session_state.user_db[user].update({
            "score": st.session_state.score,
            "stars": st.session_state.stars,
            "current_stage": st.session_state.current_stage,
            "current_q_index": st.session_state.current_q_index,
            "streak": st.session_state.streak,
            "my_prizes": st.session_state.my_prizes
        })

def load_user_progress(username):
    data = st.session_state.user_db[username]
    st.session_state.age_level = data["age_level"]
    st.session_state.score = data["score"]
    st.session_state.stars = data["stars"]
    st.session_state.current_stage = data["current_stage"]
    st.session_state.current_q_index = data["current_q_index"]
    st.session_state.streak = data["streak"]
    st.session_state.max_streak = data.get("max_streak", 0)
    st.session_state.my_prizes = data["my_prizes"]
    st.session_state.answered_current = False
    st.session_state.user_choice = None


# ==========================================
# 3. מסך ראשי - ניתוב (Routing)
# ==========================================
# אם המשתמש לא מחובר, נציג רק את מסך ההתחברות/הרשמה:
if st.session_state.logged_in_user is None:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("🔐 ברוכים הבאים לממלכת האנגלית!")
    st.subheader("כאן לומדים, צוברים כוכבים, וקונים קלפים נדירים!")
    
    tab_login, tab_register = st.tabs(["👋 התחברות (משתמש קיים)", "✨ הרשמה (משתמש חדש)"])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("שם משתמש:")
            password = st.text_input("סיסמה:", type="password")
            btn_login = st.form_submit_button("היכנס למשחק 🚀")
            if btn_login:
                if username in st.session_state.user_db and st.session_state.user_db[username]["password"] == password:
                    st.session_state.logged_in_user = username
                    load_user_progress(username)
                    st.rerun()
                else:
                    st.error("שגיאה בפרטים או שאינך רשום.")
                    
    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("בחר שם משתמש:")
            new_password = st.text_input("בחר סיסמה:", type="password")
            # הוספת בחירת רמת גיל בהרשמה!
            age_level = st.radio("בחר את רמת הגיל שלך (זה יקבע את סוג השאלות):", ["7-9", "10-12", "13-15"])
            btn_reg = st.form_submit_button("צור משתמש והתחל לשחק 🎉")
            
            if btn_reg:
                if not new_username or not new_password:
                    st.warning("נא למלא את כל השדות!")
                elif new_username in st.session_state.user_db:
                    st.error("שם המשתמש תפוס.")
                else:
                    st.session_state.user_db[new_username] = {
                        "password": new_password, "age_level": age_level, "score": 0, "stars": 0,
                        "current_stage": 1, "current_q_index": 0, "streak": 0, "max_streak": 0, "my_prizes": []
                    }
                    st.session_state.logged_in_user = new_username
                    load_user_progress(new_username)
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. המערכת המרכזית (מוצגת רק אם המשתמש מחובר)
# ==========================================
else:
    # --- תפריט צד (Sidebar) ---
    with st.sidebar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.header(f"🎒 שלום, {st.session_state.logged_in_user}!")
        st.caption(f"רמת גיל מוגדרת: {st.session_state.age_level}")
        
        st.markdown(f"### ✨ כוכבי קסם: **{st.session_state.stars}** ⭐")
        st.markdown(f"### 🆙 שלב נוכחי: **{st.session_state.current_stage}** / 50")
        st.markdown(f"### 🔥 רצף תשובות: **{st.session_state.streak}**")
        st.write("---")
        
        st.subheader("🛍️ חנות הפרסים והקלפים")
        shop_items = [
            {"name": "🍦 גלידת פיסטוק", "cost": 20, "stage": 1, "type": "normal"},
            {"name": "🐉 דרקון מחמד", "cost": 40, "stage": 1, "type": "normal"},
            {"name": "🔥 קלף פוקימון Charizard VMAX", "cost": 100, "stage": 5, "type": "pokemon"},
            {"name": "⚽ קלף Match Attax מוזהב", "cost": 200, "stage": 10, "type": "soccer"},
            {"name": "🏆 קלף Adrenalyn XL נדיר", "cost": 300, "stage": 20, "type": "soccer"}
        ]
        
        for item in shop_items:
            is_locked = st.session_state.current_stage < item['stage']
            is_owned = item['name'] in st.session_state.my_prizes
            disabled_btn = st.session_state.stars < item['cost'] or is_owned or is_locked
            
            btn_text = f"🔒 נפתח בשלב {item['stage']}" if is_locked else ("ברשותך! ✅" if is_owned else f"קנה ב-{item['cost']} ⭐")
            
            st.write(f"**{item['name']}**")
            if not is_locked and item['type'] == 'pokemon':
                st.markdown(f'<div class="trading-card-pokemon">⭐ POKÉMON ⭐<br><b>{item["name"].split("!")[0]}</b></div>', unsafe_allow_html=True)
            elif not is_locked and item['type'] == 'soccer':
                st.markdown(f'<div class="trading-card-soccer">⚽ SOCCER CARD ⚽<br><b>{item["name"]}</b></div>', unsafe_allow_html=True)
                
            if st.button(btn_text, key=f"buy_{item['name']}", disabled=disabled_btn, use_container_width=True):
                st.session_state.stars -= item['cost']
                st.session_state.my_prizes.append(item['name'])
                save_user_progress()
                st.rerun()
                
        if st.button("🚪 התנתק ושמור נתונים", use_container_width=True):
            save_user_progress()
            st.session_state.logged_in_user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- חלון המשחק הראשי ---
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title(f"👑 ממלכת האנגלית - שלב {st.session_state.current_stage} 👑")
    
    if st.session_state.current_stage > 50:
        st.balloons()
        st.success("סיימת את כל 50 השלבים ואת כל 400 השאלות של הרמה שלך! אתה אלוף אמיתי!")
        st.stop()

    # שליפת המאגר המתאים לגיל ושליפת השאלה הנוכחית
    pool = st.session_state.questions_by_age[st.session_state.age_level]
    current_q_global_idx = ((st.session_state.current_stage - 1) * 8) + st.session_state.current_q_index
    q_data = pool[current_q_global_idx]

    st.progress(st.session_state.current_q_index / 8.0)
    st.write(f"✨ שאלה {st.session_state.current_q_index + 1} מתוך 8")
    
    # תצוגה מיוחדת לאנסינים (Unseen) וטקסט ארוך
    if q_data.get("type") == "unseen":
        st.markdown(f'<div style="direction: ltr; text-align: left;" class="unseen-text">📖 <b>Reading Passage:</b><br>{q_data["passage"]}</div>', unsafe_allow_html=True)
        # כפתור הקראה לאנסין
        speak_text(q_data["passage"] + " Now the question: " + q_data["q"])
        st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
        # כפתור הקראה לשאלה רגילה
        speak_text(q_data["q"])

    # טופס בחירת התשובה
    if not st.session_state.answered_current:
        with st.form(key=f"stage_form_{q_data['id']}"):
            choice = st.radio("בחר את התשובה הנכונה:", q_data['options'], index=None)
            submit_button = st.form_submit_button("בדיקה וקבלת כוכבים! ➔", use_container_width=True)
            
            if submit_button:
                if choice is None:
                    st.warning("בחר תשובה לפני הבדיקה!")
                else:
                    st.session_state.user_choice = choice
                    st.session_state.answered_current = True
                    if choice == q_data['correct']:
                        st.session_state.score += 1
                        st.session_state.stars += 25
                        st.session_state.streak += 1
                    else:
                        st.session_state.streak = 0
                    save_user_progress()
                    st.rerun()
                    
        with st.expander("💡 צריך רמז?"):
            st.write(q_data["hint"])

    # הצגת פידבק
    else:
        for opt in q_data['options']:
            if opt == q_data['correct']:
                st.success(f"🟢 **{opt}** (התשובה הנכונה!)")
            elif opt == st.session_state.user_choice:
                st.error(f"🔴 **{opt}** (הבחירה שלך)")
            else:
                st.write(f"⚪ {opt}")
                
        if st.session_state.user_choice == q_data['correct']:
            st.balloons()
            st.markdown("## 🎉 אלופים! צדקתם + 25 כוכבים ⭐")
        else:
            st.markdown("## 🌟 לא נורא, נסו שוב בשאלה הבאה!")
            
        if st.button("לשאלה הבאה 🚀", type="primary", use_container_width=True):
            st.session_state.current_q_index += 1
            if st.session_state.current_q_index >= 8:
                st.session_state.current_stage += 1
                st.session_state.current_q_index = 0
                st.session_state.stars += 100
                st.toast("🏆 סיימתם את השלב וקיבלתם בונוס של 100 כוכבים!")
            st.session_state.answered_current = False
            st.session_state.user_choice = None
            save_user_progress()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
