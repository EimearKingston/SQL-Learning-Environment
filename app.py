from flask import Flask, render_template, request, jsonify, session, g, redirect, url_for 
import sqlite3 
import os
from werkzeug.utils import secure_filename
from sqlite3 import Error as SqliteError
from database import get_db, close_db
from forms import QueryForm, SignForm, LoginForm, UploadForm 
from larktrial import larkfunc, extract_sql_queries
from flask_session import Session 
from trial import * 
from kroc import extract, similarity_score
from functools import wraps 
from wtforms import StringField, SubmitField 
# from trial import check_cols
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)
app.teardown_appcontext(close_db) 
app.config["SECRET_KEY"]="this-is-my-secret-key"
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app) 
# workbooks = {
#     "movies": {
#         "title": "Movies",
#         "questions_file": "question_uploads/questions5.txt",
#         "solutions_file": "solutions5.sql",
#     }
# } 
# for wb_key, wb_data in workbooks.items():
#     with open(wb_data["questions_file"], "r") as file:
#         lines = file.readlines()
#     wb_data["db_name"] = lines[0].strip()
#     wb_data["questions"] = lines[1:]
#     wb_data["solutions"] = extract_sql_queries(wb_data["solutions_file"]) 
# for i in enumerate(wb_data["solutions"]): 
#      print("\n", i) 
def read(file): 
    import re

    with open(file, 'r') as f:
        content = f.read()

    
    lines = content.splitlines() 
    preamble = "" 
    preamble_bool = True

    questions = []
    current_question = ""

    for line in lines:
        line = line.strip() 

        if re.match(r'^1\.', line): 
            preamble_bool = False 
        if preamble_bool == False:
            if re.match(r'^\d+\.', line):  
                    
                    if current_question:
                        questions.append(current_question.strip())
                    
                    
                    current_question = re.sub(r'^\d+\.\s*', '', line)
            else:
                    
                    if current_question:
                        current_question += " " + line 
            
        else:
            preamble+=line+"" 
    if current_question:
        questions.append(current_question.strip()) 
    if preamble == "": 
        return questions, None

    return questions, preamble 


def load_workbooks():
    global workbooks
    db = get_db("app.db")
    workbooks = {}
    rows = db.execute("SELECT title, questions_file, solutions_file, db_file FROM workbooks").fetchall()
    for row in rows:
        title = row["title"]
        questions_file = row["questions_file"]
        solutions_file = row["solutions_file"]
        db_file = row["db_file"] 
        # preamble = row["preamble"]

        
        lines = read(questions_file)

        workbooks[title.lower()] = {
            "title": title,
            "questions_file": questions_file,
            "solutions_file": solutions_file,
            "db_file": db_file, 
            "preamble": lines[1],
            "questions": lines[0],  
            "solutions": extract(solutions_file),
        }


# load_workbooks() 

def get_workbook(workbook_id):
    """Fetch workbook details from the database."""
    user_db = get_db("app.db")  
    workbook = user_db.execute(
        '''SELECT title, questions_file, solutions_file, db_file FROM workbooks WHERE id = ?''', 
        (workbook_id,)
    ).fetchone()
    
    if not workbook:
        return None  
    
    
    questions = read(workbook["questions_file"]) 
    print(workbook["questions_file"]) 
    print(questions)
    
    solutions = extract(workbook["solutions_file"]) 
    
    
    return {
        "title": workbook["title"],
        "questions": questions[0],
        "solutions": solutions, 
        "db_file": workbook['db_file'],
        "preamble": questions[1] 
    } 

 

ALLOWED_EXTENSIONS = {'txt', 'sql', 'sqlite'}


