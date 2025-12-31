#קובץ עם פונקציות משותפות
from dotenv import load_dotenv  #הספריה שפונה לקובץ env
import os
import streamlit as st
from google import genai

all_models = ["gemini-3.0-flash",
              "gemini-2.5-flash",
              "gemini-2.0-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash-lite"]

def createClient():
    st.session_state.client = genai.Client(api_key=loadAPIKey()) #יוצרים לקוח של ג'מיני

def sendMessage(text,history=[]):
    if 'client' not in st.session_state: #אם לא יצרת חיבור
        createClient()

    for model in all_models: #עבור על כל המודלים
        client = st.session_state.client
        try: #מנסה
            chat = client.chat.create( #יוצר צ'אט
                model = model #מודל מהלולאה
            )

        except: #לא הצליח
            print(f"{model} not working...")



def loadAPIKey(): #פונקציה ששולפת את הAPI KEY
    load_dotenv()  # לטעון את הסביבה
    API_KEY = os.getenv("API_KEY")  or st.secrets["API_KEY"] # לטעון את המשתנה מהקובץ או מהגדרות האתר
    return API_KEY

def showMessage(sender,text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)  # הדמות כותבת


