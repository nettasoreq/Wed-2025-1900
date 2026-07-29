import streamlit as st

from helper import *  # תביא את כל הפונקציות מהקובץ המשותף

import PIL.Image  # ספריה שאחראית על תמונות

st.set_page_config(
    page_title="סוכן קוד חכם",
    page_icon="🤓"
)

st.title("סוכן קוד חכם")

api_key = loadAPIKey()  # מביא את הפונקציה מהקובץ

# הודעה ראשונה מהצ'אט
showMessage("AI", "היי מה נכין היום?")

# אם לא הגדרנו את הפרויקט - צור אותו בזיכרון
if "codeAgent" not in st.session_state:
    newPage("codeAgent")


# פרומפט מיוחד שמגדיר לAI איך לעבוד
system_prompt = """
    ##תפקיד
    אתה מתכנת מומחה, אתה ממש טוב בליצור פרויקטים משלב הרעיון ועד לפיתוח
    
    ##איך אתה עושה את זה
    1. המשתמש אומר מה הוא רוצה ליצור, אם אין לו רעיון אתה מציע
    2. אתה שואל שאלות להבהרה כדי לוודא שאתה מבין מה המשתמש רוצה
    3. אתה יוצר תוכנית עבודה
    4. אתה מפתח כל פעם חלק אחר
    5. אתה בודק את הקוד שלך
    
    ##חוקים
    אל תמציא, אל תניח הנחות - אם אתה לא יודע תשאל
    דבר בעברית בשפה נעימה, תהיה יצירתי
    אל תמשיך לשלב הבא לפני שאתה בטוח שסיימת או שהמשתמש אמר להמשיך
    בכל פעם - שלב אחד בלבד
    
    ##יכולות 
    אם אתה צריך הבהרות השתמש בכלי ask_questions - שלח לו בכל פעם שאלה אחת ובין 2 ל4 אפשרויות
    המשתמש יחזיר לך תשובה.
    כתוב למשתמש הודעה בסגנון: ״כמה שאלות כדי להתחיל:
    תשאל שאלות רק דרך הכלי ask_questions
    ברגע ששאלת שאלה - המתן עד שתקבל תשובה.
    
    ---
    כל שלב - מקסימום 3 שאלות. תסיים כשאתה בטוח או כשהמשתמש אומר להמשיך
    בכל תור - שאל רק שאלה אחת! אל תפעיל ברציפות ללא תשובה מהמשתמש
    השתמש בכלי mark_step_done בסיום שלב כדי לסמן שהוא הושלם
    
"""

if "steps" not in st.session_state["codeAgent"]:
    st.session_state["codeAgent"]["steps"] = {
        "idea": "",
        "clarification" : "",
        "plan" : "",
        "code": [],
        "test":""
    }
    st.session_state["codeAgent"]["current_step"] = "idea"

# לשמור בזיכרון
system_prompt+= "\n" +"השלב הנוכחי: " + st.session_state["codeAgent"]["current_step"]

import json
steps_str = json.dumps(st.session_state["codeAgent"]["steps"], ensure_ascii=False, indent=2)
system_prompt += "\n" + "השלבים הם: " + steps_str
#system_prompt+= "\n" +"השלבים הם: " + str(st.session_state["codeAgent"]["steps"])


st.session_state["codeAgent"]["system_prompt"] = system_prompt

history = st.session_state["codeAgent"]["history"]
for line in history:
    sender = line["role"]
    if sender == "model":  # ג'מיני מצפה לקבל model
        sender = "ai"  # streamlit מצפה לקבל AI

    text = line["parts"][0]["text"]  # פשוט מוציאים את הטקסט מהמבנה של ג'מיני
    showMessage(sender, text)


if not "status" in st.session_state["codeAgent"]:
    st.session_state["codeAgent"]["status"] = "chat"

if st.session_state["codeAgent"]["status"] == "wait":
    question = st.session_state["codeAgent"]["question"]
    showMessage("Ai", f"**{question}**")
    options = st.session_state["codeAgent"]["options"]
    cols = st.columns(len(options))


    for i in range(len(options)):
        with cols[i]:
            if st.button(options[i],key=f"o_{i}"):
                save_to_history("codeAgent", "model", question)
                save_to_history("codeAgent", "user", options[i])

                st.session_state["codeAgent"]["status"] = "chat"

                history = st.session_state["codeAgent"]["history"]
                with st.status("חושב"):
                    answer = sendMessage(options[i], system_prompt, history, None, [ask_questions,mark_step_done])  # לשלוח לAI את ההודעה

                if st.session_state["codeAgent"]["status"] == "chat":
                    save_to_history("codeAgent", "model", answer)
                #st.session_state["codeAgent"]["status"] = "chat"
                st.rerun()



# מקום להקליד
user = st.chat_input("ההודעה שלך...")

# כפתור  העלאה
#image_button = st.file_uploader("העלאת תמונה", type=["png", "jpg", "jpeg"])

if user:  # אם יש הודעה

    showMessage("user", user)

    image = None
    # שולפים את ההיסטוריה
 #   if image_button:  # אם יש תמונה בכפתור ההעלאה
  #      image = PIL.Image.open(image_button)  # תטען את מה שבתמונה

    save_to_history("codeAgent", "user", user)
    history = st.session_state["codeAgent"]["history"]

    with st.status("חושב"):
        answer = sendMessage(user, system_prompt, history, image,[ask_questions,mark_step_done])  # לשלוח לAI את ההודעה

    showMessage("ai", answer)  # תראה את התשובה

    if st.session_state["codeAgent"]["status"] == "chat":
        save_to_history("codeAgent", "model", answer)

    st.rerun()