UPLOAD_FOLDER = 'question_uploads' 
SOLUTION_FOLDER = 'solution_uploads' 
DB_FOLDER = 'db_uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['SOLUTION_FOLDER'] = SOLUTION_FOLDER 
app.config['DB_FOLDER'] = DB_FOLDER
@app.before_request
def load_logged_in_user():
    g.user=session.get("username", None) 
    g.user_type = session.get("user_type", None) 
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: 
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view 

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        password_again=form.password_again.data 
        db=get_db("app.db")
        username_clash=db.execute('''SELECT * FROM users
                                            WHERE username=?;''', (username,)).fetchone()
        if username_clash is not None: 
            form.username.errors.append("User is already taken")
        else:
            db.execute('''INSERT INTO users(username, password)
                      VALUES(?,?)''', (username, generate_password_hash(password))) #no .fetchall() and no variable because you are inserting into the database
            db.commit()
            return redirect(url_for('login'))
            # session.clear()
            # session["username"]=username
            # next_page=request.args.get("county")
            # if not next_page:
            #     next_page=url_for("county")
            # return redirect(next_page)
            #return redirect(url_for("county"))
            #form.username.errors.append("Username is already taken")
    return render_template("/sign_up.html", form=form, subtitle="Sign-up") 
@app.route("/teacher_sign_up", methods=["GET", "POST"])
def teacher_sign_up(): 
    
    form = SignForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        password_again=form.password_again.data 
        db=get_db("app.db")
        username_clash=db.execute('''SELECT * FROM teachers
                                            WHERE username=?;''', (username,)).fetchone()
        if username_clash is not None: 
            form.username.errors.append("User is already taken")
        else:
            db.execute('''INSERT INTO teachers(username, password)
                      VALUES(?,?)''', (username, generate_password_hash(password))) #no .fetchall() and no variable because you are inserting into the database
            db.commit()
            return redirect(url_for('teacher_login'))
            # session.clear()
            # session["username"]=username
            # next_page=request.args.get("county")
            # if not next_page:
            #     next_page=url_for("county")
            # return redirect(next_page)
            #return redirect(url_for("county"))
            #form.username.errors.append("Username is already taken")
    return render_template("/teacher_sign_up.html", form=form, subtitle="Teacher Sign-up")  
@app.route("/", methods=["GET", "POST"]) 
def start(): 
    return render_template("start.html", subtitle = "SQL Learning Environment", user_type = g.user_type) 
@app.route("/index1", methods=["GET", "POST"]) 
def index1(): 
    db = get_db('app.db') 
    workbooks = db.execute('''SELECT * FROM workbooks''').fetchall() 
    return render_template("index1.html", workbooks=workbooks, subtitle = "SQL Workbooks") 
@app.route("/login", methods=["GET", "POST"])
def login(): 
    
    form=LoginForm()
    if form.validate_on_submit(): 
        user_type = "student"
        username=form.username.data
        password=form.password.data
        db=get_db("app.db")
        valid=db.execute('''SELECT * FROM users
                            WHERE username=?;''', (username,)).fetchone()
        if valid is None:
            form.username.errors.append("Unknown Username!")
#            return render_template("/county.html", form=form, title="Guess the county")
        elif not check_password_hash(valid["password"], password):
            return render_template("/login.html", form=form, message="Incorrect Password!", subtitle="Login")
        else:
            session.clear()
            session["username"]=username 
            session["user_type"]= user_type
            next_page=request.args.get("index1")
            if not next_page:
                next_page=url_for("index1")
            return redirect(next_page)
            
    return render_template("/login.html", form=form, subtitle="Login", user_type = g.user_type) 
@app.route("/teacher_login", methods=["GET", "POST"])
def teacher_login(): 
    
    form=LoginForm()
    if form.validate_on_submit(): 
        user_type = "teacher"
        username=form.username.data
        password=form.password.data
        db=get_db("app.db")
        valid=db.execute('''SELECT * FROM teachers
                            WHERE username=?;''', (username,)).fetchone()
        if valid is None:
            form.username.errors.append("Unknown Username!")
#            return render_template("/county.html", form=form, title="Guess the county")
        elif not check_password_hash(valid["password"], password):
            return render_template("/teacher.html", form=form, message="Incorrect Password!", subtitle="Teacher Login")
        else:
            session.clear()
            session["username"]=username 
            session["user_type"]= user_type
            next_page=request.args.get("upload")
            if not next_page:
                next_page=url_for("upload")
            return redirect(next_page)
            
    return render_template("/teacher.html", form=form, subtitle="Teacher Login", user_type = g.user_type)  
