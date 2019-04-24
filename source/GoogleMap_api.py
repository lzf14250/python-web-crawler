import urllib.request
import urllib.parse
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://py4e-data.dr-chuck.net/json?'
info = {'address':'City of Westminster College','key':42}
url_e = url + urllib.parse.urlencode(info)
data = json.loads(urllib.request.urlopen(url_e,context=ctx).read().decode())
loc = data['results'][0]['geometry']['location']

print('The Coordinate of this address is:({:.3f},{:.3f})'.format(loc['lat'],loc['lng']))