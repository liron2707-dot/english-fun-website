import json

def generate_full_db():
    db = {"7-9": {}, "10-12": {}, "13-15": {}}
    
    # משימות לדוגמה (אפשר לשנות כאן כדי להוסיף גיוון)
    tasks = ["vocab", "spelling", "grammar", "reading", "video", "true_false", "game", "boss"]
    
    for age_group in db.keys():
        for level in range(1, 100): # 99 שלבים
            db[age_group][str(level)] = {}
            for sub_level in range(8): # 8 משימות
                db[age_group][str(level)][str(sub_level)] = {
                    "type": tasks[sub_level],
                    "q": f"שאלה {tasks[sub_level]} לשלב {level} (קבוצה {age_group})",
                    "options": ["אפשרות 1", "אפשרות 2", "אפשרות 3"],
                    "a": "אפשרות 1"
                }
    
    with open("content.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)
    print("content.json נוצר בהצלחה!")

generate_full_db()
