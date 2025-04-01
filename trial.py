# from database import get_db, close_db 
from larktrial import *
import sqlite3, sys 
# movies = "movies" 
# db=get_db(movies) 
# tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() 
# for table in tables: 
#     print("Tables in the database:", table) 
def starification(query): 
    select = query.upper().find("SELECT") 
    from_index = query.upper().find("FROM") 

    modified_query = query[:select + len("SELECT")] + "*" +query[from_index:] 
    return modified_query 

query_x = '''SELECT actorid
FROM castings
WHERE movieid =
(  SELECT id FROM movies WHERE title = "Star Wars"
);''' 
query_y = '''SELECT actorid
FROM castings
WHERE movieid =
(  SELECT id FROM movies WHERE title = "Star Wars"
);
''' 
def modify_x(x, db): 
    modified_query = starification(x)
    return db.execute(modified_query).fetchall() 

def modify_y(y, db): 
    modified_query = starification(y)
    return db.execute(modified_query).fetchall()
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
#y = db.execute('''SELECT * FROM students WHERE points>=400;''').fetchall() 
# for i in students:
#     print(dict(i))  
#x = db.execute('''SELECT date_of_birt FROM students WHERE points>=500;''').fetchall() 
# for i,j in zip(y,x):
#     print(dict(i)) 
    
#     # print(list(dict(j).values())[0]) 
#     print((dict(j)))
#     print("---------") 
# y_keys = dict(y).keys()
# x_keys = dict(x).keys()  
'''check cols''' 
def check_cols(x, y, query_x, query_y):
    # y_keys = [] 
    # x_keys = [] 
    # # y=db.execute(query_y).fetchall() 
    # # x=db.execute(query_x).fetchall() 
    # for key in y: 
    #     for col in dict(key).keys():
    #         if col not in y_keys:
    #             y_keys.append(col)
    #             print("y --------- " + col)
    #             #print("y ---------") 
    # for key in x: 
    #     for col in dict(key).keys():
    #         if col not in x_keys:
    #             x_keys.append(col)
    #             print("x  --------  " + col)
    #             #print("x  ---------") 

    result = [] 
    req_cols = 0 
    x_keys = extract_columns_names(larkfunc(query_x)) 
    y_keys = extract_columns_names(larkfunc(query_y)) 
    # print(x_keys) 
    # print(y_keys) 
    if x_keys == ['*']: 
        if y_keys != ['*']: 
            star_str = "Correct columns but it looks like you used *. Try being more specific to the columns asked for in the question." 
            result.append(True) 
            result.append(star_str) 
    else:
        for key in y_keys: 
            if key in x_keys: 
                req_cols+=1 
            
        # if y_keys == x_keys: 
        #     print(True) 
        if req_cols == len(y_keys): 
            result.append(True) 
            result.append("Query includes all required columns. ")
        else: 
            result.append(False) 
            missing_cols = []  
            for key in y_keys:
                if key not in x_keys: 
                    
                    missing_cols.append(key) 
            missing_cols="Query is missing the following column/s and/or function/s: "+ str(missing_cols).strip('[]').replace("'", "") + ". Make sure to include them in the SELECT statement." 
            result.append(missing_cols)
            # print(False) 
            # print(result) 
        # result="Missing columns = "+ str(result).strip('[]').replace("'", "") 
        # m_keys = "Missing columns: " 
        # i = 0 
        # while i<len(result): 
        #     if len(result)>2: 
        #         m_keys+=result[i+1] + "," 
        #     else: 
        #         m_keys+=result[i+1] 
        #     i+=1 
        # result[1] = m_keys 
        # print(result)
    # result[1] = str(result[1]).strip('[]').replace("'", "")
    #print("Missing columns = "+ str(result).strip('[]').replace("'", ""))
    return result

'''check values/rows''' 
def check_rows(x, y, qx, qy, db): 
    y_values = [] 
    x_values = [] 
    # y=db.execute(query_y).fetchall() 
    # x=db.execute(query_x).fetchall() 
    for value in y: 
        for col in dict(value).values():
            if col not in y_values:
                y_values.append(col)
                # print(col)
        # print("y ---------") 
    for value in x: 
        for col in dict(value).values():
            if col not in x_values: 
                x_values.append(col)
            # print(col)
        # print("x  ---------") 
    # print(y_values) 
    # print(x_values) 
    result=[] 
    tree = larkfunc(qx) 
    table = traverse_for_first_from_table(tree)
    if check_key(modify_x(qx, db), modify_y(qy, db), db, table): 
        # print(True) 
        result.append(True) 
        result.append("Query captured all required rows")
    else: 
        # for value in x_values:
        #     if value not in x_values:
        #         result.append(value) 

        # print(False) 
        result.append(False) 
        result.append("There appears to be rows/values missing from your results. Try looking at any WHERE/HAVING clauses.") 
        # result="Missing values = "+ str(result )
    # result = str(result).strip('[]').replace("'", "") 
    return result
