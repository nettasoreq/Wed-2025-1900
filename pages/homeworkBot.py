import streamlit as st
from helper import * #תביא את כל הפונקציות מהקובץ המשותף

import PIL.Image #ספריה שאחראית על תמונות


st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon="🤓"
)

st.title("בוט שיעורי בית")

api_key = loadAPIKey() #מביא את הפונקציה מהקובץ

#הודעה ראשונה מהצ'אט
showMessage("AI","היי אני כאן כדאי לעזור לך")

#אם לא הגדרנו את הפרויקט - צור אותו בזיכרון
if "homework" not in st.session_state:
    newPage("homework")

#פרומפט מיוחד שמגדיר לAI איך לעבוד
system_prompt = """
    #תפקיד
    אתה בוט שיעורי בית
    
    #משימה
    המשימה שלך - לעזור לי בשיעורי בית
    תסביר ברור
    תכוון אותי לתשובה הנכונה
    
    #מגבלות
    אם אתה לא יודע - תחפש בגוגל
   **אל תמציא תשובה**
    ענה כמו בן אדם - בצורה אנושית
    
    ** אם השתמשת בכלי (Tool) תכתוב את התוצאה **
    **אנחנו בשנת 2026**
"""


#לשמור בזיכרון
st.session_state["homework"]["system_prompt"] = system_prompt

history = st.session_state["homework"]["history"]
for line in history:
    sender = line["role"]
    if sender == "model": #ג'מיני מצפה לקבל model
        sender = "ai" #streamlit מצפה לקבל AI

    text = line["parts"][0]["text"] #פשוט מוציאים את הטקסט מהמבנה של ג'מיני
    showMessage(sender,text)


#מקום להקליד
user = st.chat_input("ההודעה שלך...")

#כפתור  העלאה
image_button = st.file_uploader("העלאת תמונה", type=["png","jpg","jpeg"])


if user: #אם יש הודעה

    showMessage("user",user)

    image = None
    #שולפים את ההיסטוריה
    if image_button: #אם יש תמונה בכפתור ההעלאה
        image = PIL.Image.open(image_button) #תטען את מה שבתמונה

    save_to_history("homework","user",user)
    history = st.session_state["homework"]["history"]
    answer = sendMessage(user,system_prompt,history, image) #לשלוח לAI את ההודעה

    showMessage("ai",answer) #תראה את התשובה

    save_to_history("homework","model",answer)


