import sqlite3
import ssl
import re

conn = sqlite3.connect('C:\\Users\\lzf95\\Desktop\\PythonPrac\\db1.sqlite')
cur = conn.cursor()
file_path = 'C:\\Users\\lzf95\\Desktop\\PythonPrac\\mbox.txt'

cur.execute('drop table if exists Counts')

cur.execute('create table Counts(org TEXT, count INTEGER)')

with open(file_path,'r') as f:
    for line in f:
        catched = re.findall('^From .*?@(.*?) ',line)
        if not catched: continue
        domain = catched[0]
        cur.execute('select * from Counts where org = ?',(domain,))
        row = cur.fetchone()
        if row is None:
            cur.execute('insert into Counts (org,count) values (?,1)',(domain,))
        else:
            cur.execute('update Counts set count = count + 1 where org = ? ',(domain,))
    conn.commit()
    f.close()

sqlstr = 'SELECT org,count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])
    
print('finished !')

cur.close()