def eval(cols, rows): 
    verdict = "Incorrect" 
    if cols[0] == True: 
        if rows[0] == True: 
            verdict = "Correct" 
    eval_str = "Results Evaluation: " + "\n-- "+ cols[1] + "\n-- "+ rows[1] 
    eval_lines = [
        (cols[1], cols[0]),  # (message, is_correct)
        (rows[1], rows[0])   # (message, is_correct)
    ]
    result = [eval_lines, verdict] 
    return result
# def primary(db): 
#     # pk = db.execute('''SELECT * 
#     #     FROM pragma_table_info('{db}') 
#     #     WHERE pk > 0;''').fetchall() 
#     # return pk 
#     query = '''SELECT * 
#          FROM pragma_table_info('{db}') 
#          WHERE pk > 0;'''
#     result = db.execute(query).fetchall()  

#     # Extract primary key column(s)
#     primary_keys = [row[1] for row in result if row[5] > 0]  

#     return primary_keys
# def starification(query): 
#     select = query.upper().find("SELECT") 
#     from_index = query.upper.find("FROM") 

#     modified_query = query[:select + len("SELECT")] + "*" +query[from_index:] 
#     return modified_query 

def get_primary_key(db, table_name):
    query = f"PRAGMA table_info({table_name});"
    result = db.execute(query).fetchall()
    
    
    primary_keys = []

    
    for row in result:
        
        if row[5] == 1:
            
            primary_keys.append(row[1])
    
    return primary_keys 

def check_key(x, y, db, table_name): 
    primary_keys = get_primary_key(db, table_name)
    
    if not primary_keys:
        raise ValueError(f"No primary key found for table: {table_name}")
    
    key = primary_keys[0]  
    y_keys = [] 
    x_keys = []
    for value in y: 
        y_keys.append(dict(value)[key])
        #         print(col)
        # print("y ---------") 
    for value in x: 
        
                x_keys.append(dict(value)[key]) 
    if y_keys != x_keys: 
        # print("Keys don't match:") 
        # print("y_keys:", y_keys)
        # print("x_keys:", x_keys) 
        # print(y_keys, x_keys) 
        
        # for x_key in x_keys: 
        #     if x_key not in y_keys: 
        #         print(x_key) 
        return False
    else: 
        # print("Keys match:")
        # print("y_keys:", y_keys)
        # print("x_keys:", x_keys)
        # print(y_keys, x_keys) 
        return True 

def query_analysis(struct_x, struct_y): 
    query_eval = [] 
    # print(struct_x) 
    # print(struct_y)
    if struct_x == struct_y: 
        query_eval = [True, "Query contains all of the necessary clauses."] 
        print(query_eval)
    for key in struct_y.keys(): 
        if key not in struct_x.keys(): 
            # if key == "COUNT":  
            #         query_eval = [False, "The question is asking for the quantity of a column as a separate column. Remember to include that in the query."]   
            # print(key) 
            if key not in ["WHERE", "HAVING", "GROUP BY"]: 
                
                # if len(query_eval) >= 2: 
                #     print("caught")
                #     query_eval.append("It also looks like you're query is missing a conditional clause. Check whether the question requires a WHERE, ORDER BY, HAVING, GROUP BY.") 
                # else:
                    query_eval = [False, "Looks like you're query is missing a conditional clause. Check whether the question requires a WHERE, ORDER BY, HAVING, GROUP BY."]
     
        
    return query_eval 
query = '''SELECT yr, COUNT(*)
FROM movies
WHERE yr = 1975
GROUP BY yr;
'''  
query2 = '''SELECT yr
FROM movies
WHERE yr = 1975;'''
tquery = larkfunc(query.upper()) 
tquery2 = larkfunc(query2.upper())
# print(tquery)  
dict1 = extract_sql_parts(tquery) 
dict2 = extract_sql_parts(tquery2) 
print(dict1 ) 
print(dict2) 
query_eval = query_analysis(dict2, dict1) 
print(len(query_eval)) 
if len(query_eval) > 2: 
                i = 1 
                q_str_eval = "" 
                while i<len(query_eval): 
                    q_str_eval = q_str_eval + query_eval[i] + " "
                    i += 1  
                state = query_eval[0] 
                query_eval = [state, q_str_eval] 
print(query_eval)

    # for val in x_values:
    #     print(val) 
    # y_key = [] 
    # x_key = [] 

    # for i in y: 
         
    #     y_key.append(i[0]) 
    # for i in x: 
         
    #     x_key.append(i[0]) 
    
    # if y_key != x_key: 
    #     print("Tough luck!") 
    # else:
    #     print(y_key, x_key) 
        
         
    
     

    


# print(check_rows() )
# check_cols() 
 
# print(eval(check_cols(x, y), check_rows(x, y))) 
# print(check_key(modify_x, modify_y, "actorid") ) 
# print(larkfunc(query_x, query_y))





# close_db() 

# try: 
#     user_lark =  larkfunc('''UPDATE;''')
#     # struct_user = extract_sql_parts(user_lark) 
# except Exception as e:
#     print("G") 

# evalt = [None] 
# if evalt: 
#     print(evalt)  
    