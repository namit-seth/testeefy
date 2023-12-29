# imports
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from helpers import apology, login_required
import re
from copy import deepcopy

# declaration of varables
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

db_con = sqlite3.connect("Project.db",check_same_thread=False)
db_con.row_factory = sqlite3.Row
db = db_con.cursor()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


SUBJECT_DICT = {
  "Geography": "#1E8449",
  "History": "#D35400",
  "Science": "#3498DB",
  "Music": "#8E44AD",
  "Sports": "#C0392B",
  "Movies": "#E67E22",
  "Literature": "#F39C12",
  "Food and Cuisine": "#27AE60",
  "Art and Artists": "#9B59B6",
  "General Knowledge": "#34495E",
  "Mathematics": "#2980B9",
  "Technology": "#2C3E50",
  "Biology": "#16A085",
  "Space and Astronomy": "#2E86C1",
  "Mythology": "#E74C3C",
  "World Languages": "#575A5A",
  "Politics": "#AF7AC5",
  "Fashion": "#F1C40F",
  "Environmental Science": "#229954",
  "Psychology": "#3498DB"
}

# index
'''
deliver the home page
'''
@app.route("/")
def index():
    return render_template("index.html")

# logout
'''
logout user
'''
@app.route("/logout/")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# register
"""
register new user
"""
@app.route("/register/", methods=["GET", "POST"])
def register():
    typee = ""
    if request.args:
        return render_template("registering.html", typ=request.args["type"])
    if request.method != "POST":
        return render_template("register.html")

    if not request.form.get("email_id"):
        return apology("must provide email")
    if not re.fullmatch(regex, request.form.get("email_id")):
        return apology("invalid email")
    if not request.form.get("password"):
        return apology("must provide password")
    if not request.form.get("confirmation"):
        return apology("must provide confirmation")
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords must match")
    emails = db.execute(
        "select email from user"
    )
    if request.form.get("email_id") in emails:
        return apology("email already registered")
    db.execute(
        "insert into user (email, pass, type) values (? ,? ,?)",
            [request.form.get("email_id"),
            generate_password_hash(request.form.get("password")),
            request.form.get("type")]
    )
    db_con.commit()
    flash("registeration successfull")
    return redirect("/login")

# login
"""
login registered users
"""
@app.route("/login/", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("email"):
            return apology("must provide email")
        elif not request.form.get("password"):
            return apology("must provide password")
        rows = db.execute(
            "SELECT * FROM user WHERE email = ?", (request.form.get("email"),)
        ).fetchall()
        db_con.commit()
        if len(rows) != 1 or not check_password_hash(
            rows[0][2], request.form.get("password")
        ):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0][0]
        session["type"] = rows[0][3]
        flash("logged in")
        return redirect("/")
    else:
        return render_template("login.html")

# tests
"""
deliver the page showing all the tests
"""
@app.route("/tests/")
@login_required
def tests():
    rows = []
    if session["type"] == "EXAMINER":
        rows = db.execute(
            "SELECT * from test where Examiner_id = ?",(session["user_id"],)
            ).fetchall()
    return render_template("tests.html",tests=rows,len=len(rows),sub_dict=SUBJECT_DICT)

# test create
"""
creating new test by examiner
"""
@app.route("/test/create/", methods=["GET", "POST"])
@login_required
def test_create():
    if session["type"] != "EXAMINER":
        return apology("unautherized")
    if request.method == "POST":
        if request.form.get("topic"):
            topic = request.form.get("topic")
            topic = topic.title()
        if request.form.get("subject"):
            subject = request.form.get("subject")
        max_marks = 0
        min_marks = 0
        question_num = 1
        questions = []
        while True:
            if request.form.get(f"question-{question_num}"):
                question_text = request.form.get(f"question-{question_num}")
                correct = int(request.form.get(f"question-{question_num}/marks-correct"))
                if correct > 0:
                    max_marks += correct
                elif correct < 0:
                    correct = correct*(-1)
                    max_marks += correct
                incorrect = int(request.form.get(f"question-{question_num}/marks-incorrect"))
                if incorrect < 0:
                    min_marks += incorrect
                elif incorrect > 0:
                    incorrect = incorrect*-1
                    min_marks += incorrect
                options = []
                option_number = 1
                while True:
                    if request.form.get(f"question-{question_num}/option-{option_number}"):
                        option_text = request.form.get(f"question-{question_num}/option-{option_number}")
                        option_correct = False
                        if request.form.get(f"question-{question_num}/option-{option_number}-correct"):
                            option_correct = True
                        option = {"option":option_text,"correct":option_correct}
                        options.append(option)
                        option_number += 1
                    else:
                        break
                question={"question":question_text,"correct":correct,"incorrect":incorrect,"options":options}
                questions.append(question)
                question_num += 1
            else:
                break
        data = [topic,subject,session["user_id"],max_marks,min_marks,question_num-1]
        db.execute("insert into test (Topic , Subject , Examiner_id , Max_marks , Min_marks , Num_of_question ) values (? , ? ,? , ? ,? , ? )",data)
        db_con.commit()
        test_id = db.execute("select max(id) from test").fetchall()[0][0]
        for question in questions:
            data = [test_id,question["question"],question["correct"],question["incorrect"]]
            db.execute("insert into Questions (Test_id , Ques_Text , Correct , Incorrect ) values (? , ? , ? , ?)",data)
            db_con.commit()
            Que_id = db.execute("select max(Question_id) from Questions").fetchall()[0][0]
            for option in question["options"]:
                data = [Que_id,option["option"],option["correct"]]
                db.execute("insert into Options (Question_id , Option_Text , Correct ) values (? , ? , ? )",data)
                db_con.commit()
        return redirect("/tests")
    return render_template("create.html")

