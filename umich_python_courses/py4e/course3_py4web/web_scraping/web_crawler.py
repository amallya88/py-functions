import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

def crawl_website(start_url, stride=1, repeat=1):
    """ Crawl a website
    stride: starting from stat_url follow the link at position specified by stride
    repeat: repeat the crawl repeat number of times
    return the value of <a href> tag that was found at end of crawling """
    url = start_url
    answer = ""

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for count in range(repeat):
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve all of the anchor tags
        links = soup.find_all('a')
        try:
            answer = links[stride-1].contents[0]
            url = links[stride-1].get('href')
        except IndexError:
            return answer

    return answer


start_url = input('Enter - ')  # http://py4e-data.dr-chuck.net/known_by_Fikret.html
stride = int(input('Enter position: '))
repeat = input('Enter count: ')

print(crawl_website(start_url, int(stride), int(repeat)))
