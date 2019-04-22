import urllib.request
import ssl
import re
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://zh.wikipedia.org/wiki/%E9%B2%81%E8%BF%85'    #input('Enter the url you want to craw: ')
webpage = urllib.request.urlopen(url,context=ctx).read().decode()
bs = BeautifulSoup(webpage,'html.parser')

for data in bs('img'):
    link = 'https:' + data.get('src',None)
    with open('./images/'+link.strip().split('/')[-1],'wb') as f:
        f.write(urllib.request.urlopen(link).read())
        f.close()