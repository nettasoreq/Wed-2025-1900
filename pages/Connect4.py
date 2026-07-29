import streamlit as st

import copy #ספריה המאפשרת להעתיק את הרשימה של הלוח

#משתנים קבועים - לשמור את המידע
rows_number = 6
cols_number = 7

empty_cell = "⚪"
player_cell = "🟡"
comp_cell = "🟣"


#moves = 3
if "moves" not in st.session_state:
    st.session_state.moves = 3

with st.sidebar:
    st.text(f"שחקן: {player_cell}")
    st.text(f"מחשב: {comp_cell}")
    st.divider()

    moves = st.slider(
        label="רמת קושי",
        value= st.session_state.moves,
        min_value= 0, #רנדומלי
        max_value= 5
    )
    st.session_state.moves = moves #מעדכנים בזיכרון




big_number = 4895789
#פונקציית מינמקס - מניחה שהמטרה של המחשב - לנצח
#מטרה של השחקן - שהמחשב לא ינצח
#יחשב מה קרה אם שחקן מסוים ניסה לעשות
def minimax (board,moves_left,the_player):
    print(moves_left)
    #מה הציון של כל שחקן
    computer_score = calc_board_score(board,comp_cell) #ניקוד למחשב
    human_score = calc_board_score(board,player_cell) #ניקוד לשחקן

    if computer_score >= 10000:
        return big_number #ניצח זה ממש טוב!
    if human_score >= 10000:
        return -big_number #זה ממש לא טוב!

    #איזה עמודות  יש בהן מקום
    has_place_cols = []

    for c in range(cols_number):
        if board[0][c] == empty_cell:
            has_place_cols.append(c) #מוסיף שיש עוד מקום בעמודה

    if has_place_cols == []:
        return 0

    if moves_left == 0:
        return computer_score

    if the_player == comp_cell:
        #המחשב רוצה את הציון הכי טוב
        best_score = -big_number
        for c in has_place_cols: #תעבור על כל העמודות הפנויות
            temp_board = create_virtual_board(board,the_player,c) #מדמים מצב שהמחשב לחץ
            col_score = minimax(temp_board,moves_left - 1,player_cell)
            if best_score < col_score:
                best_score = col_score #מצאתי עמודה טובה יותר
        return best_score
    else:
        #השחקן רוצה את הציון הכי גרוע
        worst_score = big_number
        for c in has_place_cols: #תעבור על כל העמודות הפנויות
            temp_board = create_virtual_board(board,the_player,c) #מדמים מצב שהמחשב לחץ
            col_score = minimax(temp_board,moves_left - 1,comp_cell)
            if col_score < worst_score: #אם יש משהו גרוע יותר למחשב
                worst_score = col_score
        return worst_score



#מה היה קורה אם השחקן היה לוחץ על העמודה
def create_virtual_board(board,player,col):
    temp_board = copy.deepcopy(board) #יוצרים העתק של הלוח

    #מה שהשורה הפנויה הראשונה בלוח
    for r in range(rows_number - 1, -1, -1): #[5,4,3,2,1,0]
        if temp_board[r][col] == empty_cell: #אם המקום פנוי
            temp_board[r][col] = player #שים את השחקן
            break #אין מה להמשיך לחפש

    return temp_board #נחזיר את הלוח הזמני

def newBoard():
    board = []
    for row in range(rows_number): #תחזור לפי מספר השורות שיש לי
        row = [] #יוצרים שורה
        for cell in range(cols_number): #לפי מספר העמודות
            row.append(empty_cell)
        board.append(row) #מוסיפים את השורה
    ##print(board)
    st.session_state.board = board

if not "board" in st.session_state:
    newBoard()

board = st.session_state.board

if "turn" not in st.session_state: #אם לא שמור של מי התור
    st.session_state.turn = player_cell

turn = st.session_state.turn

#פונקציה שתחשב ציון עבור שחקן לרצף של 4
def calc_score(range4,good):
    #השחקן הרע שווה לאדם אם השחקן הטוב זה המחשב, אם זה לא היה המחשב - אז המחשב הוא היריב
    bad = player_cell if good == comp_cell else comp_cell

    #לפני החישוב
    score = 0
    #4 טובים
    if range4.count(good) == 4:
        score += 50000 #ציון גבוה - זה ניצחון
    #אם נוצר מצב שיש 3 ברביעי ו״חור״ - אחד ריק - ממש קרוב לניצחון
    elif range4.count(good) == 3 and range4.count(empty_cell) == 1:
        score += 100 #זה טוב - אבל לא מדהים
    elif range4.count(good) == 2 and range4.count(empty_cell) == 2:
        score += 10 #זה נחמד אבל לא וואו

    #עונש שלא חסמתי
    # אם לא חסמתי - ונשאר מצב שלשחקן יש 3 וחור
    if range4.count(bad) == 3 and range4.count(empty_cell) == 1:
        score -= 500 #החלטה ממש לא טובה - השארתי את היריב עם סיכוי לנצח
    elif range4.count(bad) == 2 and range4.count(empty_cell) == 2:
        score -= 50 #לא נורא אבל לא כדאי

    return score

