from urllib.request import urlopen
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://py4e-data.dr-chuck.net/comments_220278.json'
data = urlopen(url,context=ctx).read().decode()
cont = json.loads(data)
out = 0

for i in range(len(cont['comments'])):
    out += int(cont['comments'][i].get('count',0))
print(out)