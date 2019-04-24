import json
import sqlite3

db_path = 'C:\\Users\\lzf95\\Desktop\\PythonPrac\\db2.sqlite'
file_path = 'C:\\Users\\lzf95\\Desktop\\PythonPrac\\files\\roster_data.json'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

## create the tables
cur.executescript('''
DROP IF EXISTS User;
DROP IF EXISTS Member;
DROP IF EXISTS Course;

CREATE TABLE User(
    id INTEGER PRIMRARY KEY NOT NULL AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER PRIMRARY KEY NOT NULL AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
)

CREATE TABLE Member(
    user_id INTEGER, 
    course_id INTEGER,
    role INTEGER,
    PRIMRARY KEY(user_id, course_id)
)
''')

file_content = json.loads(open(file_path).read())

for ncr in file_content:
    name, course, role = ncr[0], ncr[1],ncr[2]