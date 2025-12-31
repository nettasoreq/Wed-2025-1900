import streamlit as st
from helper import * #תביא את כל הפונקציות מהקובץ המשותף

st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon="🤓"
)

st.title("בוט שיעורי בית")

api_key = loadAPIKey() #מביא את הפונקציה מהקובץ

#הודעה ראשונה מהצ'אט
showMessage("AI","היי אני כאן כדאי לעזור לך")

#מקום להקליד
user = st.chat_input("ההודעה שלך...")

if user: #אם יש הודעה
    showMessage("user",user)


