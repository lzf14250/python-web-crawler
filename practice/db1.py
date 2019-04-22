import sqlite3
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cont = urllib.request.urlopen('https://www.py4e.com/code3/mbox.txt',context=ctx).decode()
conn = sqlite3.connect('db1.db')
ctr = conn.cursor()

for i in cont:
    print(i)