#יחשב ציון לכל הלוח
def calc_board_score(board,good):
    score = 0

    #מעבר על כל השורות
    for r in range(rows_number): #עבור על כל השורות
        row = board[r] #באיזה שורה אני
        for c in range(cols_number - 3):
            range4 = row[c:c+4] #חיתוך של השורה לרביעיה
            score += calc_score(range4,good) #מוסיף את הניקוד
    #עמודות
    for c in range(cols_number): #תעבור על כל העמודות
        col = [board[r][c] for r in range(rows_number)] #כתיבה מקוצרת
        for r in range(rows_number - 3):
            range4 = col[r:r+4]
            score += calc_score(range4,good)

    #אלכסונים
    for r in range(rows_number - 3):
        for c in range(cols_number - 3):
            #יורד
            range4 = [board[r+i][c+i] for i in range(4)]
            score += calc_score(range4,good)
            #עולה
            range4 = [board[r + 3 - i][c+i] for i in range(4)]
            score += calc_score(range4,good)

    #העמודה האמצעית
    middle_number = cols_number // 2 #חלוקה בלי שארית - למצוא את האמצעי
    middle_col = [board[r][middle_number] for r in range(rows_number)] #כל העמודה האמצעית
    score+= middle_col.count(good) * 5 #על כל דיסקית שלי בעמודה האמצעית יש לי 5 נקודות - מעלה לי את הסיכוי

    right_col = [board[r][middle_number+1] for r in range(rows_number)]  # כל העמודה האמצעית
    score += right_col.count(good) * 2

    left_col = [board[r][middle_number-1] for r in range(rows_number)]  # כל העמודה האמצעית
    score += left_col.count(good) * 2

    return score
    ##print(good,":",score)
#calc_board_score(board,turn)

def switchTurn():
    global turn
    if turn == player_cell:
        turn = comp_cell
    else:
        turn = player_cell
    st.session_state.turn = turn

def check(row,col,player):
   # #print(f"Checking row {row} col {col}")
    #שורה
    for cell in range(0, cols_number - 3): #תעבור כל תא בשורה
        if board[row][cell] == empty_cell:
            continue #תמשיך לתא הבא אל תבזבז זמן על זה
        if board[row][cell] != player: #אם התא הוא לא של מי שהתור היה שלו
            continue

        number = 0 #כמה תאים רצופים יש
        for i in range(cell,cell + 4):
            if board[row][i] == board[row][cell]: #אם התא הבא - שווה לתא שאנחנו בודקים
                number+=1 #יש לי תוספת לרצף
            else:
                break #תצא - נשבר הרצף
        if number == 4: #האם יש 4 בשורה
            #print(player) #מי ניצח
            st.session_state.winner = player #שמרנו מי ניצח
            return  #יוצא מהפונקציה

    #עמודה
    for cell in range(0, rows_number - 3): #תעבור כל תא בשורה
        if board[cell][col] == empty_cell:
            continue #תמשיך לתא הבא אל תבזבז זמן על זה
        if board[cell][col] != player: #אם התא הוא לא של מי שהתור היה שלו
            continue

        number = 0 #כמה תאים רצופים יש
        for i in range(cell,cell + 4):
            if board[i][col] == board[cell][col]: #אם התא הבא - שווה לתא שאנחנו בודקים
                number+=1 #יש לי תוספת לרצף
            else:
                break #תצא - נשבר הרצף
        if number == 4: #האם יש 4 בשורה
            #print(player) #מי ניצח
            st.session_state.winner = player #שמרנו מי ניצח
            return  #יוצא מהפונקציה

    #####
    #אלכסון יורד
    offset = min(row,col) #מי יותר קטן - מספר שורה או מספר עמודה
    start_row = row - offset #הכי הרבה שאפשר ללכת
    start_col = col - offset #הכי הרבה שאפשר ללכת

    number = 0 #ספירה של הרצף
    for i in range(cols_number): #לך לפי מספר העמודות
        check_row = start_row + i #מתקדמים על האלכסון
        check_col = start_col + i  #מתקדמים על האלכסון
        if check_col == cols_number or check_row == rows_number: #אם יצאתי מהלוח
            #print("אין רצף")
            break #אין ניצחוןֿ

        ##print(f"player: {player} row: {check_row} col: {check_col}")
        if board[check_row][check_col] == player: #אני עכשיו בתא של השחקן
            number += 1 #עוד אחד לרצף
        else: #ריק או השחקן השני קטע את הרצף
            number = 0 #הרצף מתאפס
        ##print(number)
        if number == 4: #רצף של 4
            #print(player) #מי ניצח
            st.session_state.winner = player #שמרנו מי ניצח
            return  #יוצא מהפונקציה

    #אלכסון עולה
    dist_left = col #מרחק שמאלה - מספר העמודה
    dist_bottom = rows_number - 1 - row #מרחק למטה - מספר השורות (מתחיל מ0) פחות השורה שבה אני נמצאת
    offset = min(dist_left,dist_bottom)
    #חישוב נקודת ההתחלה של האלכסון
    start_row = row + offset  #שורה - יורדים - פלוס
    start_col = col - offset #עמודה - שמאל - מינוס

    number = 0 #מתחילים לבדוק כמה ברצף
    for i in range(cols_number):
        check_row = start_row - i #למעלה - מינוס
        check_col = start_col + i #ימינה - פלוס

        if check_row < 0 or check_col >= cols_number: #אם יצאתי
            break #אין פה ניצחון

        if board[check_row][check_col] == player: #אם מצאתי תא של שחקן
            number += 1 #מוסיפים 1 לרצף
        else:
            number = 0 #מאפסים את הרצף

        if number == 4: #אם יש 4 ברצף
            #print(player) #מי ניצח
            st.session_state.winner = player #שמרנו מי ניצח
            return  #יוצא מהפונקציה









