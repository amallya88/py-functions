import json
from urllib.request import urlopen
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')  # http://py4e-data.dr-chuck.net/comments_42.json
json_txt = urlopen(url, context=ctx).read()
url_json_dict = json.loads(json_txt)

print(sum([item['count'] for item in url_json_dict['comments']]))



