'''
This program used to reset the database
'''

import sqlite3

conn = sqlite3.connect('pagerank.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Pages;
DROP TABLE IF EXISTS Links;
DROP TABLE IF EXISTS Webs
''')
conn.commit()
cur.close()