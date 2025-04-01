from lark import Lark, UnexpectedToken, Tree, UnexpectedCharacters, UnexpectedEOF, UnexpectedInput,  Token
def larkfunc(q1): 
    # print("tree") 
    g = r"""
    start: normal_query | union_query 

    normal_query:  "SELECT" distinct? STAR? columns? "FROM" from_func join_clause* ["WHERE" conditions] ["GROUP BY" group_by ["HAVING" having_conditions]] ["ORDER BY" order_by] ["LIMIT" limit] ";"

    distinct: "DISTINCT"

    union_query: "SELECT"? subquery_type ((UNION_TYPE | MATHS_OP) subquery_type)* ";"

    STAR: "*" 

    UNION_TYPE: "UNION" | "UNION ALL" 

    subquery_type: (subquery | "(" subquery ")") alias? 

    columns: column_or_aggregate ("," column_or_aggregate)* alias?

    column_or_aggregate: column  | column_with_alias | aggregate | maths_expr | concatenation | subquery_condition | func_call | STAR

    column_with_alias: (column | value | concatenation | aggregate | maths_expr) ["AS" (CNAME | SQ_STRING)]

    column: CNAME ("." CNAME)? 

    from_func: table_or_alias | subquery_type 

    table_or_alias: table ["AS"? (CNAME | SQ_STRING)]

    table: CNAME

    join_clause: join_type? "JOIN" (table_or_alias | subquery_type) ["ON" conditions] (join_clause)*

    join_type: "INNER" | "LEFT" | "RIGHT" | "FULL"

    join_condition: column comparator column

    alias: "AS"? (CNAME | SQ_STRING) 

    aggregate: func_name "(" distinct? column_or_star ")" ["AS" (CNAME | SQ_STRING)]

    func_call: func_name "(" func_args ")"

    func_args: value ("," value)*

    FUNC_NAME: "COUNT" | "SUM" | "AVG" | "MIN" | "MAX" | "CONCAT" | "SUBSTR" | "DATEDIFF" 
    func_name: FUNC_NAME

    column_or_star: column | "*"

    group_by: column ("," column)*

    order_by: (column | aggregate | condition) ("ASC" | "DESC")? ("," order_by)?

    conditions: condition ("AND" condition alias?)* ("OR" condition)* 

    concatenation: value ("||" value)* 

    having_conditions: (condition | aggregate_condition) ("AND" (condition | aggregate_condition))* | "(" having_conditions ")" 

    aggregate_condition: aggregate comparator value 

    WHERE_FUNC: "ALL" | "ANY" | "NOT IN" | "IS NOT NULL" | "CURDATE()" | "IS NULL" 
    where_func: WHERE_FUNC
    substr: func_call condition

    condition: column comparator where_func
        |column comparator value 
        | column "BETWEEN" value "AND" value 
        | value comparator column  
        | where_func "BETWEEN" value "AND" value 
        | subquery_type MATHS_OP subquery_type 
        | column MATHS_OP column 
        | column where_func condition? 
        | column comparator where_func condition? 
        | column comparator where_func  
        | column value
        | column "IN" "(" subquery ")"
        | column "IN" "(" value ("," value)* ")"  
        | "(" conditions ")" 
        | func_call comparator func_call  
        | column comparator func_call 
        | column comparator where_func
        | column comparator "(" subquery ")"  
        | column comparator "(" normal_query ")"  
        | subquery_condition 
        | column comparator concatenation
        
        


    subquery_condition: "(" subquery ")"  

    comparator: COMPARATOR
    COMPARATOR: "=" | ">" | "<" | ">=" | "<=" | "<>" | "LIKE"

    value: INTEGER | DECIMAL | SIGNED_INTEGER | SQ_STRING | "(" conditions ")" | "(" subquery ")" | func_call | "(" value ")" | STAR | maths_expr | column 

    limit: INTEGER 

    maths_expr: value (MATHS_OP value)+ 

    MATHS_OP: "+" | "-" | "*" | "/"

    subquery: "SELECT" distinct? STAR? columns? "FROM" from_func join_clause* ["WHERE" conditions] ["GROUP BY" group_by ["HAVING" having_conditions]] ["ORDER BY" order_by] ["LIMIT" limit] alias?";"? 

    SQ_STRING: /'[^']*'/ | /"[^"]*"/  

    INTEGER: /[0-9]+/

    DECIMAL: INTEGER? "." INTEGER

    SIGNED_INTEGER: /[+-]?(0|[1-9][0-9]*)/

    %import common.CNAME
    %import common.WS
    %ignore WS
    """
    sql_parser = Lark(g, start='start')


    # sql_query = '''SELECT yr
    # FROM movies
    # WHERE yr = 1975;'''
    # sql_query1 = '''SELECT yr
    # FROM movies
    # WHERE yr = 1980;'''

    try:
        etree = sql_parser.parse(q1) 
        # print(etree.pretty())
        return etree
    except UnexpectedToken as e:
        
        expected = ", ".join(e.expected) if e.expected else "nothing"
        return f"Syntax error at line {e.line}, column {e.column}. Expected: {expected}, but found: '{e.token}'."
    except UnexpectedCharacters as e:
        
        return f"Syntax error at line {e.line}, column {e.column}. Unexpected character: '{e.char}'."
    except UnexpectedEOF as e:
        
        expected = ", ".join(e.expected) if e.expected else "nothing"
        return f"Syntax error: Unexpected end of input. Expected: {expected}."
    except Exception as e:
        
        return f"An unexpected error occurred: {str(e)}"
    # etree1 = sql_parser.parse(q2)
    # print(etree.pretty()) 
    # print(etree1.pretty()) 
    return etree 