@app.route("/upload", methods=["GET", "POST"]) 
def upload(): 
    form = UploadForm() 
    message = "" 
    db_folder = app.config['DB_FOLDER']
    db_files = [f for f in os.listdir(db_folder) if f.endswith('.sqlite')] 
    form.existing_db.choices = ["Choose a database..."]
    for db in db_files: 
     form.existing_db.choices.append(db)

    message = ""

    if form.validate_on_submit():
        try:
            title = form.workbook_name.data
            question_file_data = form.question_file.data
            solution_file_data = form.solutions_file.data
            database_file_data = form.database.data
            selected_db = form.existing_db.data  
            # preamble = form.preamble.data

            
            if allowed_file(question_file_data.filename) and allowed_file(solution_file_data.filename):
                q_file = secure_filename(question_file_data.filename)
                s_file = secure_filename(solution_file_data.filename)

                q_file_path = os.path.join(app.config['UPLOAD_FOLDER'], q_file)
                s_file_path = os.path.join(app.config['SOLUTION_FOLDER'], s_file)

                question_file_data.save(q_file_path)
                solution_file_data.save(s_file_path)

                
                if selected_db:
                    d_file_path = os.path.join(db_folder, selected_db)  
                    message = "Using selected existing database."
                elif database_file_data and allowed_file(database_file_data.filename):
                    d_file = secure_filename(database_file_data.filename)
                    d_file_path = os.path.join(db_folder, d_file)

                    if d_file not in db_files:
                        
                        database_file_data.save(d_file_path)  

                else:
                    d_file_path = None  

                
                db = get_db("app.db")
                db.execute(
                    "INSERT INTO workbooks (title, questions_file, solutions_file, db_file) VALUES (?, ?, ?, ?)",
                    (title, q_file_path, s_file_path, d_file_path),
                )
                db.commit()

                message = "Workbook uploaded successfully!"

        except Exception as e:
            message = f"Error uploading file: {e}"

    return render_template("upload.html", form=form, message=message, subtitle="Upload", user_type = g.user_type)



def allowed_file(filename): 
    extension = filename.split('.')[-1]
    return extension
     

@app.route("/workbook/<workbook_id>")
def workbook_page(workbook_id):
    user_db = get_db("app.db")
    username = g.user 

    
    all_statuses = user_db.execute(
        '''SELECT question_id, status FROM questions 
           WHERE username = ? AND workbook_id = ?''',
        (username, workbook_id)
    ).fetchall()

    question_statuses = {row["question_id"]: row["status"] for row in all_statuses}

    
    workbook = get_workbook(workbook_id)
    if not workbook:
        return "Workbook not found", 404

    return render_template(
        "workbook.html", 
        workbook_id=workbook_id, 
        workbook=workbook, 
        question_statuses=question_statuses, 
        subtitle = workbook["title"],  
        user_type = g.user_type
    ) 
import traceback 

