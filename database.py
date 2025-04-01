# import os
# import sqlite3

# DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "movies.sqlite")
# db_connection=None
# def get_db(): 
#     global db_connection
#     if db_connection == None:
#         db_connection = sqlite3.connect(DATABASE,
#                 detect_types=sqlite3.PARSE_DECLTYPES, 
                
#         )
#         db_connection.row_factory = sqlite3.Row
#     return db_connection

# def close_db(e=None): 
#     global db_connection
    
#     if db_connection is not None:
#         db_connection.close() 
import os
import sqlite3
from flask import g

# DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "movies.sqlite")

# def get_db(db_name): 
#     if db_name == "app.db":  
#         DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db") 
#     else: 
#         DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{db_name}.sqlite")
#     if 'db' not in g:
#         g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
#         g.db.row_factory = sqlite3.Row  # Enable row objects (dict-like rows)
#     return g.db

# def close_db(e=None):
    
#     db = g.pop('db', None)
#     if db is not None:
#         db.close() 

def get_db(db_name):
    if 'db' not in g:
        g.db = {}
    
    if db_name not in g.db:
        if db_name == "app.db":
            DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")
        else:
            DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), db_name)
        
        g.db[db_name] = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db[db_name].row_factory = sqlite3.Row  
    
    return g.db[db_name]

def close_db(e=None):
    db_dict = g.pop('db', None)
    if db_dict is not None:
        for db in db_dict.values():
            db.close()