'''column taken out of value, may have to put back in'''
'''Took | alias out of value'''
    

# #print(larkfunc('''SELECT yr
#     FROM movies
#     WHERE yr = 1975;''', '''SELECT yr
#     FROM movies
#     WHERE yr = 1980;''')) 
import re

def extract_sql_queries(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    
    content = re.sub(r'--.*', '', content)
     
    
    queries = [query.strip() + ";" for query in content.split(';') if query.strip()]
    
    return queries 

def extract_sql_parts(tree):
    sql_parts = {
        "SELECT": 0, 
        "COUNT": 0,
        "MAX": 0,
        "FROM": 0,
        "WHERE": 0, 
        "ASC": 0,
        "DESC": 0,
        "GROUP BY": 0,
        "HAVING": 0,
        "ORDER BY": 0,
        "LIMIT": 0,
        "JOIN": 0,
        "UNION": 0,
        "LIKE": 0,
        "IN": 0,
        "BETWEEN": 0,
        ">": 0,
        "<": 0,
        ">=": 0,
        "<=": 0,
        "<>": 0,
        "=": 0,
        "SUBQUERY": 0, 
        "INSERT":0, 
        "UPDATE":0, 
        "ANY":0, 
        "ALL":0, 
         
    }

    

    
    parts = traverse_parts(tree, sql_parts, False)

    
    return {k: v for k, v in parts.items() if v > 0} 

def traverse_parts(node, sql_parts, in_join):
        
        if node.data == "columns":
            sql_parts["SELECT"] += 1

        if node.data == "func_call":
            for child in node.children:
                if type(child) == Tree and child.data == "func_name":
                    func_name = child.children[0].value
                    sql_parts[func_name] += 1

        if node.data == "from_func":
            sql_parts["FROM"] += 1
        if node.data == "conditions": 
            if in_join == False:
                sql_parts["WHERE"] += 1
        if node.data == "group_by":
            sql_parts["GROUP BY"] += 1
        if node.data == "having_conditions":
            sql_parts["HAVING"] += 1
        if node.data == "order_by":
            sql_parts["ORDER BY"] += 1 
            for child in node.children: 
                if type(child) == Tree and child.data == "condition": 
                    print("condi")
                    for grandchild in child.children: 
                        print("grand", grandchild.children[0]) 
                        for grandgrandchild in grandchild.children: 
                            # print(grandgrandchild)
                            if type(grandgrandchild) == Tree: 
                                print(grandgrandchild)
                                # if grandgrandchild.value in sql_parts.keys():
                                #     sql_parts[grandgrandchild.value] += 1 
        if node.data == "limit":
            sql_parts["LIMIT"] += 1
        if node.data == "join_clause": 
            in_join = True
            sql_parts["JOIN"] += 1
        if node.data == "union_query":
            sql_parts["UNION"] += 1
        if node.data == "subquery":
            sql_parts["SUBQUERY"] += 1  

        if node.data == "condition":
            for child in node.children:
                if type(child) == Tree and child.data == "comparator":
                    for grandchild in child.children:
                        if type(grandchild) == Token: 
                            if grandchild.value in sql_parts.keys():
                                sql_parts[grandchild.value] += 1 
               
                elif type(child) == Tree and child.data == "where_func":
                    for grandchild in child.children:
                        if type(grandchild) == Token: 
                            if grandchild.value in sql_parts.keys():
                                sql_parts[grandchild.value] += 1 
                            else: 
                                print("error") 
        

        
        for child in node.children:
            if type(child) == Tree:
                traverse_parts(child, sql_parts, in_join) 
        return sql_parts
# queries = [
#     "SELECT * FROM movies WHERE yr = 1980;",  
#     "SELECT * movies WHERE yr = 1980;",       
#     "SELECT * FROM WHERE yr = 1980;",         
#     "SELECT * FROM movies WHERE yr =;",       
#     "SELECT * FROM movies WHERE yr = 1980",   
#     "SELECT * FROM movies WHERE yr = '1980;", 
# ] 
def extract_structure(tree):
    structure = []
    for node in tree.iter_subtrees():
       
        
            for child in node.children: 
                if child is not None and hasattr(child, "data") and child.data in ["SELECT", "columns", "distinct", "STAR"]:
                    continue  
                else:
                    structure.append(
                        (node.data, 
                        tuple(child.data if hasattr(child, "data") else str(child) for child in node.children))
                    ) 
    
    return structure 
queries = extract_sql_queries("solutions5.sql") 

# for query in queries:
#     result = larkfunc(query.upper())
#     if isinstance(result, str):  # If it's an error message
#         print(f"Error in query: {query}\n{result}\n")
#     else:
#         print(f"Query parsed successfully: {query}\n{result.pretty()}\n") 
# print(extract_sql_parts(larkfunc('''SELECT COUNT(*)
# FROM movies;''')))
# i = 1
# for query in queries: 
# #     print("\nTree"+str(i)) 
#     print(query)
#     tree = larkfunc(query.upper()) 
#     print(tree) 
#     i+=1  

s1 = '''SELECT MAX(film_count)
FROM
( SELECT director, COUNT(*) AS 'film_count'
  FROM movies
  GROUP by director
 ) AS film_counts;
 '''
sql_query = '''SELECT yr, title
FROM movies 
WHERE yr > 1980 

;'''
# sql_query1 = '''SELECT yr, title
#     FROM movies
#     WHERE yr = 1980;''' 
# tree = larkfunc(sql_query.upper()) 
# print(tree.pretty()) 
 
# tree1 = larkfunc(sql_query1.upper()) 
# struct = extract_structure(tree) 
# struct1 = extract_structure(tree1) 
# if struct == struct1: 
#     print(True) 
# else: 
#     print(False)

# t1 = larkfunc(sql_query)   
# t2 = larkfunc(sql_query1) 
# print(t1.pretty())
# list_t1 = print(extract_sql_parts(tree) )
# list_t2 = print(extract_sql_parts(tree1) ) 

def traverse_for_first_from_table(node):
    
    if node.data == "from_func": 
        # print(node.data)
        for child in node.children: 
            # print(child)
            if isinstance(child, Tree) and child.data == "table_or_alias":
                for sub_child in child.children: 
                    # print(sub_child)
                    if isinstance(sub_child, Token) and sub_child.type == 'CNAME': 
                         return sub_child.value 
                    elif isinstance(sub_child, Tree):
                        for sub_sub_child in sub_child.children:
                            if isinstance(sub_sub_child, Token) and sub_sub_child.type == 'CNAME': 
                                # print(sub_sub_child.value)
                                return sub_sub_child.value
    
    
    for child in node.children:
        if isinstance(child, Tree):
            table_name = traverse_for_first_from_table(child)
            if table_name: 
                return table_name

    return None 

# sql_query1 = '''SELECT name, COUNT(*)
# FROM 
#    actors JOIN castings
#    ON actors.id = castings.actorid
# GROUP BY name
# HAVING COUNT(*) >= 10; 
# ''' 
# tree = larkfunc(sql_query1.upper()) 
# print("Tree" , tree) 
# print(traverse_for_first_from_table(tree))  


# if list_t1 == list_t2: 
#     print(list_t1, list_t2, True) 
# else: 
#     print(list_t1, list_t2, False) 

# # answer_query = '''SELECT id
# #                   FROM movies
# #                   WHERE yr = 1975;'''
# # user_query   = '''SELECT *
# #                   FROM movies
# #                   WHERE yr > 1975;'''

# # answer_tree = larkfunc(answer_query)
# # user_tree   = larkfunc(user_query)

# # if compare_queries(answer_tree, user_tree):
# #     print("Correct! The query is similar enough.")
# # else:
# #     print("Incorrect. The structure or clauses do not match.") 
def extract_columns_names(tree):
    
    columns = []

    
    
    cols = traverse(tree, columns)

    return cols 

#f Token then child.value 
# If Tree then child[0].value 
def traverse(node, columns, in_select=False):
        
        if node.data == "normal_query":
            
            in_select = True 
            for child in node.children: 
                if isinstance(child, Token) and child.type == "STAR": 
                    columns.append(child.value)
        # if in_select and node.data == "STAR":
        if in_select and node.data == "columns":
            
            for child in node.children:
                if isinstance(child, Tree) and child.data == "column_or_aggregate":
                    
                    for grandchild in child.children:
                        if isinstance(grandchild, Tree):
                            if grandchild.data == "column_with_alias":
                                
                                for subchild in grandchild.children:
                                    if isinstance(subchild, Tree):
                                        if subchild.data == "column":
                                            
                                            column_children = subchild.children
                                            if len(column_children) > 1:
                                                column_name = column_children[-1].value 
                                            else:
                                                column_name = column_children[0].value
                                            
                                            columns.append(column_name)
                                            
                                            for subsubchild in subchild.children:
                                                if isinstance(subsubchild, Tree) and subsubchild.data == "func_call":
                                                    
                                                    func_name = subsubchild.children[0].children[0].value
                                                    
                                                    func_args = []
                                                    for arg_node in subsubchild.children[1].children:
                                                        if isinstance(arg_node, Tree):
                                                            
                                                            if arg_node.data == "value":
                                                                for arg_child in arg_node.children:
                                                                    if isinstance(arg_child, Tree) and arg_child.data == "STAR":
                                                                        func_args.append("*")
                                                                    elif isinstance(arg_child, Token):
                                                                        func_args.append(arg_child.value)
                                                        elif isinstance(arg_node, Token):
                                                            func_args.append(arg_node.value)
                                                    columns.append(f"{func_name}({''.join(func_args)})") 
                                        if subchild.data == "value": 
                                            for subsubchild in subchild.children:
                                                if isinstance(subsubchild, Tree):
                                                    if subsubchild.data == "func_call": 
                                                        print("call") 
                                                        for subsubsubchild in subsubchild.children:
                                                            if isinstance(subsubsubchild, Tree):
                                                                if subsubsubchild.data == "func_name": 
                                                                    columns.append(subsubsubchild.children[0].value)
                                                        
                                                        
                            elif grandchild.data == "column":
                                
                                
                                
                                column_children = grandchild.children
                                
                               
                                if len(column_children) > 1:
                                    column_name = column_children[-1].value  
                                else:
                                    
                                    column_name = column_children[0].value
                                    
                                columns.append(column_name) 
                            elif grandchild.data == "value":
                                
                                
                                
                                column_children = grandchild.children
                                
                               
                                if len(column_children) > 1:
                                    column_name = column_children[-1].value  
                                else:
                                    
                                    column_name = column_children[0].value
                                    
                                columns.append(column_name)
                            # elif grandchild.data == "column_or_aggregate":
                            
                            #     for subsubchild in grandchild.children:
                            #         if isinstance(subsubchild, Tree) and subsubchild.data == "star":
                            #             star_found = True

                                    
            # if star_found:
            #     columns.append("*")


        
        if node.data == "subquery":
            return

        
        for child in node.children:
            if isinstance(child, Tree):
                traverse(child, columns, in_select)
        return columns
query = '''SELECT yr, COUNT(*)
FROM movies
WHERE yr = 1975
GROUP BY yr;
'''  
query2 = '''SELECT yr, COUNT(*)
FROM movies
WHERE yr = 1975
ORDER BY yr ASC;'''
tquery = larkfunc(query2.upper()) 
# print(extract_columns_names(tquery)) 
# tquery2 = larkfunc(query2.upper())
print(tquery.pretty()) 
print(tquery)  

print(extract_sql_parts(tquery))