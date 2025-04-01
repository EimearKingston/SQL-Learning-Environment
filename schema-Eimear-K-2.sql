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
    db_file TEXT,  
    preamble TEXT
); 
INSERT INTO workbooks(title, questions_file, solutions_file, db_file, preamble) 
VALUES('Movies', 'question_uploads/questions5.txt', 'solution_uploads/solutions5.sql', 'movies.sqlite', 'The movies database we saw in lectures has the following schema:
movies(id, title, yr, score, votes, director)
actors(id, name)
castings(movieid, actorid)
Within the movies table, the yr attribute denotes the year the film was released (as a DEC-
IMAL value) and the score and votes attributes capture the average rating by viewers (on
a scale of zero to ten) and the number viewers who voted. Directors are identified by id
number only. (The DB is a cut-down version of a larger one. Several tables, including the
one containing directors’ names have been omitted.)
Each actor has an id number and a name. The castings table records which actors appeared
in which films.
The DB contains information about two thousand (mostly Hollywood) films from the 1920s
until 2000 and around six thousand actors who were active during that period.
Formulate queries for each of the following. Try to use joins in preference to subqueries where
possible. This is purely to force us to get as much practice working with joins as we can.
Problems below the dotted line are more challenging, especially if we don’t use subqueries.');  
CREATE INDEX idx_questions_user_workbook_question ON questions(username, workbook_id, question_id); 
CREATE INDEX idx_workbook_question ON workbooks(id);  
