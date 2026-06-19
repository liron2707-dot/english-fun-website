import streamlit as st
import random
import streamlit.components.v1 as components
import json
import os

# ==========================================
# קובץ השמירה של המשתמשים
# ==========================================
USER_DB_FILE = "users_db.json"

# ==========================================
# מאגר התמונות האמיתיות לפרסים ולקלפים 
# ==========================================
PRIZE_IMAGES = {
    "🍦 גלידת קצפת ענקית": "https://images.unsplash.com/photo-1563805042-7684c8a9e9cb?q=80&w=800",
    "🐉 דרקון אש חמוד": "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=800",
    "🔥 קלף פוקימון Charizard VMAX נדיר!": "https://images.pokemontcg.io/swsh3/20_hires.png",
    "⚡ קלף פוקימון Pikachu Gold Star": "https://images.pokemontcg.io/ex13/104_hires.png",
    "⚽ חפיסת קלפי Adrenalyn XL זהב": "https://m.media-amazon.com/images/I/81xU+aYmC5L._AC_SX679_.jpg",
    "🏆 קלף מוזהב נדיר Match Attax": "https://m.media-amazon.com/images/I/81p+kZ1O8nL._AC_SX679_.jpg"
}

# הגדרות עמוד ותצוגה
st.set_page_config(
    page_title="ממלכת האנגלית של המקצוענים!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# עיצוב מותאם (CSS) ואנימציות תלת מימד
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
    
    /* אנימציית פתיחת קלפים בכספת (3D Flip) */
    .flip-card {
      background-color: transparent;
      width: 100%;
      height: 400px;
      perspective: 1000px;
      margin-bottom: 20px;
    }
    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.8s;
      transform-style: preserve-3d;
      cursor: pointer;
    }
    .flip-card:hover .flip-card-inner, .flip-card:active .flip-card-inner {
      transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: 15px;
      box-shadow: 0 10px 20px rgba(0,0,0,0.25);
    }
    .flip-card-front {
      background: linear-gradient(135deg, #8e44ad, #3498db);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 22px;
      font-weight: bold;
      border: 4px solid #f1c40f;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .flip-card-back {
      transform: rotateY(180deg);
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
      background-color: #1a1a1a;
      border: 4px solid #f1c40f;
    }
</style>
""", unsafe_allow_html=True)

# פונקציית הקראה קולית משופרת עם תמיכה באנגלית ובעברית (לגילאי 4-6)
def speak_text(text_en, text_he=""):
    safe_en = text_en.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    
    if text_he:
        safe_he = text_he.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
        html_code = f"""
        <div style='display:flex; justify-content:center; gap:15px; margin-bottom: 10px;'>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_he}'); msg.lang='he-IL'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
            style="background-color:#3498db; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                🔊 הקרא שאלה בעברית
            </button>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_en}'); msg.lang='en-US'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
            style="background-color:#F39C12; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                🔊 הקרא באנגלית
            </button>
        </div>
        """
    else:
        html_code = f"""
        <div style='display:flex; justify-content:center; margin-bottom: 10px;'>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_en}'); msg.lang='en-US'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
            style="background-color:#F39C12; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                🔊 לחץ כאן להקראת הטקסט באנגלית
            </button>
        </div>
        """
    components.html(html_code, height=60)


# ==========================================
# 1. מנוע ג'נרטור מתקדם עם חוקים ורמזים חכמים
# ==========================================
if 'db_generated' not in st.session_state:
    
    def generate_vocab_questions(raw_string, amount, is_toddler=False):
        words = []
        for pair in raw_string.split('|'):
            if ':' in pair:
                eng, heb = pair.split(':')
                words.append((eng.strip(), heb.strip()))
        
        all_hebrew = [w[1] for w in words]
        questions = []
        for eng, heb in words:
            # שאלת תרגום לאנגלית
            distractors = random.sample([h for h in all_hebrew if h != heb], 3)
            options = distractors + [heb]
            random.shuffle(options)
            
            if is_toddler:
                q_text1 = f"מה הפירוש של המילה '{eng}'?"
                hint1 = f"💡 רמז סודי: התשובה בעברית מתחילה באות '{heb[0]}'."
                audio_he1 = f"מה הפירוש של המילה {eng}?"
                audio_en1 = eng
            else:
                q_text1 = f"What is the meaning of the word '{eng}'?"
                hint1 = f"💡 רמז סודי: התשובה בעברית מתחילה באות '{heb[0]}'."
                audio_he1 = ""
                audio_en1 = q_text1
                
            questions.append({
                "q": q_text1, "correct": heb, "options": options, "hint": hint1,
                "audio_he": audio_he1, "audio_en": audio_en1
            })
            
            # שאלת השלמה לאנגלית
            distractors_eng = random.sample([w[0] for w in words if w[0] != eng], 3)
            options_eng = distractors_eng + [eng]
            random.shuffle(options_eng)
            
            if is_toddler:
                q_text2 = f"איך אומרים '{heb}' באנגלית?"
                hint2 = f"💡 רמז סודי: התשובה באנגלית מתחילה באות '{eng[0]}'."
                audio_he2 = f"איך אומרים {heb} באנגלית?"
                audio_en2 = "The options are: " + ", ".join(options_eng)
            else:
                q_text2 = f"How do you say '{heb}' in English?"
                hint2 = f"💡 רמז סודי: התשובה באנגלית מתחילה באות '{eng[0]}'."
                audio_he2 = ""
                audio_en2 = q_text2
                
            questions.append({
                "q": q_text2, "correct": eng, "options": options_eng, "hint": hint2,
                "audio_he": audio_he2, "audio_en": audio_en2
            })
            
        random.shuffle(questions)
        return questions[:amount]

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
                q1 = {"q": f"Where did {name} go?", "correct": f"To the {place}", "options": [f"To the {place}", "To the school", "To the hospital", "To the shop"], "hint": "💡 רמז: מצאו את המשפט הראשון בטקסט, שם רשום לאן הדמות הלכה."}
                q2 = {"q": f"How many {item} did {name} see?", "correct": str(num), "options": [str(num), str(num+1), "One", "Zero"], "hint": "💡 רמז: חפשו את המספר המדויק שמופיע בטקסט."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
                
            elif age_group == "10-12":
                place, item = random.choice(places_10_12)
                friend = random.choice([n for n in names if n != name])
                passage = f"{name} and {friend} decided to visit the {place} last weekend. They spent three hours looking at the amazing {item}. After that, they were very hungry, so they bought a large pizza."
                q1 = {"q": f"Who did {name} go with to the {place}?", "correct": friend, "options": [friend, "Mom", "A teacher", "Nobody"], "hint": "💡 רמז: מי מוזכר במשפט הראשון יחד עם הדמות המרכזית?"}
                q2 = {"q": f"What did they do because they were hungry?", "correct": "Bought a large pizza", "options": ["Bought a large pizza", "Went to sleep", "Drank water", f"Looked at {item}"], "hint": "💡 רמז: קראו את המשפט האחרון בטקסט (After that...)."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
                
            elif age_group == "13-15":
                place, item = random.choice(places_13_15)
                years = random.randint(3, 8)
                passage = f"Traveling to a {place} can be a life-changing experience. {name}, a young traveler, spent {years} months saving money for this journey. During the trip, {name} was fascinated by the incredible {item} and learned a lot about the local culture and traditions."
                q1 = {"q": f"Why is {name}'s experience described as significant?", "correct": "It was a life-changing experience.", "options": ["It was a life-changing experience.", "It was extremely boring.", "It took too much time.", "It was a terrible mistake."], "hint": "💡 רמז: קראו את תחילת הפסקה כדי למצוא את התיאור של החוויה (experience)."}
                q2 = {"q": f"How long did {name} save money for the journey?", "correct": f"{years} months", "options": [f"{years} months", f"{years} years", "One week", "A few days"], "hint": "💡 רמז: חפשו את המספר המציין את משך הזמן של חיסכון הכסף."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
                
        return unseens

    # --- מילים ודקדוק לכל קבוצות הגיל ---
    
    raw_vocab_4_6 = "Dog:כלב|Cat:חתול|Sun:שמש|Water:מים|Boy:ילד|Girl:ילדה|Red:אדום|Blue:כחול|Green:ירוק|Yellow:צהוב|One:אחד|Two:שתיים|Three:שלוש|Four:ארבע|Five:חמש|Apple:תפוח|Banana:בננה|Car:מכונית|Ball:כדור|Yes:כן|No:לא|Hello:שלום|Bye:להתראות|Mom:אמא|Dad:אבא|Eye:עין|Nose:אף|Mouth:פה|Ear:אוזן|Hand:יד|Leg:רגל|Big:גדול|Small:קטן|Happy:שמח|Sad:עצוב|Hot:חם|Cold:קר|Milk:חלב|Tree:עץ|Flower:פרח|Bird:ציפור|Fish:דג|House:בית|Door:דלת|Window:חלון|Bed:מיטה|Morning:בוקר|Night:לילה"

    raw_vocab_7_9 = "Apple:תפוח|Dog:כלב|Cat:חתול|Sun:שמש|Water:מים|Moon:ירח|Star:כוכב|Fish:דג|Bird:ציפור|Cow:פרה|Horse:סוס|Tree:עץ|Flower:פרח|Car:מכונית|Bus:אוטובוס|Train:רכבת|House:בית|Door:דלת|Window:חלון|Table:שולחן|Chair:כיסא|Book:ספר|Pen:עט|School:בית ספר|Teacher:מורה|Mother:אמא|Father:אבא|Brother:אח|Sister:אחות|Baby:תינוק|Hand:יד|Foot:רגל|Eye:עין|Ear:אוזן|Nose:אף|Mouth:פה|Head:ראש|Red:אדום|Blue:כחול|Green:ירוק|Yellow:צהוב|Black:שחור|White:לבן|Pink:ורוד|Orange:כתום|Brown:חום|Happy:שמח|Sad:עצוב|Big:גדול|Small:קטן|Hot:חם|Cold:קר|Good:טוב|Bad:רע|Fast:מהיר|Slow:איטי|Play:לשחק|Jump:לקפוץ|Run:לרוץ|Sleep:לישון|Eat:לאכול|Drink:לשתות|Milk:חלב|Bread:לחם|Cheese:גבינה|Meat:בשר|Cake:עוגה|Candy:סוכריה|Toy:צעצוע|Ball:כדור|Park:פארק|Zoo:גן חיות"
    
    grammar_7_9 = []
    base_templates_7_9 = [
        ("I", "am", ["is", "are", "be"], "a good student."),
        ("He", "is", ["am", "are", "be"], "a tall boy."),
        ("She", "is", ["am", "are", "be"], "my smart sister."),
        ("It", "is", ["am", "are", "be"], "a small brown dog."),
        ("We", "are", ["is", "am", "be"], "happy friends."),
        ("They", "are", ["is", "am", "be"], "at the big school."),
        ("You", "are", ["is", "am", "be"], "a very nice teacher."),
        ("The cat", "is", ["am", "are", "be"], "sleeping on the chair."),
        ("The apples", "are", ["is", "am", "be"], "red and sweet.")
    ]
    for i in range(50):
        base = base_templates_7_9[i % len(base_templates_7_9)]
        subj, ans, wrong, rest = base
        options = [ans] + wrong
        random.shuffle(options)
        grammar_7_9.append({
            "q": f"{subj} ___ {rest}",
            "correct": ans,
            "options": options,
            "hint": "💡 רמז דקדוקי: He, She, It מקבלים תמיד 'is'. הגוף I מקבל 'am'. והרבים We, You, They מקבלים 'are'."
        })

    raw_vocab_10_12 = "Yesterday:אתמול|Tomorrow:מחר|Today:היום|Always:תמיד|Never:אף פעם|Sometimes:לפעמים|Usually:בדרך כלל|Beautiful:יפה|Ugly:מכוער|Smart:חכם|Stupid:טיפש|Clean:נקי|Dirty:מלוכלך|Easy:קל|Hard:קשה|Heavy:כבד|Light:קל|Strong:חזק|Weak:חלש|Rich:עשיר|Poor:עני|Early:מוקדם|Late:מאוחר|Right:נכון|Wrong:לא נכון|Friend:חבר|Enemy:אויב|Neighbor:שכן|Question:שאלה|Answer:תשובה|Word:מילה|Sentence:משפט|Month:חודש|Year:שנה|Spring:אביב|Summer:קיץ|Autumn:סתיו|Winter:חורף|Holiday:חג|Vacation:חופשה|Money:כסף|Buy:לקנות|Sell:למכור|Pay:לשלם|Clothes:בגדים|Shirt:חולצה|Pants:מכנסיים|Dress:שמלה|Shoes:נעליים|Weather:מזג אוויר|Cloud:ענן|Storm:סערה|River:נהר|Sea:ים|Mountain:הר|Forest:יער|Animal:חיה|Safe:בטוח|Help:לעזור|Work:לעבוד|Job:עבודה|Doctor:רופא|Police:משטרה"
    
    grammar_10_12 = []
    base_templates_10_12 = [
        ("Yesterday, I ___ to the beautiful park.", "went", "go", "going", "goes"),
        ("Last night, we ___ a giant delicious pizza.", "ate", "eat", "eating", "eats"),
        ("Two days ago, she ___ a colorful bird in the sky.", "saw", "see", "seeing", "sees"),
        ("My father ___ a new red car last week.", "bought", "buy", "buying", "buys"),
        ("He ___ his difficult homework yesterday afternoon.", "did", "do", "doing", "does")
    ]
    for i in range(50):
        base = base_templates_10_12[i % len(base_templates_10_12)]
        sentence, v_past, v_pres, v_ing, v_s = base
        options = [v_past, v_pres, v_ing, v_s]
        random.shuffle(options)
        grammar_10_12.append({
            "q": sentence,
            "correct": v_past,
            "options": options,
            "hint": "💡 רמז דקדוקי: שימו לב למילות הזמן (Yesterday, Last, Ago)! הן מצביעות על זמן עבר (Past Simple), ולכן חפשו פועל בעבר."
        })

    raw_vocab_13_15 = "Environment:סביבה|Pollution:זיהום|Climate:אקלים|Discover:לגלות|Invent:להמציא|Technology:טכנולוגיה|Society:חברה|Culture:תרבות|Tradition:מסורת|Government:ממשלה|Election:בחירות|Law:חוק|Crime:פשע|Punishment:עונש|Justice:צדק|Peace:שלום|War:מלחמה|Army:צבא|Soldier:חייל|Weapon:נשק|Economy:כלכלה|Business:עסק|Company:חברה|Factory:מפעל|Industry:תעשייה|Trade:סחר|Import:ייבוא|Export:ייצוא|Profit:רווח|Loss:הפסד|Success:הצלחה|Failure:כישלון|Challenge:אתגר|Opportunity:הזדמנות|Advantage:יתרון|Disadvantage:חיסרון|Benefit:תועלת|Harm:נזק|Risk:סיכון|Protect:להגן|Destroy:להרוס|Create:ליצור|Improve:לשפר|Develop:לפתח|Grow:לגדול/לצמוח|Reduce:להפחית|Increase:להגדיל|Measure:למדוד|Compare:להשוות|Explain:להסביר|Describe:לתאר|Argue:להתווכח|Agree:להסכים|Disagree:לא להסכים|Opinion:דעה|Fact:עובדה|Evidence:ראיה|Prove:להוכיח|Suggest:להציע|Advise:לייעץ|Recommend:להמליץ|Decide:להחליט|Choose:לבחור|Result:תוצאה|Cause:גורם|Reason:סיבה|Purpose:מטרה|Goal:יעד|Achieve:להשיג|Succeed:להצליח|Fail:להיכשל|Effort:מאמץ|Energy:אנרגיה"

    grammar_13_15 = []
    base_templates_13_15 = [
        ("give", "up", "להיכנע/לוותר", "You should never give ___ on your dreams and goals."),
        ("look", "after", "לשמור על/לטפל ב-", "She stays at home to look ___ her little brother."),
        ("take", "off", "להמריא", "The airplane is ready to take ___ from the airport runway."),
        ("find", "out", "לגלות", "We need to find ___ the secret truth about this mystery.")
    ]
    for i in range(50):
        base = base_templates_13_15[i % len(base_templates_13_15)]
        verb, prep, mean, sentence = base
        distractors = random.sample([p for p in ["in", "on", "at", "over", "down", "away", "up", "off", "out", "to", "of"] if p != prep], 3)
        options = [prep] + distractors
        random.shuffle(options)
        grammar_13_15.append({
            "q": f"Choose the correct preposition to complete the phrasal verb: {sentence}",
            "correct": prep,
            "options": options,
            "hint": f"💡 רמז סודי: מדובר ב-Phrasal Verb. השילוב של הפועל '{verb}' יחד עם מילת היחס הנכונה יוצר את המשמעות '{mean}'."
        })

    def build_massive_pool(raw_vocab, grammar_list, age):
        pool = []
        is_toddler = (age == "4-6")
        
        # 1. נוסיף המון שאלות אוצר מילים
        pool.extend(generate_vocab_questions(raw_vocab, 350 if is_toddler else 300, is_toddler))
        
        # 2. נוסיף דקדוק ואנסינים רק לגדולים יותר
        if not is_toddler:
            pool.extend(grammar_list)
            pool.extend(generate_dynamic_unseens(age, 30))
        
        random.shuffle(pool)
        
        final_pool = []
        q_id = 1
        for item in pool:
            item_copy = item.copy()
            item_copy["id"] = q_id
            final_pool.append(item_copy)
            q_id += 1
            
        while len(final_pool) < 400:
            extra = random.choice(pool).copy()
            extra["id"] = q_id
            random.shuffle(extra["options"])
            final_pool.append(extra)
            q_id += 1
            
        return final_pool[:400] 

    st.session_state.questions_by_age = {
        "4-6": build_massive_pool(raw_vocab_4_6, [], "4-6"),
        "7-9": build_massive_pool(raw_vocab_7_9, grammar_7_9, "7-9"),
        "10-12": build_massive_pool(raw_vocab_10_12, grammar_10_12, "10-12"),
        "13-15": build_massive_pool(raw_vocab_13_15, grammar_13_15, "13-15")
    }
    st.session_state.db_generated = True

# ==========================================
# 2. מערכת התחברות חכמה ושמירה אוטומטית כנגד רענונים
# ==========================================
if 'user_db' not in st.session_state:
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r", encoding="utf-8") as f:
            try:
                st.session_state.user_db = json.load(f)
            except:
                st.session_state.user_db = {}
    else:
        st.session_state.user_db = {}

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
if 'show_vault' not in st.session_state: st.session_state.show_vault = False

if st.session_state.logged_in_user is None:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("🔐 ברוכים הבאים לממלכת האנגלית!")
    st.subheader("התחברו או הירשמו כדי לשמור את השלבים והקלפים שלכם")
    st.info("💡 **טיפ להורים ולילדים:** הנתונים שלכם נשמרים אוטומטית! אם הדף התרענן בטעות, פשוט הזינו שוב את שם המשתמש והסיסמה ותחזרו בדיוק לאותה השאלה שבה עצרתם.")
    
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
                    st.session_state.my_prizes = data.get("my_prizes", [])
                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    st.session_state.show_vault = False
                    st.rerun()
                else:
                    st.error("שם משתמש או סיסמה שגויים. נסו שוב!")
                    
    with tab_register:
        with st.form("form_reg"):
            new_u = st.text_input("בחר שם משתמש:")
            new_p = st.text_input("בחר סיסמה:", type="password")
            age_select = st.radio("בחר את קבוצת הגיל שלך:", ["4-6", "7-9", "10-12", "13-15"])
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
                    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
                        json.dump(st.session_state.user_db, f, ensure_ascii=False, indent=4)
                        
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
                    st.session_state.show_vault = False
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 3. מסך המשחק הראשי (וכספת הפרסים עם האנימציות)
# ==========================================
else:
    def sync_data():
        u = st.session_state.logged_in_user
        st.session_state.user_db[u].update({
            "age_level": st.session_state.age_level,
            "score": st.session_state.score,
            "stars": st.session_state.stars,
            "current_stage": st.session_state.current_stage,
            "current_q_index": st.session_state.current_q_index,
            "streak": st.session_state.streak,
            "my_prizes": st.session_state.my_prizes
        })
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.user_db, f, ensure_ascii=False, indent=4)

    # --- תפריט צד ימני (Sidebar) ---
    with st.sidebar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.header(f"🎒 שלום, {st.session_state.logged_in_user}!")
        st.caption(f"רמת שאלות מוגדרת: גילאי {st.session_state.age_level}")
        
        new_age = st.selectbox(
            "🔄 שנה קבוצת גיל / רמה:",
            ["4-6", "7-9", "10-12", "13-15"],
            index=["4-6", "7-9", "10-12", "13-15"].index(st.session_state.age_level),
            key="change_user_age_level"
        )
        if new_age != st.session_state.age_level:
            st.session_state.age_level = new_age
            u = st.session_state.logged_in_user
            st.session_state.user_db[u]["age_level"] = new_age
            sync_data()
            st.toast(f"🚀 הרמה שונתה בהצלחה לגילאי {new_age}!")
            st.rerun()
            
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
                st.balloons()
                st.toast("🎉 איזה כיף! הפרס נכנס לכספת שלך!")
                st.rerun()

        st.write("---")
        
        if st.button("💼 הצג את כספת הפרסים והקלפים שלי!", type="primary", use_container_width=True):
            st.session_state.show_vault = True
            st.rerun()
                
        if st.button("🚪 התנתק ושמור התקדמות", use_container_width=True):
            sync_data()
            st.session_state.logged_in_user = None
            st.session_state.show_vault = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- חלון כספת הפרסים ---
    if st.session_state.show_vault:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.title("💼 כספת הפרסים והקלפים האמיתיים שלי!")
        st.subheader("ריחפו עם העכבר (או לחצו במסך מגע) על חבילות הקלפים כדי לפתוח ולחשוף אותם!")
        
        if not st.session_state.my_prizes:
            st.info("הכספת שלכם ריקה בינתיים... חזרו למשחק, הרוויחו כוכבים וקנו פרסים נדירים בחנות!")
        else:
            cols = st.columns(3)
            for i, prize_name in enumerate(st.session_state.my_prizes):
                with cols[i % 3]:
                    image_url = PRIZE_IMAGES.get(prize_name, "https://via.placeholder.com/300")
                    html_card = f"""
                    <div class="flip-card">
                      <div class="flip-card-inner">
                        <div class="flip-card-front">
                          🎁<br>הקליקו/רחפו לפתיחת החבילה!<br><br><span style="font-size:18px;">{prize_name.split('!')[0]}</span>
                        </div>
                        <div class="flip-card-back" style="background-image: url('{image_url}');">
                        </div>
                      </div>
                    </div>
                    """
                    st.markdown(html_card, unsafe_allow_html=True)
        
        st.write("---")
        if st.button("🔙 חזור להמשיך לשחק", type="primary"):
            st.session_state.show_vault = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # --- חלון המשחק הראשי ---
    else:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.title(f"👑 ממלכת האנגלית של הילדים - שלב {st.session_state.current_stage} 👑")
        
        if st.session_state.current_stage > 50:
            st.balloons()
            st.success("🏆 מדהים! השלמתם את כל 50 השלבים ופתרתם את כל השאלות ברמה שלכם!")
        else:
            pool = st.session_state.questions_by_age[st.session_state.age_level]
            global_index = ((st.session_state.current_stage - 1) * 8) + st.session_state.current_q_index
            q_data = pool[global_index]
            
            st.progress(st.session_state.current_q_index / 8.0)
            st.write(f"✨ שאלה {st.session_state.current_q_index + 1} מתוך 8 בשלב הנוכחי")
            
            # מערכת הקראה חכמה ודינמית (אנגלית ועברית במידת הצורך)
            if st.session_state.age_level == "4-6":
                # לגילאי 4-6 יש כפתורים כפולים לשאלה ותשובה
                st.markdown(f'<div style="text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
                speak_text(text_en=q_data.get("audio_en", ""), text_he=q_data.get("audio_he", ""))
            else:
                if q_data.get("passage"):
                    st.markdown(f'<div style="direction: ltr; text-align: left;" class="unseen-text">📖 <b>Reading Passage:</b><br>{q_data["passage"]}</div>', unsafe_allow_html=True)
                    speak_text(text_en=q_data["passage"] + " Question: " + q_data["q"])
                    st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="direction: ltr; text-align: center;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
                    speak_text(text_en=q_data["q"])
                
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
                            sync_data() # שמירה מיידית לאחר תשובה!
                            st.rerun()
                            
                with st.expander("💡 צריך עזרה? לחץ כאן לקבלת רמז סודי וחכם"):
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
                    st.markdown("## 🎉 כל הכבוד אלופים! צדקתם והרווחתם **25 כוכבי קסם!** ⭐")
                else:
                    st.markdown(f"## 🌟 לא נורא, במשחק תמיד אפשר לנסות שוב! התשובה היא: **{q_data['correct']}**")
                    
                if st.button("קדימה, לשאלה הבאה! 🚀", type="primary", use_container_width=True):
                    st.session_state.current_q_index += 1
                    if st.session_state.current_q_index >= 8:
                        st.session_state.current_stage += 1
                        st.session_state.current_q_index = 0
                        st.session_state.stars += 100
                        st.toast("🏆 איזה אלופים! סיימתם שלב שלם וקיבלתם בונוס של 100 כוכבים!")
                        
                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    sync_data() # גיבוי מיידי לפני מעבר שאלה!
                    st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)
