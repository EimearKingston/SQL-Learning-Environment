# from database import get_db, close_db 
# import sqlite3, sys 
# db=get_db() 
# # tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() 
# # for table in tables: 
# #     print("Tables in the database:", table) 
# def starification(query): 
#     select = query.upper().find("SELECT") 
#     from_index = query.upper().find("FROM") 

#     modified_query = query[:select + len("SELECT")] + "*" +query[from_index:] 
#     return modified_query 

# query_x = '''SELECT actorid
# FROM castings
# WHERE movieid =
# (  SELECT id FROM movies WHERE title = "Star Wars"
# );''' 
# query_y = '''SELECT actorid
# FROM castings
# WHERE movieid =
# (  SELECT id FROM movies WHERE title = "Big Sleep, The"
# );
# ''' 
# try: 
#     modify_x = db.execute(starification(query_x) ).fetchall()
#     modify_y = db.execute(starification(query_y) ).fetchall()
# except sqlite3.OperationalError as e: 
#     print(f"SQL Error:{e}") 
#     sys.exit(1)

 
# x=[]
 


# try: 
#     y = db.execute(query_y).fetchall()  
#     x = db.execute(query_x).fetchall() 
# except sqlite3.OperationalError as e: 
#     print(f"SQL Error:{e}") 
#     sys.exit(1)
# #y = db.execute('''SELECT * FROM students WHERE points>=400;''').fetchall() 
# # for i in students:
# #     print(dict(i))  
# #x = db.execute('''SELECT date_of_birt FROM students WHERE points>=500;''').fetchall() 
# # for i,j in zip(y,x):
# #     print(dict(i)) 
    
# #     # print(list(dict(j).values())[0]) 
# #     print((dict(j)))
# #     print("---------") 
# # y_keys = dict(y).keys()
# # x_keys = dict(x).keys()

# def get_table_columns(table_name):
#     try:
#         # Directly execute the query on the db connection
#         tables = db.execute(f"PRAGMA table_info({table_name})")
#         columns = [row[1] for row in tables.fetchall()]  # row[1] is the column name
#         return columns
#     except sqlite3.Error as e:
#         print("Database error:", e)
#         return []
  
# '''check cols''' 
# def check_cols(x, y):
#     y_keys = [] 
#     x_keys = [] 
#     # y=db.execute(query_y).fetchall() 
#     # x=db.execute(query_x).fetchall() 
#     for key in y: 
#         for col in dict(key).keys():
#             if col not in y_keys:
#                 y_keys.append(col)
#                 print("y --------- " + col)
#                 #print("y ---------") 
#     for key in x: 
#         for col in dict(key).keys():
#             if col not in x_keys:
#                 x_keys.append(col)
#                 print("x  --------  " + col)
#                 #print("x  ---------") 

#     result = []  
#     if y_keys == x_keys: 
#         print(True) 
#         result.append("Correct columns")
#     else: 
#         for key in y_keys:
#             if key not in x_keys:
#                 result.append(key)

#         print(False) 
#         result="Missing columns = "+ str(result).strip('[]').replace("'", "") 
#     result = str(result).strip('[]').replace("'", "")
#     #print("Missing columns = "+ str(result).strip('[]').replace("'", ""))
#     return result

# '''check values/rows''' 
# def check_rows(x, y): 
#     y_values = [] 
#     x_values = [] 
#     # y=db.execute(query_y).fetchall() 
#     # x=db.execute(query_x).fetchall() 
#     for value in y: 
#         for col in dict(value).values():
#             if col not in y_values:
#                 y_values.append(col)
#                 # print(col)
#         # print("y ---------") 
#     for value in x: 
#         for col in dict(value).values():
#             if col not in x_values: 
#                 x_values.append(col)
#             # print(col)
#         # print("x  ---------") 
#     print(y_values) 
#     print(x_values) 
#     result=[] 
#     if check_key(modify_x, modify_y, "actorid"): 
#         print(True) 
#         result.append("Correct values")
#     else: 
#         # for value in x_values:
#         #     if value not in x_values:
#         #         result.append(value) 

#         print(False) 
#         result.append("") 
#         # result="Missing values = "+ str(result )
#     result = str(result).strip('[]').replace("'", "") 
#     return result
# def eval(cols, rows): 
#     result = "Evaluation: " + "\n-- "+ cols + "\n-- " + rows 
#     return result 

# # def starification(query): 
# #     select = query.upper().find("SELECT") 
# #     from_index = query.upper.find("FROM") 

# #     modified_query = query[:select + len("SELECT")] + "*" +query[from_index:] 
# #     return modified_query 

# def check_key(x, y, key): 
#     y_keys = [] 
#     x_keys = []
#     for value in y: 
#         y_keys.append(dict(value)[key])
#         #         print(col)
#         # print("y ---------") 
#     for value in x: 
        
#                 x_keys.append(dict(value)[key]) 
#     if y_keys != x_keys: 
#         print("Keys don't match:") 
#         print("y_keys:", y_keys)
#         print("x_keys:", x_keys) 
#         print(y_keys, x_keys) 
        
#         # for x_key in x_keys: 
#         #     if x_key not in y_keys: 
#         #         print(x_key) 
#         return False
#     else: 
#         print("Keys match:")
#         print("y_keys:", y_keys)
#         print("x_keys:", x_keys)
#         print(y_keys, x_keys) 
#         return True
#     # for val in x_values:
#     #     print(val) 
#     # y_key = [] 
#     # x_key = [] 

#     # for i in y: 
         
#     #     y_key.append(i[0]) 
#     # for i in x: 
         
#     #     x_key.append(i[0]) 
    
