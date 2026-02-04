#קובץ עם פונקציות משותפות
from dotenv import load_dotenv  #הספריה שפונה לקובץ env
import os
import streamlit as st
from google import genai
from google.genai import types
import time

from ddgs import DDGS

#פונקציה לחיפוש באינטרנט
#תקבל מה מחפשים - תחזיר תוצאות - מקבל טקסט ומחזיר טקסט
def web_search(query : str) -> []:
    """
    פונקציה שמחפשת באינטרנט
    :param query: מה לחפש
    :return: תוצאות מהאינטרנט
    """
    print("search: "+ query)

    with DDGS() as d:
        results = d.text( query, max_results=3)
        return results


def current_time() -> str:  #הולך לחזור משתנה מסוג טקסט
    """
    פונקציה שמחזירה מה התאריך והשעה
    """
    print("use tool")
    return time.ctime() #מחזיר את הזמן עכשיו

all_models = [
              "gemini-2.5-flash",
              "gemini-2.5-flash-lite",
              "gemini-2.0-flash",
              "gemini-2.0-flash-lite",
             #  "gemini-3-flash",
               ]

def createClient():
    st.session_state.client = genai.Client(api_key=loadAPIKey()) #יוצרים לקוח של ג'מיני

def sendMessage(text,system_prompt,history=[]):
    if 'client' not in st.session_state: #אם לא יצרת חיבור
        createClient()

    for model in all_models: #עבור על כל המודלים
        client = st.session_state.client
        try: #מנסה
            chat = client.chats.create( #יוצר צ'אט
                model = model,
                history = history, #ההיסטוריה ששלחנו
                config = types.GenerateContentConfig (
                    system_instruction = system_prompt,  #ההוראות זה הסיסטם פרומפט
                    tools = [current_time,web_search],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
                )
            )

            ai = chat.send_message(text)  #שליחת הודעה
            print(ai)
            print(ai.text)  #הדפסת תשובה
            return ai.text #תחזיר את התשובה
        except Exception as e: #לא הצליח
            error = str(e) #שומרים את השגיאה
            print(e)
            if "429" in error: #אם הסיבה היא ששלחתי יותר מדי הודעות
                st.error("שלחת יותר מדי הודעות, בבקשה לנסות מחר")
                return #צא
            if "503" in error: #המודל עמוס
                st.info(f"המודל עמוס, ננסה מודל אחר")
            else:
                st.info("Error: " + error)
                return
            print(f"{model} not working...")



def loadAPIKey(): #פונקציה ששולפת את הAPI KEY
    load_dotenv()  # לטעון את הסביבה
    API_KEY = os.getenv("API_KEY")  or st.secrets["API_KEY"] # לטעון את המשתנה מהקובץ או מהגדרות האתר
    return API_KEY

def showMessage(sender,text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)  # הדמות כותבת

def save_to_history(project,sender,text): #לאיזה פרויקט, מי שלח, מה הוא שלח
    if project not in st.session_state: #אם לא יצרת את הפרויקט בזיכרון
        st.session_state[project] = { #צור פרויקט עם היסטוריה ריקה
            "history": []
        }
    st.session_state[project]["history"].append(
        {
            "role" : sender,  #מי שלח
            "parts": [{"text":text }] #הצורה שג'מיני מצפה לקבל בה את ההיטוריה
        }
    )

def newPage(project): #פתיחת פרויקט חדש - פועל בפעם הראשונה שנכנסים לדף
    st.session_state[project] = {  # צור פרויקט עם היסטוריה ריקה
        "history": []
    }

