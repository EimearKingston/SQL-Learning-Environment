DROP TABLE IF EXISTS users;
CREATE TABLE users
(
username TEXT PRIMARY KEY NOT NULL,
password TEXT NOT NULL
); 
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers
(
username TEXT PRIMARY KEY NOT NULL,
password TEXT NOT NULL
); 
DROP TABLE IF EXISTS questions;
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    workbook_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answer TEXT,  
    status TEXT CHECK(status IN ('incomplete', 'in_progress', 'completed')) DEFAULT 'incomplete',
    FOREIGN KEY (username) REFERENCES users(username)
); 
DROP TABLE IF EXISTS workbooks; 
CREATE TABLE workbooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    questions_file TEXT NOT NULL,
    solutions_file TEXT NOT NULL,
    db_file TEXT
); 
INSERT INTO workbooks(title, questions_file, solutions_file, db_file) 
VALUES('Movies', 'question_uploads/questions5.txt', 'solution_uploads/solutions5.sql', 'movies.sqlite');  
CREATE INDEX idx_questions_user_workbook_question ON questions(username, workbook_id, question_id); 
CREATE INDEX idx_workbook_question ON workbooks(id);  
