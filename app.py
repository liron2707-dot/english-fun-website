import streamlit as st
import random
import streamlit.components.v1 as components
import json
import os
import time
import hashlib
from datetime import datetime

# ==========================================
# הגדרות עמוד ותצוגה - חובה להיות ראשון!
# ==========================================
st.set_page_config(
    page_title="ממלכת האנגלית - מהדורת Brawl Stars!",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# קובץ השמירה של המשתמשים
# ==========================================
USER_DB_FILE = "users_db.json"

# ==========================================
# מאגר התמונות - קישורים יציבים (ללא בעיות Hotlinking)
# ==========================================
PRIZE_IMAGES = {
    "🔥 קלף פוקימון Charizard VMAX": "https://images.pokemontcg.io/swsh3/20_hires.png",
    "⚡ קלף פוקימון Pikachu Gold": "https://images.pokemontcg.io/ex13/104_hires.png",
    "🌊 קלף פוקימון Blastoise Holographic": "https://images.pokemontcg.io/base1/2_hires.png",
    "⚽ קלף מסי - Match Attax Rare": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
    "🏆 קלף רונאלדו - Adrenalyn XL": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
    "🌟 מארז פרימיום Match Attax 2025": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Soccerball.svg",
    "🎁 תיבת מגה (Mega Box) ברולסטארס": "https://upload.wikimedia.org/wikipedia/commons/a/af/Treasure_chest_open_icon.svg",
    "🌵 סקין ספייק - ברולסטארס": "https://upload.wikimedia.org/wikipedia/commons/5/53/Cactus_icon.svg",
    "🦅 סקין קרואו - ברולסטארס": "https://upload.wikimedia.org/wikipedia/commons/3/30/Crow_icon.svg",
    "💎 קופסת יהלומים ענקית": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Diamond_icon.svg",
    "📱 אייפון 15 פרו מקס": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    "🎮 סוני פלייסטיישן 5": "https://upload.wikimedia.org/wikipedia/commons/3/39/PS5_logo.svg"
}

ALL_SHOP_ITEMS = [
    {"name": "🔥 קלף פוקימון Charizard VMAX", "cost": 150, "type": "stars"},
    {"name": "⚡ קלף פוקימון Pikachu Gold", "cost": 150, "type": "stars"},
    {"name": "🌊 קלף פוקימון Blastoise Holographic", "cost": 150, "type": "stars"},
    {"name": "⚽ קלף מסי - Match Attax Rare", "cost": 250, "type": "stars"},
    {"name": "🏆 קלף רונאלדו - Adrenalyn XL", "cost": 250, "type": "stars"},
    {"name": "🌟 מארז פרימיום Match Attax 2025", "cost": 300, "type": "stars"},
    {"name": "🎁 תיבת מגה (Mega Box) ברולסטארס", "cost": 300, "type": "xp"},
    {"name": "🌵 סקין ספייק - ברולסטארס", "cost": 500, "type": "xp"},
    {"name": "🦅 סקין קרואו - ברולסטארס", "cost": 500, "type": "xp"},
    {"name": "💎 קופסת יהלומים ענקית", "cost": 800, "type": "xp"},
    {"name": "📱 אייפון 15 פרו מקס", "cost": 1500, "type": "xp"},
    {"name": "🎮 סוני פלייסטיישן 5", "cost": 2000, "type": "xp"}
]

AVATARS = ["😎", "🦄", "🚀", "🐱‍👤", "👑", "🐉", "🤖", "🦊"]

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

# ==========================================
# עיצוב מותאם (CSS) - סגנון משחק מובייל 
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Secular+One&family=Rubik:wght@400;600;800&display=swap');
    * { font-family: 'Secular One', sans-serif !important; }
    .rtl-container { direction: rtl; text-align: right; }
    [data-testid="stSidebar"] { direction: rtl; text-align: right; background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%); color: white !important; }
    .stButton > button, div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(180deg, #FFDE00 0%, #FD8A00 100%) !important;
        border: 3px solid #1a1a1a !important; border-radius: 16px !important; color: #1a1a1a !important;
        font-size: 22px !important; font-weight: 900 !important; box-shadow: 0px 6px 0px #1a1a1a !important; padding: 10px !important;
    }
    .stButton > button:active, div[data-testid="stFormSubmitButton"] button:active { transform: translateY(6px) !important; box-shadow: 0px 0px 0px #1a1a1a !important; }
    div[data-testid="stRadio"] label { background: white; border-radius: 16px; border: 3px solid #e0e0e0; margin-bottom: 8px; padding: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; }
    div[data-testid="stRadio"] label p { font-size: 35px !important; font-weight: bold; color: #2b2d42; }
    .question-box { font-size: 30px !important; color: #ffffff; background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); padding: 25px; border-radius: 20px; border: 4px solid #1a1a1a; box-shadow: 0 8px 0px #1a1a1a; text-align: center; margin-bottom: 30px; line-height: 1.4; }
    .stats-bar { display: flex; justify-content: space-around; background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 16px; border: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .stat-item { text-align: center; font-size: 24px; color: #FFDE00; text-shadow: 2px 2px 0px #000; }
    .store-card { background: white; border-radius: 15px; border: 3px solid #2d2d2d; padding: 15px; text-align: center; box-shadow: 0px 5px 0px #2d2d2d; margin-bottom: 15px; color: black; }
    [data-testid="collapsedControl"] { color: #FD8A00 !important; background-color: white !important; border-radius: 50% !important; box-shadow: 0px 2px 5px rgba(0,0,0,0.5); }
    img { max-width: 100% !important; height: auto !important; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

def play_sound(sound_type):
    if sound_type == "correct": audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg"></audio>"""
    elif sound_type == "wrong": audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3" type="audio/mpeg"></audio>"""
    elif sound_type in ["level_up", "loot"]: audio_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3" type="audio/mpeg"></audio>"""
    else: return
    st.markdown(audio_html, unsafe_allow_html=True)

def speak_text(text_en, text_he=""):
    safe_en = text_en.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    if text_he:
        safe_he = text_he.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
        html_code = f"""
        <div style='display:flex; justify-content:center; gap:10px; margin-bottom: 15px;'>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_he}'); msg.lang='he-IL'; window.speechSynthesis.speak(msg);" style="background:#3498db; color:white; border:2px solid black; padding:8px 15px; border-radius:10px; cursor:pointer; font-weight:bold; font-size: 16px;">🔊 שמע עברית</button>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_en}'); msg.lang='en-US'; window.speechSynthesis.speak(msg);" style="background:#e74c3c; color:white; border:2px solid black; padding:8px 15px; border-radius:10px; cursor:pointer; font-weight:bold; font-size: 16px;">🔊 שמע אנגלית</button>
        </div>"""
    else:
        html_code = f"""
        <div style='display:flex; justify-content:center; margin-bottom: 15px;'>
            <button onclick="var msg = new SpeechSynthesisUtterance('{safe_en}'); msg.lang='en-US'; window.speechSynthesis.speak(msg);" style="background:#e74c3c; color:white; border:2px solid black; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold; font-size: 18px;">🔊 לחץ לשמיעה באנגלית</button>
        </div>"""
    components.html(html_code, height=60)
    # ==========================================
# 2. מנוע האנסינים החכם, אוצר המילים והדקדוק
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
                options_with_pics = [f"{h} {toddler_pics.get(heb_to_eng.get(h, ''), '✨')}" for h in options]
                correct_with_pic = f"{heb} {toddler_pics.get(eng, '✨')}"
                q_text1 = f"איזו תמונה מתאימה למילה באנגלית: **{eng}**?"
                hint1 = f"💡 רמז קסם: התשובה בעברית מתחילה באות '{heb[0]}'."
                questions.append({
                    "q": q_text1, "correct": correct_with_pic, "options": options_with_pics, "hint": hint1,
                    "audio_he": f"איזו תמונה מתאימה למילה באנגלית {eng}?", "audio_en": eng
                })
            else:
                q_text1 = f"What is the meaning of the word '{eng}'?"
                hint1 = f"💡 רמז סודי: התשובה בעברית מתחילה באות '{heb[0]}'."
                questions.append({
                    "q": q_text1, "correct": heb, "options": options, "hint": hint1,
                    "audio_he": "", "audio_en": q_text1
                })
                
            distractors_eng = random.sample([w[0] for w in words if w[0] != eng], 3)
            options_eng = distractors_eng + [eng]
            random.shuffle(options_eng)
            
            if is_toddler:
                options_eng_with_pics = [f"{e} {toddler_pics.get(e, '✨')}" for e in options_eng]
                correct_eng_with_pic = f"{eng} {toddler_pics.get(eng, '✨')}"
                q_text2 = f"מי יודע איך אומרים באנגלית את המילה '{heb}'?"
                hint2 = f"💡 רמז קסם: התשובה באנגלית מתחילה באות '{eng[0]}'."
                questions.append({
                    "q": q_text2, "correct": correct_eng_with_pic, "options": options_eng_with_pics, "hint": hint2,
                    "audio_he": f"איך אומרים {heb} באנגלית?", "audio_en": eng
                })
            else:
                q_text2 = f"How do you say '{heb}' in English?"
                hint2 = f"💡 רמז סודי: התשובה באנגלית מתחילה באות '{eng[0]}'."
                questions.append({
                    "q": q_text2, "correct": eng, "options": options_eng, "hint": hint2,
                    "audio_he": "", "audio_en": q_text2
                })

        random.shuffle(questions)
        return questions[:amount]

    # ... (כאן תמשיך להוסיף את שאר הפונקציות כמו generate_dynamic_unseens וכו', וכולן צריכות להיות מוזחות פנימה תחת ה-if הזה)
    # לאחר סיום כל הפונקציות, בסוף הבלוק של ה-if, תכתוב:
    
    st.session_state.db_generated = True
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
                options_with_pics = [f"{h} {toddler_pics.get(heb_to_eng.get(h, ''), '✨')}" for h in options]
                correct_with_pic = f"{heb} {toddler_pics.get(eng, '✨')}"
                q_text1 = f"איזו תמונה מתאימה למילה באנגלית: **{eng}**?"
                hint1 = f"💡 רמז קסם: התשובה בעברית מתחילה באות '{heb[0]}'."
                questions.append({
                    "q": q_text1, "correct": correct_with_pic, "options": options_with_pics, "hint": hint1,
                    "audio_he": f"איזו תמונה מתאימה למילה באנגלית {eng}?", "audio_en": eng
                })
            else:
                q_text1 = f"What is the meaning of the word '{eng}'?"
                hint1 = f"💡 רמז סודי: התשובה בעברית מתחילה באות '{heb[0]}'."
                questions.append({
                    "q": q_text1, "correct": heb, "options": options, "hint": hint1,
                    "audio_he": "", "audio_en": q_text1
                })
                
            distractors_eng = random.sample([w[0] for w in words if w[0] != eng], 3)
            options_eng = distractors_eng + [eng]
            random.shuffle(options_eng)
            
            if is_toddler:
                options_eng_with_pics = [f"{e} {toddler_pics.get(e, '✨')}" for e in options_eng]
                correct_eng_with_pic = f"{eng} {toddler_pics.get(eng, '✨')}"
                q_text2 = f"מי יודע איך אומרים באנגלית את המילה '{heb}'?"
                hint2 = f"💡 רמז קסם: התשובה באנגלית מתחילה באות '{eng[0]}'."
                questions.append({
                    "q": q_text2, "correct": correct_eng_with_pic, "options": options_eng_with_pics, "hint": hint2,
                    "audio_he": f"איך אומרים {heb} באנגלית?", "audio_en": eng
                })
            else:
                q_text2 = f"How do you say '{heb}' in English?"
                hint2 = f"💡 רמז סודי: התשובה באנגלית מתחילה באות '{eng[0]}'."
                questions.append({
                    "q": q_text2, "correct": eng, "options": options_eng, "hint": hint2,
                    "audio_he": "", "audio_en": q_text2
                })

        random.shuffle(questions)
        return questions[:amount]

    # אנסינים מתקדמים הדורשים הסקת מסקנות
    def generate_dynamic_unseens(age_group, amount):
        unseens = []
        names = ["Danny", "Maya", "Tom", "Sarah", "David", "Anna", "Ben", "Emma"]
        for _ in range(amount):
            name = random.choice(names)
            if age_group == "7-9":
                situations = [
                    ("There were dark grey clouds and water was falling from the sky.", "Rainy", ["Rainy", "Sunny", "Snowy", "Windy"]),
                    ("The sky was bright blue and everyone was wearing sunglasses.", "Sunny", ["Sunny", "Rainy", "Cold", "Snowy"])
                ]
                sit = random.choice(situations)
                passage = f"{name} looked out the window. {sit[0]} {name} decided what to wear."
                q1 = {"q": "What was the weather like?", "correct": sit[1], "options": sit[2], "hint": "💡 רמז: תחשבו איזו מילה מתארת את מה שקורה בחוץ."}
                unseens.append({"passage": passage, **q1})

            elif age_group == "10-12":
                situations = [
                    ("He looked at the clock, grabbed his bag, and ran as fast as he could to the bus stop, but the yellow vehicle was already gone.", "He was late for school"),
                    ("Her stomach was making loud noises and she couldn't stop thinking about the big sandwich in her bag.", "She was hungry")
                ]
                sit = random.choice(situations)
                passage = f"It was 8:00 AM. {sit[0]} It was going to be a long day."
                q1 = {"q": "What is the actual problem here?", "correct": sit[1], "options": [sit[1], "They wanted to sleep", "They lost a phone", "They were sick"], "hint": "💡 רמז: קראו בין השורות. מה קרה באמת?"}
                unseens.append({"passage": passage, **q1})

            elif age_group == "13-15":
                topics = [
                    ("Despite their exhaustion and aching muscles, the athletes kept pushing their limits until the final whistle.", "They were highly determined.", ["They were highly determined.", "They wanted to quit.", "They were very lazy.", "They didn't care about the game."]),
                    ("The sudden software update caused massive disruptions across the company's network, leaving technicians scrambling for hours to restore order.", "The update was highly problematic.", ["The update was highly problematic.", "The update improved performance.", "The technicians were bored.", "The network was untouched."])
                ]
                topic = random.choice(topics)
                passage = f"It was a day full of unexpected events. {topic[0]}"
                q1 = {"q": "What can be inferred from this situation?", "correct": topic[1], "options": topic[2], "hint": "💡 רמז: הסיקו מסקנה (Inference) מתוך הפעולות שמתוארות."}
                unseens.append({"passage": passage, **q1})
        random.shuffle(unseens)
        return unseens[:amount]

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
        ("You", "are", ["is", "am", "be"], "a very nice teacher.")
    ]
    for i in range(50):
        base = base_templates_7_9[i % len(base_templates_7_9)]
        subj, ans, wrong, rest = base
        options = [ans] + wrong
        random.shuffle(options)
        grammar_7_9.append({"q": f"{subj} ___ {rest}", "correct": ans, "options": options, "hint": "💡 רמז דקדוקי: He, She, It מקבלים תמיד 'is'. I מקבל 'am'. We, You, They מקבלים 'are'."})

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
        grammar_10_12.append({"q": sentence, "correct": v_past, "options": options, "hint": "💡 רמז דקדוקי: שימו לב למילות הזמן (Yesterday, Last, Ago)! הן מצביעות על זמן עבר (Past Simple)."})

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
        grammar_13_15.append({"q": f"Choose the correct preposition: {sentence}", "correct": prep, "options": options, "hint": f"💡 רמז סודי: השילוב של הפועל '{verb}' עם מילת היחס הנכונה יוצר את המשמעות '{mean}'."})

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
# 2. מערכת התחברות חכמה 
# ==========================================
def load_db():
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(db_data):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)

if 'user_db' not in st.session_state: st.session_state.user_db = load_db()

query_params = st.query_params
if 'logged_in_user' not in st.session_state:
    if "user" in query_params and query_params["user"] in st.session_state.user_db:
        st.session_state.logged_in_user = query_params["user"]
    else:
        st.session_state.logged_in_user = None

if 'show_vault' not in st.session_state: st.session_state.show_vault = False

def get_player_title(xp):
    if xp < 200: return "מתחיל 🥉"
    if xp < 800: return "לומד מתקדם 🥈"
    if xp < 2000: return "אלוף האנגלית 🥇"
    return "אגדת ברולסטארס 👑"

if st.session_state.logged_in_user is None:
    st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
    st.title("👑 ממלכת האנגלית של המקצוענים!")
    st.subheader("שחקו, למדו, אספו קלפים נדירים ושדרגו את השחקן שלכם!")
    st.info("💡 **הוראות שמירה חשובות:** המערכת שלנו זוכרת הכל! שמרו את הכתובת במועדפים כדי לחזור לשחקן שלכם בדיוק איפה שעצרתם.")

    tab_login, tab_register, tab_backup = st.tabs(["👋 התחברות", "✨ משתמש חדש", "💾 שחזור ממשובש"])

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
                else:
                    st.error("שם משתמש או סיסמה שגויים. נסו שוב!")

    with tab_register:
        with st.form("form_reg"):
            new_u = st.text_input("בחר שם משתמש:")
            new_p = st.text_input("בחר סיסמה:", type="password")
            age_select = st.radio("בחר את קבוצת הגיל שלך:", ["4-6", "7-9", "10-12", "13-15"], horizontal=True)
            avatar_select = st.radio("בחר סמל שחקן (אווטאר):", AVATARS, horizontal=True)
            submit_r = st.form_submit_button("צור חשבון והתחל להרוויח כוכבים! 🌟")
            if submit_r:
                if not new_u or not new_p:
                    st.warning("נא למלא את כל הפרטים.")
                elif new_u in st.session_state.user_db:
                    st.error("שם משתמש זה כבר קיים במערכת.")
                else:
                    st.session_state.user_db[new_u] = {
                        "password": new_p, "age_level": age_select, "score": 0, "stars": 50, "xp": 0,
                        "avatar": avatar_select, "current_stage": 1, "current_q_index": 0, "streak": 0, "my_prizes": []
                    }
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
                    
    with tab_backup:
        st.write("במידה והמערכת התאפסה, ניתן לייבא קובץ שמירה כאן:")
        uploaded_file = st.file_uploader("העלה קובץ גיבוי (users_db.json)", type="json")
        if uploaded_file is not None:
            try:
                imported_db = json.load(uploaded_file)
                st.session_state.user_db = imported_db
                save_db(imported_db)
                st.success("✅ השמירה שוחזרה בהצלחה! כעת ניתן להתחבר.")
            except Exception as e:
                st.error("שגיאה בקריאת הקובץ.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. מסך המשחק הראשי (וכספת הפרסים)
# ==========================================
else:
    def sync_data():
        u = st.session_state.logged_in_user
        st.session_state.user_db[u].update({
            "age_level": st.session_state.age_level,
            "score": st.session_state.score,
            "stars": st.session_state.stars,
            "xp": st.session_state.xp,
            "current_stage": st.session_state.current_stage,
            "current_q_index": st.session_state.current_q_index,
            "streak": st.session_state.streak,
            "my_prizes": st.session_state.my_prizes,
            "last_login": datetime.now().strftime("%Y-%m-%d")
        })
        save_db(st.session_state.user_db)

    with st.sidebar:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; font-size: 50px; margin:0;'>{st.session_state.avatar}</h1>", unsafe_allow_html=True)
        st.header(f"שלום, {st.session_state.logged_in_user}!")

        # תואר המשתמש מבוסס XP
        player_title = get_player_title(st.session_state.xp)
        st.markdown(f"<p style='text-align: center; color: #FFDE00; font-weight: bold;'>{player_title}</p>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">⭐<br>{st.session_state.stars}<br><span class="stat-label">כוכבים</span></div>
            <div class="stat-item">🔥<br>{st.session_state.streak}<br><span class="stat-label">רצף</span></div>
            <div class="stat-item">⚡<br>{st.session_state.xp}<br><span class="stat-label">XP</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🆙 שלב: **{st.session_state.current_stage}** / 50")

        new_age = st.selectbox(
            "🔄 שנה רמה:",
            ["4-6", "7-9", "10-12", "13-15"],
            index=["4-6", "7-9", "10-12", "13-15"].index(st.session_state.age_level),
            key="change_user_age_level"
        )
        if new_age != st.session_state.age_level:
            st.session_state.age_level = new_age
            sync_data()
            st.toast(f"🚀 הרמה שונתה בהצלחה לגילאי {new_age}!")
            st.rerun()

        st.write("---")
        
        # חנות יומית מתחלפת המבוססת על השם של הילד והתאריך
        st.subheader("🛒 החנות היומית שלך!")
        st.caption("מתחלפת כל יום! חזור מחר למבצעים חדשים.")
        
        seed_str = f"{st.session_state.logged_in_user}_{datetime.now().strftime('%Y-%m-%d')}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        shop_random = random.Random(seed)
        daily_shop_items = shop_random.sample(ALL_SHOP_ITEMS, 4)
        
        for item in daily_shop_items:
            is_owned = item['name'] in st.session_state.my_prizes
            if not is_owned:
                currency = "⭐" if item["type"] == "stars" else "⚡"
                if st.button(f"קנה: {item['name']}\n({item['cost']} {currency})", key=f"buy_{item['name']}", use_container_width=True):
                    can_buy = False
                    if item["type"] == "stars" and st.session_state.stars >= item['cost']:
                        st.session_state.stars -= item['cost']
                        can_buy = True
                    elif item["type"] == "xp" and st.session_state.xp >= item['cost']:
                        st.session_state.xp -= item['cost']
                        can_buy = True
                        
                    if can_buy:
                        st.session_state.my_prizes.append(item['name'])
                        play_sound("loot")
                        sync_data()
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"אין מספיק {currency}!")

        st.write("---")

        if st.button("💼 כספת הפרסים והקלפים שלי!", type="primary", use_container_width=True):
            st.session_state.show_vault = True
            st.rerun()

        st.download_button(
            label="💾 הורד קובץ גיבוי של השחקן",
            data=json.dumps(st.session_state.user_db, ensure_ascii=False, indent=4),
            file_name="users_db.json",
            mime="application/json",
            use_container_width=True
        )

        if st.button("🚪 התנתק ושמור", use_container_width=True):
            sync_data()
            st.session_state.logged_in_user = None
            st.query_params.clear()
            st.session_state.show_vault = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.show_vault:
        st.markdown('<div class="rtl-container">', unsafe_allow_html=True)
        st.title("💼 אלבום הקלפים וכספת הפרסים שלי!")

        if not st.session_state.my_prizes:
            st.info("הכספת שלכם ריקה בינתיים... חזרו למשחק, הרוויחו כוכבים וקנו מתנות בחנות היומית!")
        else:
            cols = st.columns(2)
            for i, prize_name in enumerate(st.session_state.my_prizes):
                with cols[i % 2]:
                    st.markdown('<div class="store-card">', unsafe_allow_html=True)
                    st.write(f"**{prize_name}**")
                    image_url = PRIZE_IMAGES.get(prize_name, "https://upload.wikimedia.org/wikipedia/commons/d/d3/Soccerball.svg")
                    st.image(image_url, use_container_width=True) 
                    st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")
        if st.button("🔙 חזור להמשיך לשחק", type="primary"):
            st.session_state.show_vault = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
                    st.markdown(f'<div style="direction: ltr; text-align: left; background-color: #e8f6f3; padding: 20px; border-radius: 15px; font-size: 20px; margin-bottom: 20px; border-left: 5px solid #1abc9c;">📖 <b>Reading Passage:</b><br>{q_data["passage"]}</div>', unsafe_allow_html=True)
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
                                st.session_state.xp += 15
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
                    st.markdown("## 🎉 כל הכבוד אלופים! צדקתם והרווחתם **25 ⭐ ו-15 ⚡ XP!**")
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
