import sqlite3
import ssl
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('pagerank.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS Pages(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    url TEXT UNIQUE, html TEXT, error INTEGER, old_rank REAL, new_rank REAL
);

CREATE TABLE IF NOT EXISTS Links(
    fromn_id INTEGER, to_id INTEGER
);

CREATE TANLE IF NOT EXISTS Webs(
    url TEXT UNIQUE
)
''')

## check if there already exists a pagerank application
cur.execute('SELECT id,url FROM Pages ORDER BY id LIMIT 1')
result = cur.fetchone()
if result is not None:
    print('there exists a ')
else:
    url = input('Enter a new url to get start pagerank: ')
    ## use the default if input nothing
    if(len(url) < 1): url = 'https://www.python.org/'
    ## clean the url 
    if(url.endswith('/')): url = url[:-1]
    if(url.endswith('.html') or url.endswith('.htm')):
        pos = url.rfind('/')
        url = url[:pos]
    if(len(url) > 1):
        cur.execute('INSERT OR IGNORE INTO Pages (url,html,new_rank) VALUES (?, NULL,1.0)',(url,))
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES (?)',(url))
    conn.commit()

num_to_retr = 0
commit_count = 0
while True:
    if(commit_count == 10):
        conn.commit()
        commit_count = 0

    if(num_to_retr < 1):
        num_to_retr = int(input('Enter the numbe of websites to retrieve: '))
        if(num_to_retr < 1):
            print('Quit because no pages setted to retrieve, STOP program.')
            conn.commit()
            break
    
    num_to_retr -= 1
    commit_count += 1 

    ## choose one page from database to start retrieving html
    cur.execute('SELECT id,url from Pages WHERE html IS NULL AND error IS NULL ORDER BY id LIMIT 1')
    try:
        fetched = cur.fetchone()
        url = fetched[1]
        from_id = fetched[0]
    except:
        num_to_retr = 0
        print('No pages found to retrieve, STOP program.')
        conn.commit()
        break
    
    print('The selected page to retrieve is: ({}, {})'.format(from_id,url))

    ## start retrieving
    #### delete all the links with the from_id which are already in the database
    cur.execute('DELETE FROM Links WHERE from_id = ?',(from_id,))
    try:
        ## try open this url
        document = urlopen(url,context=ctx)
        document_code = document.getcode()
        
        if document_code != 200:
            print('Failed to retrieve the page, failed code is: {}'.format(document))
            cur.execute('UPDATE Pages SET error = ? WHERE url = ?',(document_code,url))
            continue
        
        if document.info().get_content_type != 'text/html':
            print('Ignore this page, the content of it is not text or html.')
            cur.execute('DELETE FROM Pages WHERE url = ?',(url,))
            continue
        
        ## the content is OK, start parsing this page
    except KeyboardInterrupt:
        print('Interrupted by the user, STOP program')
        conn.commit()
        break
    except:
        print('Failed to retrive or parse this page, continue to next one.')
        cur.execute('UPDATE Pages SET error = -1 WHERE url = ?',(url,))
        continue