#     # if y_key != x_key: 
#     #     print("Tough luck!") 
#     # else:
#     #     print(y_key, x_key) 
#     # 

# def select(query): 
#     words = query.split() 
#     statement = ["SELECT", "INSERT", "DELETE", "UPDATE"] 
#     index = 0 
#     if words[index] not in statement: 
#         return "Error" 
#     else: 
#         index += 1 
#     next = ["*", "DISTINCT", "ALL", get_table_columns("movies"), get_table_columns("castings"), get_table_columns("actors")] 
#     while words[index] != "FROM": 
#         if words[index] not in next or words[index] != ",": 
#             return "Error" 
#         else: 
#             index += 1 
#     tables = ["movies", "actors", "castings"] 
#     if words[index] == "FROM": 
#         index += 1 
#     else: 
#         return "Error" 
#     keywords = ["WHERE", "GROUP BY", "ORDER BY"]
#     while words[index] not in keywords: 
         
#         if words[index] not in tables and words[index] != "," and words[index] != "JOIN": 
#             return "Error" 
#         else: 
#             if words[index+1] == "AS": 
#                 if words[index+3] == "JOIN": 
#                     joins(words, index+3, tables) 
#             elif words[index+1] == "JOIN": 
#                 joins(words, index+2, tables)
#             index += 1 

# def joins(query, index, tables): 
    
#     if query[index] not in tables: 
#         return "Error" 
#     else:  
#         index += 1 
#     while query[index] != "ON": 
#         if query[index] == "AS": 
#             index += 2 
#             if query[index] == "JOIN": 
#                 index += 1 
#                 if query[index] in tables: 
#                     continue 
#         else: 
#             break

    


# # print(check_rows() )
# # check_cols() 
 
# # print(eval(check_cols(x, y), check_rows(x, y))) 
# # print(check_key(modify_x, modify_y, "actorid") ) 

# # print(select(query_x))
# print(get_table_columns("movies"), get_table_columns("castings"), get_table_columns("actors"))




# close_db() 
def allowed_file(filename): 
    
    extension = filename.split('.')[-1]
    return extension
file = "3.sqlite" 
print(allowed_file(file)) 
import os
def read(file): 
    import re
    #file_path = os.path.abspath(file) 
    #print(file_path)
    with open(file, 'r') as f:
        content = f.read() 
    print(content)

    # Split content by lines
    lines = content.splitlines()

    questions = []
    current_question = ""

    for line in lines:
        line = line.strip()  # Clean up the line by removing leading/trailing spaces
        
        if re.match(r'^\d+\.', line):  # Check if the line starts with a number followed by a period
            # If we already have a question, append the current one
            if current_question:
                questions.append(current_question.strip())
            
            # Start a new question with this line (remove the leading number and period)
            current_question = re.sub(r'^\d+\.\s*', '', line)
        else:
            # If it's part of the current question (multi-line question), add it
            if current_question:
                current_question += " " + line 
    if current_question:
        questions.append(current_question.strip())

    return questions
from larktrial import *
# print(read('question_uploads/questions5.txt')) 
query1 = '''SELECT  a.name, m.title
FROM actors AS a
	JOIN castings AS c1
	JOIN movies AS m
	ON a.id = c1.actorid AND c1.movieid = m.id
GROUP BY c1.actorid, c1.movieid 
HAVING COUNT(c2.movieid) >= 10;
''' 
query2 = '''SELECT  a.name, m.title
FROM actors AS a
	JOIN castings AS c1
	JOIN movies AS m
	JOIN castings AS c2
	ON a.id = c1.actorid AND a.id = c2.actorid AND c1.movieid = m.id
GROUP BY c1.actorid, c1.movieid
HAVING COUNT(c2.movieid) >= 10;''' 
def similarity_score(dict1, dict2):
    distance = 0  

    for k in dict2:  
        if k in dict1: 
            distance += abs(dict1[k] - dict2[k]) 
        else: 
            distance +=1 

             

    return distance 
# tree1 = larkfunc(query1)
# tree2 = larkfunc(query2) 
# parts = extract_sql_parts(tree1) 
# parts2 = extract_sql_parts(tree2) 
# print(parts) 
# print(parts2) 
# print(similarity_score(parts, parts2)) 

def extract(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    
    parts = re.split(r'--\s*\d+\)', content) 
    parts_dict = {} 
    i = 1 
    for part in parts: 
        part.strip()  
        
        
        
        if part: 
            lines_list = []

            
            for line in part.split(";"):
                
                stripped_line = line.strip()

                
                if stripped_line:
                    lines_list.append(stripped_line+";")
 
            parts_dict[i] = lines_list
            i+=1
    
    return parts_dict 

    
    # questions = {}
    # current_question_number = None
    
    # for part in parts:
    #     part = part.strip()
        
    #     if part:  # Only process non-empty parts
    #         # Step 2: Try to extract the question number from the start of the part
    #         match = re.match(r'(\d+\))', part)  # e.g., "17)"
    #         if match:
    #             current_question_number = match.group(1)
    #             query = part[match.end():].strip()  # Clean the query
                
    #             # If a question already exists, append the query to its list
    #             if current_question_number not in questions:
    #                 questions[current_question_number] = []
    #             questions[current_question_number].append(query)
    #         else:
    #             # If there's no question number, treat the part as a query belonging to the last question
    #             if current_question_number:
    #                 query = part.strip()
    #                 questions[current_question_number].append(query)
    
    # return questions 
    for line in parts: 
        print("Line: " + line) 
queries = extract('solutions5.sql') 
# for key, value in queries.items():
#     print(f"Question {key}:")
#     print(value)
#     print() 

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

file = read("trial.txt") 
print(file[1])

