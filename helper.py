#קובץ עם פונקציות משותפות
from dotenv import load_dotenv  #הספריה שפונה לקובץ env
import os
import streamlit as st
from google import genai

all_models = ["gemini-3-flash",
              "gemini-2.5-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash",
              "gemini-2.0-flash-lite",
               ]

def createClient():
    st.session_state.client = genai.Client(api_key=loadAPIKey()) #יוצרים לקוח של ג'מיני

def sendMessage(text,history=[]):
    if 'client' not in st.session_state: #אם לא יצרת חיבור
        createClient()

    for model in all_models: #עבור על כל המודלים
        client = st.session_state.client
        try: #מנסה
            chat = client.chats.create( #יוצר צ'אט
                model = model #מודל מהלולאה
            )

            ai = chat.send_message(text)  #שליחת הודעה
            print(ai.text)  #הדפסת תשובה
            return ai.text #תחזיר את התשובה
        except Exception as e: #לא הצליח
            error = str(e) #שומרים את השמירה
            print(e)
            if "429" in error: #אם הסיבה היא ששלחתי יותר מדי הודעות
                st.error("שלחת יותר מדי הודעות, בבקשה לנסות מחר")
                return #צא
            if "503" in error: #המודל עמוס
                st.info(f"המודל עמוס, ננסה מודל אחר")
            print(f"{model} not working...")



def loadAPIKey(): #פונקציה ששולפת את הAPI KEY
    load_dotenv()  # לטעון את הסביבה
    API_KEY = os.getenv("API_KEY")  or st.secrets["API_KEY"] # לטעון את המשתנה מהקובץ או מהגדרות האתר
    return API_KEY

def showMessage(sender,text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)  # הדמות כותבת


