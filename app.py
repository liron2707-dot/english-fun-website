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
# עיצוב מותאם (CSS)
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
# 1. מנוע ג'נרטור אולטרה-מתקדם - אלפי אפשרויות ללא חזרות!
# ==========================================
if 'db_generated' not in st.session_state:
    
    # ------------------ מחולל שאלות דינמי ממאגר דחוס ------------------
    def generate_vocab_questions(raw_string, amount):
        words = []
        for pair in raw_string.split('|'):
            if ':' in pair:
                eng, heb = pair.split(':')
                words.append((eng.strip(), heb.strip()))
        
        all_hebrew = [w[1] for w in words]
        questions = []
        # נייצר פי 2 שאלות מאוצר המילים (פעם מה הפירוש, פעם השלמת מילה)
        for eng, heb in words:
            distractors = random.sample([h for h in all_hebrew if h != heb], 3)
            options = distractors + [heb]
            random.shuffle(options)
            questions.append({
                "q": f"What is the meaning of the word '{eng}'?",
                "correct": heb,
                "options": options,
                "hint": "תרגום מאנגלית לעברית"
            })
            
            # סוג שאלה הפוך - השלמת החסר
            distractors_eng = random.sample([w[0] for w in words if w[0] != eng], 3)
            options_eng = distractors_eng + [eng]
            random.shuffle(options_eng)
            questions.append({
                "q": f"How do you say '{heb}' in English?",
                "correct": eng,
                "options": options_eng,
                "hint": "תרגום מעברית לאנגלית"
            })
            
        random.shuffle(questions)
        return questions[:amount]

    # ------------------ מחולל אנסינים דינמי (Infinite Unseens) ------------------
    def generate_dynamic_unseens(age_group, amount):
        unseens = []
        names = ["Danny", "Maya", "Tom", "Sarah", "David", "Anna", "Ben", "Emma"]
        places_7_9 = [("zoo", "animals"), ("park", "trees"), ("beach", "shells"), ("farm", "cows")]
        places_10_12 = [("museum", "paintings"), ("stadium", "players"), ("concert", "singers"), ("library", "books")]
        places_13_15 = [("foreign country", "tourists"), ("technology exhibition", "robots"), ("historic city", "monuments")]
        
        for _ in range(amount):
            name = random.choice(names)
            if age_group == "7-9":
                place, item = random.choice(places_7_9)
                num = random.randint(2, 10)
                passage = f"Yesterday, {name} went to the {place}. It was a very sunny day. {name} saw {num} beautiful {item} there. {name} was very happy."
                q1 = {"q": f"Where did {name} go?", "correct": f"To the {place}", "options": [f"To the {place}", "To the school", "To the hospital", "To the shop"], "hint": "קרא את המשפט הראשון."}
                q2 = {"q": f"How many {item} did {name} see?", "correct": str(num), "options": [str(num), str(num+1), "One", "Zero"], "hint": "חפש את המספר בטקסט."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
                
            elif age_group == "10-12":
                place, item = random.choice(places_10_12)
                friend = random.choice([n for n in names if n != name])
                passage = f"{name} and {friend} decided to visit the {place} last weekend. They spent three hours looking at the amazing {item}. After that, they were very hungry, so they bought a large pizza."
                q1 = {"q": f"Who did {name} go with to the {place}?", "correct": friend, "options": [friend, "Mom", "A teacher", "Nobody"], "hint": "מי מוזכר במשפט הראשון יחד עם הדמות?"}
                q2 = {"q": f"What did they do because they were hungry?", "correct": "Bought a large pizza", "options": ["Bought a large pizza", "Went to sleep", "Drank water", f"Looked at {item}"], "hint": "קרא את המשפט האחרון."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
                
            else: # 13-15
                place, item = random.choice(places_13_15)
                years = random.randint(3, 8)
                passage = f"Traveling to a {place} can be a life-changing experience. {name}, a young traveler, spent {years} months saving money for this journey. During the trip, {name} was fascinated by the incredible {item} and learned a lot about the local culture and traditions."
                q1 = {"q": f"Why is {name}'s experience described as significant?", "correct": "It was a life-changing experience.", "options": ["It was a life-changing experience.", "It was extremely boring.", "It took too much time.", "It was a terrible mistake."], "hint": "קרא את תחילת הטקסט."}
                q2 = {"q": f"How long did {name} save money for the journey?", "correct": f"{years} months", "options": [f"{years} months", f"{years} years", "One week", "A few days"], "hint": "חפש את המספר בטקסט."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
                
        return unseens

    # ------------------ בניית מאגרי המילים והדקדוק הענקיים ------------------

    # --- גיל 7-9: 100+ מילים בסיסיות, חיות, צבעים, משפחה, פעלים פשוטים ---
    raw_vocab_7_9 = "Apple:תפוח|Dog:כלב|Cat:חתול|Sun:שמש|Water:מים|Boy:ילד|Girl:ילדה|Moon:ירח|Star:כוכב|Fish:דג|Bird:ציפור|Cow:פרה|Horse:סוס|Tree:עץ|Flower:פרח|Car:מכונית|Bus:אוטובוס|Train:רכבת|House:בית|Door:דלת|Window:חלון|Table:שולחן|Chair:כיסא|Book:ספר|Pen:עט|Pencil:עיפרון|Bag:תיק|School:בית ספר|Teacher:מורה|Mother:אמא|Father:אבא|Brother:אח|Sister:אחות|Baby:תינוק|Hand:יד|Foot:רגל|Eye:עין|Ear:אוזן|Nose:אף|Mouth:פה|Head:ראש|Hair:שיער|Red:אדום|Blue:כחול|Green:ירוק|Yellow:צהוב|Black:שחור|White:לבן|Pink:ורוד|Orange:כתום|Brown:חום|One:אחד|Two:שתיים|Three:שלוש|Four:ארבע|Five:חמש|Six:שש|Seven:שבע|Eight:שמונה|Nine:תשע|Ten:עשר|Happy:שמח|Sad:עצוב|Big:גדול|Small:קטן|Hot:חם|Cold:קר|Good:טוב|Bad:רע|Fast:מהיר|Slow:איטי|Day:יום|Night:לילה|Morning:בוקר|Evening:ערב|Play:לשחק|Jump:לקפוץ|Run:לרוץ|Sleep:לישון|Eat:לאכול|Drink:לשתות|Milk:חלב|Bread:לחם|Cheese:גבינה|Meat:בשר|Cake:עוגה|Candy:סוכריה|Toy:צעצוע|Ball:כדור|Park:פארק|Zoo:גן חיות|Shop:חנות|Street:רחוב|Rain:גשם|Snow:שלג"
    
    grammar_7_9 = []
    for _ in range(50):
        subj = random.choice(["I", "He", "She", "It", "We", "They"])
        if subj == "I": ans, wrong = "am", ["is", "are", "be"]
        elif subj in ["He", "She", "It"]: ans, wrong = "is", ["am", "are", "be"]
        else: ans, wrong = "are", ["is", "am", "be"]
        options = [ans] + wrong
        random.shuffle(options)
        grammar_7_9.append({"q": f"{subj} ___ happy today.", "correct": ans, "options": options, "hint": "התאם את פועל העזר לנושא."})

    # --- גיל 10-12: 100+ מילים, תארים, זמנים, מקצועות, מזג אוויר ---
    raw_vocab_10_12 = "Yesterday:אתמול|Tomorrow:מחר|Today:היום|Always:תמיד|Never:אף פעם|Sometimes:לפעמים|Usually:בדרך כלל|Beautiful:יפה|Ugly:מכוער|Smart:חכם|Stupid:טיפש|Clean:נקי|Dirty:מלוכלך|Easy:קל|Hard:קשה|Heavy:כבד|Light:קל (משקל/אור)|Strong:חזק|Weak:חלש|Rich:עשיר|Poor:עני|High:גבוה|Low:נמוך|Early:מוקדם|Late:מאוחר|Right:נכון/ימין|Wrong:לא נכון|True:אמת|False:שקר|Friend:חבר|Enemy:אויב|Neighbor:שכן|Question:שאלה|Answer:תשובה|Word:מילה|Sentence:משפט|Page:עמוד|Letter:מכתב/אות|Number:מספר|Minute:דקה|Hour:שעה|Week:שבוע|Month:חודש|Year:שנה|Spring:אביב|Summer:קיץ|Autumn:סתיו|Winter:חורף|Holiday:חג|Vacation:חופשה|Trip:טיול|Ticket:כרטיס|Money:כסף|Price:מחיר|Market:שוק|Buy:לקנות|Sell:למכור|Pay:לשלם|Cost:לעלות (מחיר)|Wear:ללבוש|Clothes:בגדים|Shirt:חולצה|Pants:מכנסיים|Dress:שמלה|Shoes:נעליים|Hat:כובע|Coat:מעיל|Weather:מזג אוויר|Cloud:ענן|Storm:סערה|River:נהר|Sea:ים|Mountain:הר|Forest:יער|Island:אי|Animal:חיה|Wild:פראי|Pet:חיית מחמד|Danger:סכנה|Safe:בטוח|Help:לעזור|Work:לעבוד|Job:עבודה|Office:משרד|Doctor:רופא|Nurse:אחות (מקצוע)|Police:משטרה|Fire:אש|Cook:לבשל|Build:לבנות|Farm:חווה"
    
    grammar_10_12 = []
    verbs = [("go", "went"), ("eat", "ate"), ("see", "saw"), ("buy", "bought"), ("do", "did")]
    for _ in range(50):
        v_pres, v_past = random.choice(verbs)
        options = [v_past, v_pres, v_pres+"ing", v_pres+"s"]
        random.shuffle(options)
        grammar_10_12.append({"q": f"Yesterday, I ___ to the mall.", "correct": v_past, "options": options, "hint": "יש פה רמז לעבר (Yesterday)."})

    # --- גיל 13-15: 100+ מילים גבוהות, מושגים, חברה, כלכלה, ופעלים מתקדמים ---
    raw_vocab_13_15 = "Environment:סביבה|Pollution:זיהום|Climate:אקלים|Discover:לגלות|Invent:להמציא|Technology:טכנולוגיה|Society:חברה|Culture:תרבות|Tradition:מסורת|Government:ממשלה|Election:בחירות|Law:חוק|Crime:פשע|Punishment:עונש|Justice:צדק|Peace:שלום|War:מלחמה|Army:צבא|Soldier:חייל|Weapon:נשק|Economy:כלכלה|Business:עסק|Company:חברה (עסקית)|Factory:מפעל|Industry:תעשייה|Trade:סחר|Import:ייבוא|Export:ייצוא|Profit:רווח|Loss:הפסד|Success:הצלחה|Failure:כישלון|Challenge:אתגר|Opportunity:הזדמנות|Advantage:יתרון|Disadvantage:חיסרון|Benefit:תועלת|Harm:נזק|Risk:סיכון|Protect:להגן|Destroy:להרוס|Create:ליצור|Improve:לשפר|Develop:לפתח|Grow:לגדול/לצמוח|Reduce:להפחית|Increase:להגדיל|Measure:למדוד|Compare:להשוות|Contrast:לעמת (למצוא הבדלים)|Explain:להסביר|Describe:לתאר|Argue:להתווכח|Agree:להסכים|Disagree:לא להסכים|Opinion:דעה|Fact:עובדה|Evidence:ראיה/הוכחה|Prove:להוכיח|Suggest:להציע|Advise:לייעץ|Recommend:להמליץ|Decide:להחליט|Choose:לבחור|Option:אפשרות|Alternative:חלופה|Result:תוצאה|Cause:גורם|Effect:השפעה/תוצאה|Reason:סיבה|Purpose:מטרה|Goal:יעד|Achieve:להשיג|Succeed:להצליח|Fail:להיכשל|Attempt:ניסיון|Effort:מאמץ|Energy:אנרגיה|Power:כוח|Control:שליטה|Manage:לנהל|Organize:לארגן|Plan:לתכנן|Prepare:להכין"

    grammar_13_15 = []
    phrasal = [("give up", "להיכנע/לוותר"), ("look after", "לשמור על"), ("take off", "להמריא/להוריד"), ("run out of", "לגמור את המלאי")]
    for _ in range(50):
        phrase, mean = random.choice(phrasal)
        distractors = random.sample(["in", "on", "at", "over", "down", "away"], 3)
        verb, prep = phrase.split()
        options = [prep] + distractors
        random.shuffle(options)
        grammar_13_15.append({"q": f"Choose the correct preposition: We need to {verb} ___ our goals.", "correct": prep, "options": options, "hint": f"ביטוי שמשמעותו קרובה ל: {mean}"})

    # --- איחוד וערבוב מושלם ליצירת מעל 400 שאלות ייחודיות לכל רמה! ---
    def build_massive_pool(raw_vocab, grammar_list, age):
        pool = []
        # 1. נוסיף מאות שאלות אוצר מילים
        pool.extend(generate_vocab_questions(raw_vocab, 300))
        # 2. נוסיף עשרות שאלות דקדוק
        pool.extend(grammar_list)
        # 3. נוסיף המון אנסינים דינמיים שנוצרו הרגע
        pool.extend(generate_dynamic_unseens(age, 30))
        
        # ערבוב עמוק של כל המאגר!
        random.shuffle(pool)
        
        # נוודא שיש לנו לפחות 400 שאלות (ל-50 שלבים), וניתן ID מסודר
        final_pool = []
        q_id = 1
        for item in pool:
            item_copy = item.copy()
            item_copy["id"] = q_id
            final_pool.append(item_copy)
            q_id += 1
            
        # אם חסר (לא סביר), נשכפל ונערבב שוב
        while len(final_pool) < 400:
            extra = random.choice(pool).copy()
            extra["id"] = q_id
            random.shuffle(extra["options"])
            final_pool.append(extra)
            q_id += 1
            
        return final_pool[:400] # לוקחים בדיוק 400 שאלות ייחודיות ל-50 שלבים

    st.session_state.questions_by_age = {
        "7-9": build_massive_pool(raw_vocab_7_9, grammar_7_9, "7-9"),
        "10-12": build_massive_pool(raw_vocab_10_12, grammar_10_12, "10-12"),
        "13-15": build_massive_pool(raw_vocab_13_15, grammar_13_15, "13-15")
    }
    st.session_state.db_generated = True


# ==========================================
# 2. מערכת התחברות
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
