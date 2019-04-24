from urllib.request import urlopen
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cmd = 'http://py4e-data.dr-chuck.net/comments_220277.xml'
cont = urlopen(cmd,context=ctx).read().decode()
tree = ET.fromstring(cont)

out = 0
for ele in tree.findall('.//count'):
    out += int(ele.text)

print(out)