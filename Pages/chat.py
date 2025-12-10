import os #Operating System = מערכת הפעלה = התוכנה ששולטת במחשב - Window / macOS
from dotenv import load_dotenv  #הספריה שפונה לקובץ env
from google import genai # Generative Ai = בינה מלאכותית יוצרת
import streamlit as st  #הספרייה של הGUI - הנראות

st.title("הצ'אט שלי") #כותרת

#הגדרות
st.set_page_config(
    page_title="שיחה עם טראמפ",
    page_icon='👱🏻'
)

load_dotenv()  #לטעון את הסביבה

API_KEY = os.getenv("API_KEY") #לטעון את המשתנה

#gemini = genai.Client(api_key=API_KEY) #יוצרים לקוח לAPI - שולחים לו את המזהה שלנו

def saveToHistory(sender,text):
    st.session_state.history.append({ #מילון
        "sender" : sender,
        "text" : text
    })

def send(prompt):

    saveToHistory("user",prompt) #שומרים בהיסטוריה

    all_models = ["gemini-2.5-flash","gemini-2.0-flash","gemini-2.5-flash-lite","gemini-2.0-flash-lite"]

    context = ""
    for line in st.session_state.history:
        context += f"{line['sender']}: {line['text']} \n"

    for model in all_models:
        chat = st.session_state.gemini.chats.create(model=model)
        try: #תנסה לשלוח הודעה
            message = chat.send_message(context)

            saveToHistory("assistant", message.text)  # שומרים בהיסטוריה

            return message
        except: #לא הצליח
            print(f"מודל {model} לא עבד - מנסה את המודל הבא ")

#chat = gemini.chats.create(model="gemini-2.5-flash")


#פקודה - הנחייה לAI
prompt = """
        אתה עונה תמיד כמו טראמפ
        אנחנו נתחיל שיחה קצרה
    """
#message = chat.send_message(prompt)

#session

def start(): #פונקציה שתפעל כשמתחילים את הפרויקט
    st.session_state.gemini = genai.Client(api_key=API_KEY) #תשמור את החיבור לג'מיני בסשיין -
    st.session_state.history = [] #רשימה של כל ההודעות

    #מתחיל
    message = send(prompt)
    #print(message.text)

    #ai_msg = st.chat_message("assistant")
    #ai_msg.write(message.text) #הדמות כותבת

if "gemini" not in st.session_state: # אם אתה לא יודע מי זה ג'מיני
     start() #תתחיל

if "history" in st.session_state: #אם שמורה לך היסטוריה
    for line in st.session_state.history[1:]: #תעבור הודעה הודעה - חיתוך - תתחיל מההודעה השניה
        chat = st.chat_message(line["sender"]) #מי כתב את ההודעה
        chat.write(line["text"]) #מה הוא כתב

prompt = st.chat_input("Say something")
if prompt:
    user_msg = st.chat_message("user")
    user_msg.write(prompt)  # הדמות כותבת

    #שליחה לג'מיני
    message = send(prompt)
    ai_msg = st.chat_message("assistant")
    ai_msg.write(message.text)

#st.text(message.text)