@app.route("/workbook/<workbook_id>/question/<int:question_id>", methods=["GET", "POST"]) 
def question_page(workbook_id, question_id): 
    workbook = get_workbook(workbook_id)
    if not workbook:
        return "Workbook not found", 404
    
    questions = workbook["questions"]
    solutions = workbook["solutions"]

    
    if question_id >= len(questions):
        return "Invalid question ID", 404
    # workbook = workbooks[workbook_id]
    questions = workbook["questions"]
    solutions = workbook["solutions"] 

    question_text = questions[question_id].strip()
    correct_query = solutions[question_id+1]
    db_name = workbook["db_file"] 
    status = 'incomplete'
    form = QueryForm()
    result = None
    evaluation = None 
    query_eval = None 
    preamble = workbook['preamble'] 
 
    user_db = get_db("app.db") 
    username = g.user 
    all_statuses = user_db.execute(
        '''SELECT question_id, status FROM questions 
           WHERE username = ? AND workbook_id = ?''',
        (username, workbook_id)
    ).fetchall() 
    
    question_statuses = {} 
    for row in all_statuses:
            q_id = row["question_id"]  
            question_statuses[q_id] = row["status"] 
    # print("Question Statuses:", question_statuses)  
    stored_query = user_db.execute('''SELECT answer FROM questions 
                                      WHERE username =? AND workbook_id = ? AND question_id = ?''', 
                                      (username, workbook_id, question_id)).fetchone()
    
    if request.method == "GET" and stored_query is not None:
        
        form.query.data = stored_query['answer'] 
    elif request.method == "GET": 
         form.query.data = ""  
    error = None
    
    if form.validate_on_submit():
        user_query = form.query.data 
        # user_db.execute('''UPDATE questions SET answer =? WHERE username =? AND workbook_id = ? AND question_id = ? ''', (user_query, username, workbook_id, question_id)) 
        # user_db.commit() 
        db = get_db(db_name)
        
        
        status = "in_progress" 
        
             
            
        try: 
            try: 
                # struct_user = extract_sql_parts(larkfunc(user_query))  
                user_result = db.execute(user_query).fetchall() 
            except SqliteError as e: 
                
                status = "in_progress" 
                all_statuses = user_db.execute(
                    '''SELECT question_id, status FROM questions 
                    WHERE username = ? AND workbook_id = ?''',
                    (username, workbook_id)
                ).fetchall() 
                
                question_statuses = {} 
                for row in all_statuses:
                    q_id = row["question_id"]  
                    question_statuses[q_id] = row["status"] 
                result = None
                error = f"SQLite Error: {str(e)}" 
                result = None 
                print(error) 
                return render_template(
            "question.html",
            form=form,
            workbook_id=workbook_id,
            workbook=workbook,
            question_id=question_id,
            question=question_text,
            result=result,
            error=error,  
            evaluation=None,
            total_questions=len(questions),
            status="in_progress",
            question_statuses=question_statuses,
            preamble=preamble,
            subtitle=f"Question {question_id + 1}", 
            
            user_type=g.user_type,
        ) 
            struct_user = extract_sql_parts(larkfunc(user_query)) 
            model_query = correct_query[0]
             
            if len(correct_query)>1: 
                i = 0 
                max_dist = 0 
                for query in correct_query: 
                    struct_model = extract_sql_parts(larkfunc(query)) 
                    distance = similarity_score(struct_user, struct_model) 
                     
                    if distance<=max_dist: 
                        model_query = correct_query[i] 
                        max_dist = distance 
                    i+=1
            # else: 
            #     model_query = correct_query[0] 
            print(model_query) 
            # user_result = db.execute(user_query).fetchall() 
            print(True) 
            correct_result = db.execute(model_query).fetchall() 
            print(True) 
            # print(user_query) 
            # print(correct_query) 
            # user_db = get_db("app.db") 
            clash = user_db.execute('''SELECT question_id FROM questions WHERE username =? AND workbook_id = ? AND question_id = ?''', (username, workbook_id, question_id)).fetchone() 

            if clash is not None:
                        user_db.execute('''UPDATE questions 
                                                SET  answer = ?, 
                                                status = ? WHERE username = ? AND workbook_id = ? AND question_id = ?''', 
                                                (user_query, status, username, workbook_id, question_id)) 
                        user_db.commit() 
            else: 
                        user_db.execute('''INSERT into questions(username, workbook_id, question_id, answer, status) 
                                   VALUES(?, ?, ?, ?, ?);''', 
                                   (username, workbook_id, question_id, user_query, status)) 
                        user_db.commit()
            evaluation = eval(
                check_cols(user_result, correct_result, user_query, model_query),
                check_rows(user_result, correct_result, user_query, model_query, db),
            ) 
            print("evaluation: " + str(evaluation[1]))
            if evaluation[1] == "Correct": 
                # print("Correct") 
                status = "completed"  
                # completed_questions = session.get(f"completed_{workbook_id}", [])
                # if question_id not in completed_questions:
                #     completed_questions.append(question_id) 
                
                user_db.execute('''UPDATE questions 
                                            SET   
                                            status = ? WHERE username = ? AND question_id = ? AND workbook_id = ?''', 
                                            (status, username, question_id,  workbook_id)) 
                user_db.commit() 
                
                # session[f"completed_{workbook_id}"] = completed_questions
                # session.modified = True 
            print(True)
            
            struct_model_1 = extract_sql_parts(larkfunc(model_query)) 
            
            query_eval = query_analysis(struct_user, struct_model_1) 
            if len(query_eval) > 2: 
                i = 1 
                q_str_eval = "" 
                while i<len(query_eval): 
                    q_str_eval = q_str_eval + "\n" + query_eval[i] 
                    i += 1  
                state = query_eval[0] 
                query_eval = [state, q_str_eval] 
            print(query_eval[0])
            

            # tree = larkfunc(user_query) 
            # print(tree) 
            # print("Tree: {tree.pretty()}") 
            # print(evaluation) 
            # evaluation_lines = evaluation[0].split("--") 
            # query_eval_lines = query_eval[0].split(":")  
            all_statuses = user_db.execute(
                '''SELECT question_id, status FROM questions 
                WHERE username = ? AND workbook_id = ?''',
                (username, workbook_id)
            ).fetchall() 
            
            question_statuses = {} 
            for row in all_statuses:
                q_id = row["question_id"]  
                question_statuses[q_id] = row["status"]
            # print("Question Statuses:", question_statuses)     
            return render_template(
                "question.html",
                form=form,
                workbook_id=workbook_id, 
                workbook = workbook,
                question_id=question_id,
                question=question_text,
                result=user_result,
                evaluation=evaluation,
                total_questions=len(questions), 
                question_statuses = question_statuses, 
                evaluation_lines = evaluation[0], 
                query_eval = query_eval, 
                preamble = preamble, 
                subtitle = "Question " + str(question_id +1 ), 
                user_type = g.user_type,  
                error = error
                # query_eval_lines = query_eval_lines
                
                
            ) 
            # result = user_result
            # return render_template(
            #     "question.html",
            #     form=form,
            #     workbook_id=workbook_id, 
            #     workbook = workbook,
            #     question_id=question_id,
            #     question=question_text,
            #     result=result,
            #     evaluation=evaluation,
            #     total_questions=len(questions), 
            #     completed_questions = completed_questions
            # ) 
        # except SqliteError as e: 
        #     status = "in_progress" 
        #     all_statuses = user_db.execute(
        #         '''SELECT question_id, status FROM questions 
        #         WHERE username = ? AND workbook_id = ?''',
        #         (username, workbook_id)
        #     ).fetchall() 
            
        #     question_statuses = {} 
        #     for row in all_statuses:
        #         q_id = row["question_id"]  
        #         question_statuses[q_id] = row["status"] 
        #     result = None
        #     error = f"SQLite Error: {str(e)}" 
        #     result = None 
        #     print(error) 
            
        except Exception as e: 
            status = "in_progress" 
            all_statuses = user_db.execute(
                '''SELECT question_id, status FROM questions 
                WHERE username = ? AND workbook_id = ?''',
                (username, workbook_id)
            ).fetchall() 
            
            question_statuses = {} 
            for row in all_statuses:
                q_id = row["question_id"]  
                question_statuses[q_id] = row["status"] 
            tb_str = traceback.format_exc() 
            error = f"Error executing query: {e}\nTraceback:\n{tb_str}" 
            result = None 
            
            print(error)
    # completed_questions = session.get(f"completed_{workbook_id}", []) 
    return render_template(
        "question.html",
        form=form,
        workbook_id=workbook_id, 
        workbook = workbook,
        question_id=question_id,
        question=question_text, 
        result=result, 
        error = error,
        evaluation=evaluation,
        total_questions=len(questions), 
        status = status, 
        question_statuses = question_statuses, 
        preamble = preamble, 
        subtitle = "Question " + str(question_id +1), 
        user_type = g.user 
        

        
    ) 
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("start"))

 
    
     