def click(col):
    if board[0][col] != empty_cell: #אם התא העליון בשורה לא ריק
        st.rerun() #אין פה תור
    ##print (col)
    for row in range(rows_number - 1, -1, -1):
        if board[row][col] == empty_cell: #אם התא פנוי
            board[row][col] = turn #שם בו את העיגול
            check(row,col,turn) #בודקים האם מישהו ניצח
            break
    #board[rows_number - 1][col] = player_cell #שמים סימן
    switchTurn() #להחליף תור
    st.session_state.board = board #שמירה בזיכרון של הלוח המעודכן
    st.rerun() #רענון התצוגה

def computer_play():
    import random,time
    #time.sleep(1)
    #coll = random.randint(0,cols_number - 1)
    best_score = -39484093850493859043 - big_number #מתחילים שהציון הכי טוב ממש נמוך
    best_col = -1 #העמודה הכי טובה היא -1
    all_scores = [] #כל הניקודים

    if moves == 0: #רנדומלי
        col =  random.randint(0,cols_number - 1)
        click(col)
        return

    for c in range(cols_number):
        if board[0][c] != empty_cell: #אם העמודה מלאה
            all_scores.append("-")
            continue #תמשיך הלאה אין מה לעשות עם העמודה הזאת היא לא אפשרית

        temp_board = create_virtual_board(board,comp_cell,c)
        #score = calc_board_score(temp_board,comp_cell)
        score = minimax(temp_board,moves - 1 , player_cell) #תחשב מהמלך של השחקן
        all_scores.append(score)
        #אם הניקוד של העמודה יותר גבוה מהעמודה הקודמת שנבדקה - עכשיו היא הכי טובה
        if best_score < score:
            best_score = score
            best_col = c
    st.session_state.all_scores = all_scores #שומרים בזיכרון של סטרימליט
    click(best_col) #המחשב לוחץ על העמודה הכי טובה
    #click(coll) #כאילו המחשב לחץ על העמודה

if "winner" not in st.session_state: #אם לא שמור מנצח
    st.session_state.winner = "" #אין מנצח


winner = st.session_state.winner #שליפה מה שהיה שמור
#בדיקה האם תיקו
has_empty = False #כרגע אין ריק
for col in range(cols_number): #עבור כל עמודה לפי מספר העמודות
    if board[0][col] == empty_cell:
        has_empty = True #יש עוד עמודות ריקות
        break

if winner == comp_cell:
    st.info("המחשב ניצח")
elif winner == player_cell:
    st.info("ניצחת!!!")
elif not has_empty: #אם אין תא ריק
    st.info("תיקו")
else: #אם לא השחקן ולא המחשב ניצח
    if turn == player_cell:
        st.info("התור שלך")
    else:
        st.status("המחשב חושב...")

#ליצור את הלוח על המסך
for row in range (rows_number): #עבור כל שורה
    all_column = st.columns(cols_number) #לכל שורה - צור תאים
    #שמים בתאים
    for col in range(cols_number): #תעבור על כל תא לפי מספר התאים
        with all_column[col]: #כניסה לעמודה
            cell = board[row][col] #שולפים מהזיכרון מה אמור להיות בתא
            if st.button(cell,
                         key=f"row_{row}_col_{col}",
                         use_container_width=True,
                         disabled = turn==comp_cell or winner!=""): #שמים בכפתור
                click(col)

if turn == comp_cell and winner=="" and has_empty: #אם התור של המחשב וגם לא ניצחו
    computer_play() #תפעיל את התור של המחשב

if "all_scores" not in st.session_state:
    st.session_state.all_scores = [0] * cols_number
all_scores = st.session_state.all_scores

scores_cols = st.columns(cols_number) #שורה עם עמודות
for c in range(cols_number): #עבור כל עמודה
    with scores_cols[c]:
        col_score = all_scores[c]
        #print(col_score)
        if col_score == 0 or col_score == "-":
            st.badge(str(col_score),color = "gray")
        elif col_score < 0:
            st.badge(str(col_score),color = "red")
        else:
            st.badge(str(col_score),color = "green")

