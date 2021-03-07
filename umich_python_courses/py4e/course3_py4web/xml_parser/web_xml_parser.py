import ssl
from urllib.request import urlopen
import xml.etree.ElementTree as ET

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter url - ')  # http://py4e-data.dr-chuck.net/comments_42.xml
xml_data = urlopen(url, context=ctx).read()
root_xml = ET.fromstring(xml_data)

lst_comment_cnts = [int(elem.text) for elem in root_xml.findall('.//count')]

print(len(lst_comment_cnts), sum(lst_comment_cnts))
