import sqlite3
import xml.etree.ElementTree as ET

db_path = input('Enter the path of target Database to read into: ')
file_path = input('Enter the path of the Track file to read from: ')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
commit_count = 0

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

def lookup(block, tags):
    ## return an dictionary
    output = {}
    found = False
    for line in block:
        if found:
            output[cur_tag] = line.text
            found = False
            continue
        if line.tag == 'key' and line.text in tags:
            cur_tag = line.text
            found = True
    for tag in tags:
        if tag not in output.keys():
            output[tag] = None
    return output

file_content = ET.parse(file_path)
file_content_dic = file_content.findall('dict/dict/dict')
print('There is {} targets need to be extracted'.format(len(file_content_dic)))

for block in file_content_dic:
    commit_count += 1
    tags_to_lookup = ['Name','Artist','Album','Genre','Rating','Play Count','Total Time']
    
    ## extract the block and assign the values
    extr = lookup(block,tags_to_lookup)
    name, artist, album, length = extr['Name'], extr['Artist'], extr['Album'],extr['Total Time']
    genre, rating, play_count = extr['Genre'], extr['Rating'], extr['Play Count']

    ## continue if any of the parameter is None
    if not(name and artist and album and length and genre and rating and play_count) : 
        continue

    ## isnert the artist name into the Artist table
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)',(artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ?',(artist,))
    artist_id = cur.fetchone()[0]

    ## insert the album name into Album table
    cur.execute('INSERT OR IGNORE INTO Album (artist_id,title) VALUES (?,?)',(artist_id,album))
    cur.execute('SELECT id FROM Album WHERE title = ?',(album,))
    album_id = cur.fetchone()[0]

    ## insert the genre into Genre table
    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)',(genre,))
    cur.execute('SELECT id FROM Genre WHERE name = ?',(genre,))
    genre_id = cur.fetchone()[0]

    ## insert all related info into Track table
    cur.execute('''INSERT OR REPLACE INTO Track
        (title,album_id,genre_id,len,rating,count)
        VALUES (?,?,?,?,?,?)''',
        (name,album_id,genre_id,length,rating,play_count))
    
    ## commit periodically
    if commit_count == len(file_content_dic)//10:
        conn.commit()
        commit_count = 0

conn.commit()
cur.close()
print('Finished successfully')