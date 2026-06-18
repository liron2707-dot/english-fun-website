import streamlit as st
import json
import os

# פונקציה לטעינת תוכן מהקובץ
def load_content():
    with open("content.json", "r", encoding="utf-8") as f:
        return json.load(f)

# פונקציה שמביאה את המשימה הנכונה למשתמש
def get_current_mission(user):
    content = load_content()
    age_group = "7-9" if user['age'] <= 9 else "10-12" if user['age'] <= 12 else "13-15"
    
    # שליפת המשימה לפי: גיל -> רמה -> שלב בתוך הרמה
    # שימוש ב-str() כי ה-JSON שומר מפתחות כמחרוזות
    try:
        return content[age_group][str(user['level'])][str(user['sub_level'])]
    except:
        return {"type": "error", "q": "אין משימה לשלב זה", "a": "סיום"}

# בתוך מסך המשחק (במקום ה-get_mission הישן):
mission = get_current_mission(user)

# הצגת המשימה (דוגמה למשימת אוצר מילים)
if mission['type'] == 'vocab':
    st.write(mission['q'])
    choice = st.radio("בחר תשובה:", mission['options'])
    if st.button("בדוק"):
        if choice == mission['a']:
            st.success("נכון מאוד!")
            user['sub_level'] += 1
            # כאן מוסיפים שמירה ל-DB...
        else:
            st.error("טעות, נסה שוב.")
