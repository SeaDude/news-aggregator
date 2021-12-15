import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# ---------------------------------------------------

def get_source(url):
    url = urllib.parse.urlparse(url).netloc
    source = url.split('.')
    if len(source) == 2:
        source = source[0]
    elif len(source) == 3:
        source = source[1]
    elif len(source) == 4:
        source = source[1]
    return source


def get_rss(url):
    try:
        header= {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url=url, headers=header)
        response = urllib.request.urlopen(request)
        bsoup = BeautifulSoup(response, 'xml')
        return bsoup
    except:
        print(url)
        return None


def get_headlines(bsoup_obj, source):
    headlines = []
    story = bsoup_obj.find_all('item') 
    for item in story:
        headline = {
            "source": source,
            "pubDate": item.pubDate.text if item.pubDate is not None else 'Unknown',
            "headline": item.title.text,
            "link": item.link.text
        }
        headlines.append(headline)
    return headlines


def save_json(data, filename):
    with open(f'./output/{filename}.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


# ---------------------------------------------------

urls = open('./input/urls.py', 'r')

for u in urls.readlines():
    if '#' not in u:
        source = get_source(u)
        response = get_rss(u)
        data = get_headlines(response, source)
        save_json(data, source)