import streamlit as st
import random
import streamlit.components.v1 as components
import json
import os
import time
from datetime import datetime

# ==========================================
# קובץ השמירה של המשתמשים (מערכת גיבוי חכמה)
# ==========================================
USER_DB_FILE = "users_db.json"

# ==========================================
# מאגר התמונות האמיתיות לפרסים ולקלפים (תוקן והורחב בענק!)
# ==========================================
PRIZE_IMAGES = {
    "🍦 גלידת קצפת ענקית": "https://images.unsplash.com/photo-1563805042-7684c8a9e9cb?q=80&w=800",
    "🐉 דרקון אש חמוד": "https://images.unsplash.com/photo-1577493340887-b7bfff550145?q=80&w=800",
    "🔥 קלף פוקימון Charizard": "https://assets.pokemon.com/assets/cms2/img/cards/web/XY2/XY2_EN_12.png",
    "⚡ קלף פוקימון Pikachu": "https://assets.pokemon.com/assets/cms2/img/cards/web/XY1/XY1_EN_42.png",
    "🌊 קלף פוקימון Blastoise": "https://assets.pokemon.com/assets/cms2/img/cards/web/XY1/XY1_EN_16.png",
    "⚽ חפיסת קלפי מסי זהב": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?q=80&w=800",
    "🏆 קלף רונאלדו נדיר": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=800",
    "🎧 אוזניות אפל Airpods": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?q=80&w=800",
    "🌟 מארז קלפי כדורגל": "https://images.unsplash.com/photo-1614632537190-23e4146777db?q=80&w=800",
    "🤖 רובוט אינטראקטיבי": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=800",
    "💻 מחשב גיימינג מפלצתי": "https://images.unsplash.com/photo-1600861194942-f883de0dfe96?q=80&w=800",
    "📱 אייפון 15 פרו מקס": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?q=80&w=800",
    "🛹 הוברבורד חשמלי": "https://images.unsplash.com/photo-1564227503881-2b083315a6b0?q=80&w=800",
    "🎮 סוני פלייסטיישן 5": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?q=80&w=800",
    "🥽 משקפי מציאות מדומה VR": "https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?q=80&w=800",
    "🦸‍♂️ קלף ספיידרמן נדיר": "https://images.unsplash.com/photo-1608889175123-8ee362201f81?q=80&w=800",
    "⚔️ חרב נינג'ה זוהרת": "https://images.unsplash.com/photo-1588783424168-fc890c2eb7ff?q=80&w=800",
    "🦄 בובת חד קרן ענקית": "https://images.unsplash.com/photo-1559715541-5daf8a0296d0?q=80&w=800",
    "🛸 רחפן צילום מקצועי": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?q=80&w=800",
    "🏎️ מכונית על למבורגיני": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?q=80&w=800",
    "🪄 שרביט קסמים אמיתי": "https://images.unsplash.com/photo-1618842676088-c4d48a6a7c9d?q=80&w=800",
    "👑 כתר יהלומים": "https://images.unsplash.com/photo-1595986630530-969786b19b4d?q=80&w=800",
    "💎 תיבת אוצר מסתורית": "https://images.unsplash.com/photo-1580215758509-32cf431e71e7?q=80&w=800"
}

# דמויות לבחירה (Avatars)
AVATARS = ["😎", "🦄", "🚀", "🐱‍👤", "👑", "🐉", "🤖", "🦊"]

# מילון תמונות לילדי 4-6
toddler_pics = {
    "Dog": "🐶", "Cat": "🐱", "Sun": "☀️", "Water": "💧", "Boy": "👦", "Girl": "👧",
    "Red": "🔴", "Blue": "🔵", "Green": "🟢", "Yellow": "🟡",
    "One": "1️⃣", "Two": "2️⃣", "Three": "3️⃣", "Four": "4️⃣", "Five": "5️⃣",
    "Apple": "🍎", "Banana": "🍌", "Car": "🚗", "Ball": "⚽",
    "Yes": "✅", "No": "❌", "Hello": "👋", "Bye": "👋",
    "Mom": "👩", "Dad": "👨", "Eye": "👁️", "Nose": "👃", "Mouth": "👄", "Ear": "👂",
    "Hand": "✋", "Leg": "🦵", "Big": "🐘", "Small": "🐜",
    "Happy": "😊", "Sad": "😢", "Hot": "🔥", "Cold": "❄️",
    "Milk": "🥛", "Tree": "🌳", "Flower": "🌻", "Bird": "🐦", "Fish": "🐟",
    "House": "🏠", "Door": "🚪", "Window": "🪟", "Bed": "🛏️",
    "Morning": "🌅", "Night": "🌙"
}