# test subject
"""
a seprate page for all subjects
"""
@app.route("/tests/<subject>")
@login_required
def subject(subject):
    if subject not in SUBJECT_DICT:
        return apology("not found",404)
    tests = db.execute(
        "select * from test where subject = ? ;"
        ,[subject,]
    ).fetchall()
    return render_template("subject.html",tests=tests,sub_dict=SUBJECT_DICT)

# test
"""
page to attempt each test
"""
@app.route("/test")
@login_required
def test():
    if session["type"] == "EXAMINER":
        return apology("unautherized")
    id=request.args.get("id")
    if id == None:
        return apology("Enter test id")
    test = db.execute(
        "select * from test where id = ? ;"
        ,[id,]
    ).fetchall()
    questions = db.execute(
        "select * from Questions where Test_id = ? ;"
        ,[id,]
    ).fetchall()
    options = {}
    for i in questions :
        opt = db.execute(
        "select * from Options where Question_id = ? ;"
        ,[i[1],]
        ).fetchall()
        options[i[1]]=opt

    return render_template("test.html",test=test,Questions=questions ,options=options)

def calc_result(attempt,test_id):
    total_mark = 0
    no_correct = 0
    no_incorrect = 0
    for i in attempt:
        corr = db.execute("select Correct from Options where Option_id = ? ;",[attempt[i],]).fetchall()
        if corr[0][0]:
            marks = db.execute("select Correct from Questions where Question_id = ? ;",[i,]).fetchall()
            total_mark += marks[0][0]
            no_correct += 1
        else:
            marks = db.execute("select Incorrect from Questions where Question_id = ? ;",[i,]).fetchall()
            total_mark += marks[0][0]
            no_incorrect += 1
    data = [session["user_id"],test_id,no_correct,no_incorrect,total_mark]
    db.execute("insert into Result (User_Id , Test_id , No_Correct , No_Incorrect , Total ) values ( ? , ? , ? , ? , ? )",data)
    db_con.commit()
    result_id = db.execute("select max(Id) from Result").fetchall()[0][0]
    return result_id

@app.route("/test/submit",methods=["POST"])
@login_required
def submit():
    test_id = request.form.get("test_id")
    attempt = {}
    for i in request.form:
        if i == "test_id":
            continue
        ques_id = i
        option_id = request.form.get(i)
        attempt[ques_id] = option_id
    result_id = calc_result(attempt,test_id)
    for i in attempt:
        data = [session["user_id"],test_id,i,attempt[i],result_id]
        db.execute("insert into Attempts (User_Id , Test_id , Que_Id , Option_Id , Result_id ) values ( ? , ? , ? , ? , ? )",data)
        db_con.commit()
    db.execute('UPDATE test SET Num_of_attempts = Num_of_attempts + 1  WHERE ID = ? ;' , [test_id])
    db_con.commit()
    flash("submitted")
    return redirect("/init")

@app.route("/result")
@login_required
def result():
    id=request.args.get("Test_id")
    if id == None:
        tests = db.execute(
            "select * from test where ID in (select DISTINCT test_id from Result Where User_Id = ?)"
            ,[session["user_id"],]
        ).fetchall()
        return render_template("result.html",tests = tests , sub_dict=SUBJECT_DICT)
    tests = db.execute(
            "select * from Result Where User_Id = ? and Test_id = ?"
            ,[session["user_id"],id]
        ).fetchall()
    return render_template("result_id.html",tests = tests , sub_dict=SUBJECT_DICT)

@app.route("/attempt")
@login_required
def attempt():
    Result_id=request.args.get("result_id")
    if Result_id == None:
        return apology()
    id = db.execute("select Test_id from Result where Id = ?",[Result_id,] ).fetchall()[0][0]
    test = db.execute(
        "select * from test where id = ? ;"
        ,[id,]
    ).fetchall()
    questions = db.execute(
        "select * from Questions where Test_id = ? ;"
        ,[id,]
    ).fetchall()
    options = {}
    for i in questions :
        opt = db.execute(
        "select * from Options where Question_id = ? ;"
        ,[i[1],]
        ).fetchall()
        options[i[1]]=opt
    attempts = db.execute("select option_id from attempts where Result_id = ?",[Result_id]).fetchall()
    return render_template("attempt.html",test=test,Questions=questions ,options=options , attempts = attempts)

@app.route("/init")
@login_required
def init():
    tets = db.execute("Select ID from test").fetchall()
    for i in tets:
        db.execute("UPDATE Result SET time = datetime('now')" )
        db_con.commit()
    return redirect("/tests/")
