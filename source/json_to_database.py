import json
import sqlite3

db_path = input('Enter the path of database to write into: ')
file_path = input('Enter the path of the file to read from: ')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
commit_count = 0

## create the tables
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member(
    user_id INTEGER, 
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

file_content = json.loads(open(file_path).read())

for ncr in file_content:
    commit_count += 1
    name, course, role = ncr[0], ncr[1],ncr[2]

    ## insert into user table and get the index of the user
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)',(name,))
    cur.execute('SELECT id FROM User WHERE name = ?',(name,))
    user_id = cur.fetchone()[0]

    ## insert into course table and get the index of the course
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)',(course,))
    cur.execute('SELECT id FROM Course WHERE title = ?',(course,))
    course_id = cur.fetchone()[0]

    ## insert into member table
    cur.execute(
    '''INSERT OR REPLACE INTO Member 
    (user_id,course_id,role) 
    VALUES (?,?,?)''',(user_id,course_id,role))
    
    if commit_count == len(file_content)//10:
        conn.commit()
        commit_count = 0
conn.commit()
conn.close()
print('Successfully finished') 