# הגדרות עמוד ותצוגה
st.set_page_config(
    page_title="ממלכת האנגלית של המקצוענים!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# עיצוב מותאם (CSS) משוכלל בסגנון Brawl Stars!
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Varela+Round&display=swap');

    /* החלת הפונט רק על אלמנטים מסוימים כדי לא לדרוס את האייקונים של המערכת (החץ הכפול) */
    html, body, p, div, h1, h2, h3, h4, h5, h6, label, span {
        font-family: 'Varela Round', sans-serif;
    }
    .material-symbols-rounded, svg {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    .rtl-container {
        direction: rtl;
        text-align: right;
    }
    
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 3px solid #dcdde1;
    }

    /* עיצוב תשובות קופצני ותלת מימדי (כמו במשחק סלולר) */
    div[data-testid="stRadio"] label p {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #2f3640;
        padding: 12px 20px;
        background: #ffffff;
        border-radius: 20px;
        border: 3px solid #dcdde1;
        border-bottom: 6px solid #dcdde1;
        transition: all 0.2s ease;
        margin-bottom: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
    }
    div[data-testid="stRadio"] label p:hover {
        background: #f5f6fa;
        border-color: #0097e6;
        border-bottom: 6px solid #0097e6;
        transform: translateY(-3px);
    }

    /* עיצוב שאלות מרכזי עגול וצבעוני */
    .question-box {
        font-size: 32px !important;
        color: #ffffff;
        font-weight: 800;
        margin-bottom: 25px;
        background: linear-gradient(135deg, #192a56 0%, #273c75 100%);
        padding: 30px;
        border-radius: 25px;
        border: 5px solid #00a8ff;
        box-shadow: 0 10px 0px rgba(0,168,255,0.4);
        text-align: center;
        animation: pulse 2s infinite alternate;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.02); }
    }

    /* כרטיסים نדירים בחנות */
    .trading-card-pokemon, .trading-card-soccer, .vip-card {
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        color: white;
        text-shadow: 1px 1px 3px black;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .trading-card-pokemon {
        background: linear-gradient(135deg, #f1c40f, #e67e22);
        border: 4px solid #fff;
        box-shadow: 0 6px 0px #d35400;
    }
    .trading-card-soccer {
        background: linear-gradient(135deg, #3498db, #2980b9);
        border: 4px solid #fff;
        box-shadow: 0 6px 0px #1f618d;
    }
    .vip-card {
        background: linear-gradient(135deg, #2c3e50, #000000);
        border: 4px solid gold;
        color: gold;
        box-shadow: 0 6px 0px #b8860b;
    }

    /* חלונית הסטטיסטיקות */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 15px;
        border-radius: 20px;
        border: 3px solid #f1f2f6;
        border-bottom: 6px solid #f1f2f6;
        margin-bottom: 20px;
    }
    .stat-item {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .stat-label {
        font-size: 14px;
        color: #7f8fa6;
    }

    /* אנימציית פתיחת קלפים בכספת */
    .flip-card {
      background-color: transparent;
      width: 100%;
      height: 350px;
      perspective: 1000px;
      margin-bottom: 30px;
    }
    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      transform-style: preserve-3d;
      cursor: pointer;
    }
    .flip-card:hover .flip-card-inner, .flip-card:active .flip-card-inner {
      transform: rotateY(180deg) scale(1.05);
    }
    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: 20px;
    }
    .flip-card-front {
      background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 26px;
      border: 5px solid #f1c40f;
      border-bottom: 10px solid #f39c12;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .flip-card-back {
      transform: rotateY(180deg);
      background-color: #2c3e50;
      border: 5px solid #f1c40f;
      border-bottom: 10px solid #f39c12;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 10px;
    }
    
    /* כפתורי סאבמיט מיוחדים (כמו כפתור Play במשחקים) */
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(180deg, #44bd32 0%, #4cd137 100%) !important;
        color: white !important;
        font-size: 26px !important;
        border-radius: 25px !important;
        border: none !important;
        border-bottom: 8px solid #27ae60 !important;
        padding: 10px 0 !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    div[data-testid="stFormSubmitButton"] button:active {
        border-bottom: 2px solid #27ae60 !important;
        transform: translateY(6px) !important;
    }
    
    /* התאמה לסלולר */
    @media (max-width: 768px) {
        .question-box { font-size: 24px !important; padding: 20px; }
        .flip-card { height: 280px; }
        div[data-testid="stFormSubmitButton"] button { font-size: 20px !important; }
    }
</style>
""", unsafe_allow_html=True)

# אפקטים קוליים
def play_sound(sound_type):
    if sound_type == "correct":
        audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg"></audio>"""
    elif sound_type == "wrong":
        audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3" type="audio/mpeg"></audio>"""
    elif sound_type == "level_up":
        audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3" type="audio/mpeg"></audio>"""
    elif sound_type == "loot":
        audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2018/2018-preview.mp3" type="audio/mpeg"></audio>"""
    else: return
    st.markdown(audio_html, unsafe_allow_html=True)

# פונקציית הקראה קולית
def speak_text(text_en, text_he=""):
    safe_en = text_en.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    if text_he:
        safe_he = text_he.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
        html_code = f"""
        <div style='display:flex; justify-content:center; gap:10px; margin-bottom: 5px; flex-wrap: wrap;'>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_he}'); msg.lang='he-IL'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
            style="background-color:#3498db; color:white; border:none; padding:10px 20px; border-radius:15px; border-bottom: 4px solid #2980b9; cursor:pointer; font-size:18px; font-weight:bold;">
                🔊 הקרא בעברית
            </button>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_en}'); msg.lang='en-US'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
            style="background-color:#F39C12; color:white; border:none; padding:10px 20px; border-radius:15px; border-bottom: 4px solid #d35400; cursor:pointer; font-size:18px; font-weight:bold;">
                🔊 הקרא באנגלית
            </button>
        </div>
        """
    else:
        html_code = f"""
        <div style='display:flex; justify-content:center; margin-bottom: 5px;'>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_en}'); msg.lang='en-US'; msg.rate=0.85; window.speechSynthesis.speak(msg);" 
            style="background-color:#F39C12; color:white; border:none; padding:10px 20px; border-radius:15px; border-bottom: 4px solid #d35400; cursor:pointer; font-size:18px; font-weight:bold;">
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
        heb_to_eng = {w[1]: w[0] for w in words}

        questions = []
        for eng, heb in words:
            distractors = random.sample([h for h in all_hebrew if h != heb], 3)
            options = distractors + [heb]
            random.shuffle(options)

            if is_toddler:
                # משפט בעברית, המילה המבוקשת באנגלית, ותשובות בעברית עם תמונה!
                options_with_pics = [f"{h} {toddler_pics.get(heb_to_eng.get(h, ''), '✨')}" for h in options]
                correct_with_pic = f"{heb} {toddler_pics.get(eng, '✨')}"

                q_text1 = f"ילדים אלופים, מה הפירוש של המילה באנגלית '{eng}'?"
                hint1 = f"💡 רמז קסם: התשובה מתחילה באות '{heb[0]}'."
                audio_he1 = f"ילדים אלופים, מה הפירוש של המילה באנגלית {eng}?"
                audio_en1 = eng

                questions.append({
                    "q": q_text1, "correct": correct_with_pic, "options": options_with_pics, "hint": hint1,
                    "audio_he": audio_he1, "audio_en": audio_en1
                })
                # לגילאי 4-6 נכניס רק את סוג השאלה הזה כפי שביקשת
            else:
                q_text1 = f"What is the meaning of the word '{eng}'?"
                hint1 = f"💡 רמז סודי: התשובה בעברית מתחילה באות '{heb[0]}'."
                questions.append({"q": q_text1, "correct": heb, "options": options, "hint": hint1, "audio_he": "", "audio_en": q_text1})

                # שאלת השלמה לאנגלית לילדים הגדולים יותר
                distractors_eng = random.sample([w[0] for w in words if w[0] != eng], 3)
                options_eng = distractors_eng + [eng]
                random.shuffle(options_eng)
                
                q_text2 = f"How do you say '{heb}' in English?"
                hint2 = f"💡 רמז סודי: התשובה באנגלית מתחילה באות '{eng[0]}'."
                questions.append({"q": q_text2, "correct": eng, "options": options_eng, "hint": hint2, "audio_he": "", "audio_en": q_text2})

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
                q1 = {"q": f"Where did {name} go?", "correct": f"To the {place}", "options": [f"To the {place}", "To the school", "To the hospital", "To the shop"], "hint": "💡 רמז: מצאו את המשפט הראשון בטקסט."}
                q2 = {"q": f"How many {item} did {name} see?", "correct": str(num), "options": [str(num), str(num+1), "One", "Zero"], "hint": "💡 רמז: חפשו את המספר המדויק בטקסט."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
            elif age_group == "10-12":
                place, item = random.choice(places_10_12)
                friend = random.choice([n for n in names if n != name])
                passage = f"{name} and {friend} decided to visit the {place} last weekend. They spent three hours looking at the amazing {item}. After that, they were very hungry, so they bought a large pizza."
                q1 = {"q": f"Who did {name} go with to the {place}?", "correct": friend, "options": [friend, "Mom", "A teacher", "Nobody"], "hint": "💡 רמז: מי מוזכר במשפט הראשון יחד עם הדמות?"}
                q2 = {"q": f"What did they do because they were hungry?", "correct": "Bought a large pizza", "options": ["Bought a large pizza", "Went to sleep", "Drank water", f"Looked at {item}"], "hint": "💡 רמז: קראו את המשפט האחרון (After that...)."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
            elif age_group == "13-15":
                place, item = random.choice(places_13_15)
                years = random.randint(3, 8)
                passage = f"Traveling to a {place} can be a life-changing experience. {name}, a young traveler, spent {years} months saving money for this journey. During the trip, {name} was fascinated by the incredible {item} and learned a lot about the local culture and traditions."
                q1 = {"q": f"Why is {name}'s experience described as significant?", "correct": "It was a life-changing experience.", "options": ["It was a life-changing experience.", "It was extremely boring.", "It took too much time.", "It was a terrible mistake."], "hint": "💡 רמז: קראו את תחילת הפסקה."}
                q2 = {"q": f"How long did {name} save money for the journey?", "correct": f"{years} months", "options": [f"{years} months", f"{years} years", "One week", "A few days"], "hint": "💡 רמז: חפשו את המספר המציין את משך הזמן."}
                unseens.extend([{"passage": passage, **q1}, {"passage": passage, **q2}])
        return unseens

    raw_vocab_4_6 = "Dog:כלב|Cat:חתול|Sun:שמש|Water:מים|Boy:ילד|Girl:ילדה|Red:אדום|Blue:כחול|Green:ירוק|Yellow:צהוב|One:אחד|Two:שתיים|Three:שלוש|Four:ארבע|Five:חמש|Apple:תפוח|Banana:בננה|Car:מכונית|Ball:כדור|Yes:כן|No:לא|Hello:שלום|Bye:להתראות|Mom:אמא|Dad:אבא|Eye:עין|Nose:אף|Mouth:פה|Ear:אוזן|Hand:יד|Leg:רגל|Big:גדול|Small:קטן|Happy:שמח|Sad:עצוב|Hot:חם|Cold:קר|Milk:חלב|Tree:עץ|Flower:פרח|Bird:ציפור|Fish:דג|House:בית|Door:דלת|Window:חלון|Bed:מיטה|Morning:בוקר|Night:לילה"
    raw_vocab_7_9 = "Apple:תפוח|Dog:כלב|Cat:חתול|Sun:שמש|Water:מים|Moon:ירח|Star:כוכב|Fish:דג|Bird:ציפור|Cow:פרה|Horse:סוס|Tree:עץ|Flower:פרח|Car:מכונית|Bus:אוטובוס|Train:רכבת|House:בית|Door:דלת|Window:חלון|Table:שולחן|Chair:כיסא|Book:ספר|Pen:עט|School:בית ספר|Teacher:מורה|Mother:אמא|Father:אבא|Brother:אח|Sister:אחות|Baby:תינוק|Hand:יד|Foot:רגל|Eye:עין|Ear:אוזן|Nose:אף|Mouth:פה|Head:ראש|Red:אדום|Blue:כחול|Green:ירוק|Yellow:צהוב|Black:שחור|White:לבן|Pink:ורוד|Orange:כתום|Brown:חום|Happy:שמח|Sad:עצוב|Big:גדול|Small:קטן|Hot:חם|Cold:קר|Good:טוב|Bad:רע|Fast:מהיר|Slow:איטי|Play:לשחק|Jump:לקפוץ|Run:לרוץ|Sleep:לישון|Eat:לאכול|Drink:לשתות|Milk:חלב|Bread:לחם|Cheese:גבינה|Meat:בשר|Cake:עוגה|Candy:סוכריה|Toy:צעצוע|Ball:כדור|Park:פארק|Zoo:גן חיות"
    grammar_7_9 = []
    base_templates_7_9 = [("I", "am", ["is", "are", "be"], "a good student."), ("He", "is", ["am", "are", "be"], "a tall boy."), ("She", "is", ["am", "are", "be"], "my smart sister."), ("It", "is", ["am", "are", "be"], "a small brown dog."), ("We", "are", ["is", "am", "be"], "happy friends."), ("They", "are", ["is", "am", "be"], "at the big school."), ("You", "are", ["is", "am", "be"], "a very nice teacher.")]
    for i in range(50):
        base = base_templates_7_9[i % len(base_templates_7_9)]
        subj, ans, wrong, rest = base
        options = [ans] + wrong
        random.shuffle(options)
        grammar_7_9.append({"q": f"{subj} ___ {rest}", "correct": ans, "options": options, "hint": "💡 רמז דקדוקי: He, She, It מקבלים תמיד 'is'. I מקבל 'am'. We, You, They מקבלים 'are'."})

    raw_vocab_10_12 = "Yesterday:אתמול|Tomorrow:מחר|Today:היום|Always:תמיד|Never:אף פעם|Sometimes:לפעמים|Usually:בדרך כלל|Beautiful:יפה|Ugly:מכוער|Smart:חכם|Stupid:טיפש|Clean:נקי|Dirty:מלוכלך|Easy:קל|Hard:קשה|Heavy:כבד|Light:קל|Strong:חזק|Weak:חלש|Rich:עשיר|Poor:עני|Early:מוקדם|Late:מאוחר|Right:נכון|Wrong:לא נכון|Friend:חבר|Enemy:אויב|Neighbor:שכן|Question:שאלה|Answer:תשובה|Word:מילה|Sentence:משפט|Month:חודש|Year:שנה|Spring:אביב|Summer:קיץ|Autumn:סתיו|Winter:חורף|Holiday:חג|Vacation:חופשה|Money:כסף|Buy:לקנות|Sell:למכור|Pay:לשלם|Clothes:בגדים|Shirt:חולצה|Pants:מכנסיים|Dress:שמלה|Shoes:נעליים|Weather:מזג אוויר|Cloud:ענן|Storm:סערה|River:נהר|Sea:ים|Mountain:הר|Forest:יער|Animal:חיה|Safe:בטוח|Help:לעזור|Work:לעבוד|Job:עבודה|Doctor:רופא|Police:משטרה"
    grammar_10_12 = []
    base_templates_10_12 = [("Yesterday, I ___ to the beautiful park.", "went", "go", "going", "goes"), ("Last night, we ___ a giant delicious pizza.", "ate", "eat", "eating", "eats"), ("Two days ago, she ___ a colorful bird in the sky.", "saw", "see", "seeing", "sees"), ("My father ___ a new red car last week.", "bought", "buy", "buying", "buys"), ("He ___ his difficult homework yesterday afternoon.", "did", "do", "doing", "does")]
    for i in range(50):
        base = base_templates_10_12[i % len(base_templates_10_12)]
        sentence, v_past, v_pres, v_ing, v_s = base
        options = [v_past, v_pres, v_ing, v_s]
        random.shuffle(options)
        grammar_10_12.append({"q": sentence, "correct": v_past, "options": options, "hint": "💡 רמז דקדוקי: שימו לב למילות הזמן (Yesterday, Last, Ago)! הן מצביעות על זמן עבר (Past Simple)."})

    raw_vocab_13_15 = "Environment:סביבה|Pollution:זיהום|Climate:אקלים|Discover:לגלות|Invent:להמציא|Technology:טכנולוגיה|Society:חברה|Culture:תרבות|Tradition:מסורת|Government:ממשלה|Election:בחירות|Law:חוק|Crime:פשע|Punishment:עונש|Justice:צדק|Peace:שלום|War:מלחמה|Army:צבא|Soldier:חייל|Weapon:נשק|Economy:כלכלה|Business:עסק|Company:חברה|Factory:מפעל|Industry:תעשייה|Trade:סחר|Import:ייבוא|Export:ייצוא|Profit:רווח|Loss:הפסד|Success:הצלחה|Failure:כישלון|Challenge:אתגר|Opportunity:הזדמנות|Advantage:יתרון|Disadvantage:חיסרון|Benefit:תועלת|Harm:נזק|Risk:סיכון|Protect:להגן|Destroy:להרוס|Create:ליצור|Improve:לשפר|Develop:לפתח|Grow:לגדול/לצמוח|Reduce:להפחית|Increase:להגדיל|Measure:למדוד|Compare:להשוות|Explain:להסביר|Describe:לתאר|Argue:להתווכח|Agree:להסכים|Disagree:לא להסכים|Opinion:דעה|Fact:עובדה|Evidence:ראיה|Prove:להוכיח|Suggest:להציע|Advise:לייעץ|Recommend:להמליץ|Decide:להחליט|Choose:לבחור|Result:תוצאה|Cause:גורם|Reason:סיבה|Purpose:מטרה|Goal:יעד|Achieve:להשיג|Succeed:להצליח|Fail:להיכשל|Effort:מאמץ|Energy:אנרגיה"
    grammar_13_15 = []
    base_templates_13_15 = [("give", "up", "להיכנע/לוותר", "You should never give ___ on your dreams and goals."), ("look", "after", "לשמור על/לטפל ב-", "She stays at home to look ___ her little brother."), ("take", "off", "להמריא", "The airplane is ready to take ___ from the airport runway."), ("find", "out", "לגלות", "We need to find ___ the secret truth about this mystery.")]
    for i in range(50):
        base = base_templates_13_15[i % len(base_templates_13_15)]
        verb, prep, mean, sentence = base
        distractors = random.sample([p for p in ["in", "on", "at", "over", "down", "away", "up", "off", "out", "to", "of"] if p != prep], 3)
        options = [prep] + distractors
        random.shuffle(options)
        grammar_13_15.append({"q": f"Choose the correct preposition to complete the phrasal verb: {sentence}", "correct": prep, "options": options, "hint": f"💡 רמז סודי: מדובר ב-Phrasal Verb. השילוב של הפועל '{verb}' יחד עם מילת היחס הנכונה יוצר את המשמעות '{mean}'."})

    def build_massive_pool(raw_vocab, grammar_list, age):
        pool = []
        is_toddler = (age == "4-6")
        pool.extend(generate_vocab_questions(raw_vocab, 350 if is_toddler else 300, is_toddler))
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
# 2. מערכת התחברות
# ==========================================
def load_db():
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def save_db(db_data):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)

if 'user_db' not in st.session_state: st.session_state.user_db = load_db()
query_params = st.query_params

if 'logged_in_user' not in st.session_state:
    if "user" in query_params and query_params["user"] in st.session_state.user_db:
        st.session_state.logged_in_user = query_params["user"]
    else: st.session_state.logged_in_user = None

if 'show_vault' not in st.session_state: st.session_state.show_vault = False

if st.session_state.logged_in_user is None:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("👑 ממלכת האנגלית של המקצוענים!")
    st.subheader("שחקו, למדו, אספו קלפים נדירים ושדרגו את השחקן שלכם!")
    
    tab_login, tab_register = st.tabs(["👋 התחברות משתמש קיים", "✨ הרשמה (משתמש חדש)"])

    with tab_login:
        with st.form("form_login"):
            u_name = st.text_input("שם משתמש:")
            u_pass = st.text_input("סיסמה:", type="password")
            submit_l = st.form_submit_button("היכנס למשחק 🚀")
            if submit_l:
                if u_name in st.session_state.user_db and st.session_state.user_db[u_name]["password"] == u_pass:
                    st.session_state.logged_in_user = u_name
                    st.query_params["user"] = u_name
                    data = st.session_state.user_db[u_name]
                    st.session_state.age_level = data.get("age_level", "4-6")
                    st.session_state.score = data.get("score", 0)
                    st.session_state.stars = data.get("stars", 0)
                    st.session_state.xp = data.get("xp", 0) 
                    st.session_state.avatar = data.get("avatar", "😎")
                    st.session_state.current_stage = data.get("current_stage", 1)
                    st.session_state.current_q_index = data.get("current_q_index", 0)
                    st.session_state.streak = data.get("streak", 0)
                    st.session_state.my_prizes = data.get("my_prizes", [])
                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    st.session_state.show_vault = False
                    st.rerun()
                else: st.error("שם משתמש או סיסמה שגויים. נסו שוב!")

    with tab_register:
        with st.form("form_reg"):
            new_u = st.text_input("בחר שם משתמש:")
            new_p = st.text_input("בחר סיסמה:", type="password")
            age_select = st.radio("בחר את קבוצת הגיל שלך:", ["4-6", "7-9", "10-12", "13-15"], horizontal=True)
            avatar_select = st.radio("בחר סמל שחקן (אווטאר):", AVATARS, horizontal=True)

            submit_r = st.form_submit_button("צור חשבון והתחל להרוויח כוכבים! 🌟")
            if submit_r:
                if not new_u or not new_p: st.warning("נא למלא את כל הפרטים.")
                elif new_u in st.session_state.user_db: st.error("שם משתמש זה כבר קיים במערכת.")
                else:
                    st.session_state.user_db[new_u] = {"password": new_p, "age_level": age_select, "score": 0, "stars": 50, "xp": 0, "avatar": avatar_select, "current_stage": 1, "current_q_index": 0, "streak": 0, "my_prizes": []}
                    save_db(st.session_state.user_db)
                    st.session_state.logged_in_user = new_u
                    st.query_params["user"] = new_u
                    st.session_state.age_level = age_select
                    st.session_state.avatar = avatar_select
                    st.session_state.score = 0
                    st.session_state.stars = 50 
                    st.session_state.xp = 0
                    st.session_state.current_stage = 1
                    st.session_state.current_q_index = 0
                    st.session_state.streak = 0
                    st.session_state.my_prizes = []
                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    st.session_state.show_vault = False
                    st.toast("🎉 קיבלת 50 כוכבים במתנה להרשמה!")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. מסך המשחק הראשי 
# ==========================================
else:
    def sync_data():
        u = st.session_state.logged_in_user
        st.session_state.user_db[u].update({"age_level": st.session_state.age_level, "score": st.session_state.score, "stars": st.session_state.stars, "xp": st.session_state.xp, "current_stage": st.session_state.current_stage, "current_q_index": st.session_state.current_q_index, "streak": st.session_state.streak, "my_prizes": st.session_state.my_prizes, "last_login": datetime.now().strftime("%Y-%m-%d")})
        save_db(st.session_state.user_db)
        
    # חישוב הדרגה לפי ה-XP
    # במקום הקוד הקודם, תכתוב את זה:
    xp_val = st.session_state.get('xp', 0)

    if xp_val >= 1000: rank = "אגדה 👑"
    elif xp_val >= 600: rank = "אלוף 🏆"
    elif xp_val >= 300: rank = "מקצוען 🥇"
    elif xp_val >= 100: rank = "מתקדם 🥈"
    else: rank = "טירון 🥉"

    with st.sidebar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; font-size: 60px; margin:0; filter: drop-shadow(0px 5px 2px rgba(0,0,0,0.2));'>{st.session_state.avatar}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; margin-top:5px;'>{st.session_state.logged_in_user}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: #8e44ad; margin-top:-10px;'>דרגה: {rank}</h4>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">⭐<br>{st.session_state.stars}<br><span class="stat-label">כוכבים</span></div>
            <div class="stat-item">🔥<br>{st.session_state.streak}<br><span class="stat-label">רצף</span></div>
            <div class="stat-item">⚡<br>{st.session_state.xp}<br><span class="stat-label">XP</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🆙 שלב: **{st.session_state.current_stage}** / 50")

        new_age = st.selectbox("🔄 שנה רמה:", ["4-6", "7-9", "10-12", "13-15"], index=["4-6", "7-9", "10-12", "13-15"].index(st.session_state.age_level), key="change_user_age_level")
        if new_age != st.session_state.age_level:
            st.session_state.age_level = new_age
            sync_data()
            st.rerun()

        st.write("---")

        st.subheader("🛍️ חנות הקלפים והפרסים")
        shop_items = [
            {"name": "🍦 גלידת קצפת ענקית", "cost": 20, "stage": 1, "type": "normal"},
            {"name": "🐉 דרקון אש חמוד", "cost": 40, "stage": 1, "type": "normal"},
            {"name": "🔥 קלף פוקימון Charizard", "cost": 100, "stage": 3, "type": "pokemon"},
            {"name": "⚡ קלף פוקימון Pikachu", "cost": 150, "stage": 5, "type": "pokemon"},
            {"name": "🌊 קלף פוקימון Blastoise", "cost": 150, "stage": 8, "type": "pokemon"},
            {"name": "⚽ חפיסת קלפי מסי זהב", "cost": 200, "stage": 10, "type": "soccer"},
            {"name": "🏆 קלף רונאלדו נדיר", "cost": 250, "stage": 13, "type": "soccer"},
            {"name": "🎧 אוזניות אפל Airpods", "cost": 300, "stage": 15, "type": "gadget"},
            {"name": "🌟 מארז קלפי כדורגל", "cost": 350, "stage": 18, "type": "soccer"},
            {"name": "🤖 רובוט אינטראקטיבי", "cost": 350, "stage": 20, "type": "gadget"},
            {"name": "💻 מחשב גיימינג מפלצתי", "cost": 400, "stage": 23, "type": "gadget"},
            {"name": "📱 אייפון 15 פרו מקס", "cost": 450, "stage": 25, "type": "gadget"},
            {"name": "🛹 הוברבורד חשמלי", "cost": 450, "stage": 28, "type": "gadget"},
            {"name": "🎮 סוני פלייסטיישן 5", "cost": 500, "stage": 30, "type": "gadget"},
            {"name": "🥽 משקפי מציאות מדומה VR", "cost": 550, "stage": 33, "type": "gadget"},
            {"name": "🦸‍♂️ קלף ספיידרמן נדיר", "cost": 600, "stage": 35, "type": "marvel"},
            {"name": "⚔️ חרב נינג'ה זוהרת", "cost": 650, "stage": 38, "type": "normal"},
            {"name": "🦄 בובת חד קרן ענקית", "cost": 700, "stage": 40, "type": "normal"},
            {"name": "🛸 רחפן צילום מקצועי", "cost": 750, "stage": 43, "type": "gadget"},
            {"name": "🏎️ מכונית על למבורגיני", "cost": 800, "stage": 45, "type": "normal"},
            {"name": "🪄 שרביט קסמים אמיתי", "cost": 900, "stage": 48, "type": "normal"},
            {"name": "👑 כתר יהלומים", "cost": 1000, "stage": 50, "type": "vip"},
            {"name": "💎 תיבת אוצר מסתורית", "cost": 1500, "stage": 50, "type": "vip"}
        ]

        # שימוש ל-XP - פתיחת קופסאות הפתעה!
        st.markdown('<div class="vip-card" style="border-color: #9b59b6;">🎁 <b>קופסת הפתעה אגדית!</b><br>הגרלת פרס רנדומלי! (100 XP)</div>', unsafe_allow_html=True)
        if st.button("פתח קופסת הפתעה ב-100 ⚡", use_container_width=True):
            if st.session_state.xp >= 100:
                st.session_state.xp -= 100
                available_prizes = [i["name"] for i in shop_items if i["name"] not in st.session_state.my_prizes]
                if available_prizes:
                    random_prize = random.choice(available_prizes)
                    st.session_state.my_prizes.append(random_prize)
                    play_sound("loot")
                    st.balloons()
                    st.success(f"🎉 וואו! פתחתם את הקופסה וקיבלתם: **{random_prize}**!")
                    sync_data()
                    time.sleep(2)
                    st.rerun()
                else: st.warning("יש לכם כבר את כל הפרסים במשחק!")
            else: st.error("אין לכם מספיק XP. ענו נכונה כדי להרוויח!")

        st.write("---")
        for item in shop_items:
            is_locked = st.session_state.current_stage < item['stage']
            is_owned = item['name'] in st.session_state.my_prizes
            disabled_btn = st.session_state.stars < item['cost'] or is_owned or is_locked

            btn_text = f"🔒 נפתח בשלב {item['stage']}" if is_locked else ("ברשותך! ✅" if is_owned else f"קנה ב-{item['cost']} ⭐")

            if not is_locked and item['type'] == 'pokemon':
                st.markdown(f'<div class="trading-card-pokemon">⭐ POKÉMON CARD ⭐<br><b>{item["name"].split("!")[0]}</b></div>', unsafe_allow_html=True)
            elif not is_locked and item['type'] == 'soccer':
                st.markdown(f'<div class="trading-card-soccer">⚽ MATCH ATTAX ⚽<br><b>{item["name"]}</b></div>', unsafe_allow_html=True)
            elif not is_locked and item['type'] in ['gadget', 'marvel', 'vip']:
                st.markdown(f'<div class="vip-card">✨ VIP ITEM ✨<br><b>{item["name"]}</b></div>', unsafe_allow_html=True)
            else:
                st.write(f"**{item['name']}**")

            if st.button(btn_text, key=f"buy_{item['name']}", disabled=disabled_btn, use_container_width=True):
                st.session_state.stars -= item['cost']
                st.session_state.my_prizes.append(item['name'])
                play_sound("loot")
                sync_data()
                st.balloons()
                st.toast("🎉 איזה כיף! הפרס נכנס לכספת שלך!")
                time.sleep(1)
                st.rerun()
        st.write("---")

        if st.button("💼 אלבום הקלפים והכספת שלי!", type="primary", use_container_width=True):
            st.session_state.show_vault = True
            st.rerun()

        if st.button("🚪 התנתק ושמור", use_container_width=True):
            sync_data()
            st.session_state.logged_in_user = None
            st.query_params.clear()
            st.session_state.show_vault = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- חלון כספת הפרסים ---
    if st.session_state.show_vault:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.title("💼 אלבום הקלפים וכספת הפרסים שלי!")
        st.subheader("ריחפו עם העכבר (או לחצו במסך מגע) על חבילות הקלפים כדי לפתוח ולחשוף אותם!")

        if not st.session_state.my_prizes:
            st.info("הכספת שלכם ריקה בינתיים... חזרו למשחק, הרוויחו כוכבים וקנו קלפי פוקימון ופרסים נדירים בחנות!")
        else:
            cols = st.columns(3) # במסכים קטנים/ניידים Streamlit הופך את זה אוטומטית לעמודה 1 מתחת לשנייה
            for i, prize_name in enumerate(st.session_state.my_prizes):
                with cols[i % 3]:
                    image_url = PRIZE_IMAGES.get(prize_name, "https://via.placeholder.com/300")
                    html_card = f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                🎁<br>הקליקו/רחפו לפתיחת החבילה!<br><br><span style="font-size:18px;">{prize_name.split('!')[0]}</span>
                            </div>
                            <div class="flip-card-back">
                                <img src="{image_url}" style="width:100%; height:100%; object-fit:contain; border-radius:15px; background-color:#2c3e50;">
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
        st.title(f"👑 שלב {st.session_state.current_stage} 👑")

        if st.session_state.current_stage > 50:
            st.balloons()
            st.success("🏆 מדהים! השלמתם את כל 50 השלבים ופתרתם את כל השאלות ברמה שלכם!")
        else:
            pool = st.session_state.questions_by_age[st.session_state.age_level]
            global_index = ((st.session_state.current_stage - 1) * 8) + st.session_state.current_q_index
            q_data = pool[global_index]

            progress = (st.session_state.current_q_index) / 8.0
            st.progress(progress)
            st.markdown(f"**שאלה {st.session_state.current_q_index + 1} מתוך 8**")

            if st.session_state.age_level == "4-6":
                st.markdown(f'<div class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
                speak_text(text_en=q_data.get("audio_en", ""), text_he=q_data.get("audio_he", ""))
            else:
                if q_data.get("passage"):
                    st.markdown(f'<div style="direction: ltr; text-align: left; background-color: #e8f6f3; padding: 20px; border-radius: 20px; font-size: 20px; margin-bottom: 20px; border-left: 6px solid #1abc9c; color: #2c3e50; font-weight: bold;">📖 <b>Reading Passage:</b><br>{q_data["passage"]}</div>', unsafe_allow_html=True)
                    speak_text(text_en=q_data["passage"] + " Question: " + q_data["q"])
                    st.markdown(f'<div style="direction: ltr;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="direction: ltr;" class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
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
                                st.session_state.xp += 10
                                st.session_state.streak += 1
                                play_sound("correct")
                            else:
                                st.session_state.streak = 0
                                play_sound("wrong")
                            sync_data() 
                            st.rerun()

                with st.expander("💡 צריך עזרה? לחץ כאן לקבלת רמז סודי וחכם"):
                    st.info(q_data["hint"])

            else:
                for opt in q_data['options']:
                    if opt == q_data['correct']:
                        st.success(f"🟢 **{opt}** (זו התשובה הנכונה!)")
                    elif opt == st.session_state.user_choice:
                        st.error(f"🔴 **{opt}** (הבחירה שלך)")
                    else:
                        st.write(f"⚪ {opt}")

                if st.session_state.user_choice == q_data['correct']:
                    st.markdown("## 🎉 כל הכבוד אלופים! צדקתם והרווחתם **25 כוכבי קסם!** ⭐ ו-10 XP! ⚡")
                else:
                    st.markdown(f"## 🌟 לא נורא, במשחק תמיד אפשר לנסות שוב! התשובה היא: **{q_data['correct']}**")

                if st.button("קדימה, לשאלה הבאה! 🚀", type="primary", use_container_width=True):
                    st.session_state.current_q_index += 1
                    if st.session_state.current_q_index >= 8:
                        st.session_state.current_stage += 1
                        st.session_state.current_q_index = 0
                        st.session_state.stars += 100
                        st.session_state.xp += 50
                        play_sound("level_up")
                        st.toast("🏆 איזה אלופים! סיימתם שלב שלם וקיבלתם בונוס של 100 כוכבים ו-50 XP!")

                    st.session_state.answered_current = False
                    st.session_state.user_choice = None
                    sync_data() 
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
