import json
from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup

# ---------------------------------------------------

def create_filename(url):
    url = urlparse(url).netloc
    source = url.split('.')[1]
    return source


def get_rss(url):
    header= {'User-Agent': 'Mozilla/5.0'}
    request = urllib.request.Request(url=url, headers=header)
    response = urllib.request.urlopen(request)
    bsoup = BeautifulSoup(response, 'xml')
    return bsoup


def get_headlines(bsoup_obj):
    headlines = []
    story = bsoup_obj.find_all('item')
    for item in story:
        headline = {
            "headline": item.title.text,
            "link": item.link.text
        }
        headlines.append(headline)
    return headlines


def save_json(data, filename):
    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


# ---------------------------------------------------

urls = [
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'https://news.ycombinator.com/rss',
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'https://www.latimes.com/california/rss2.0.xml',
    'https://www.chicagotribune.com/arcio/rss/category/news/breaking/',
    'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
    'https://www.aljazeera.com/xml/rss/all.xml',
    'https://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml',
    'http://feeds.foxnews.com/foxnews/latest',
    'https://feeds.washingtonpost.com/rss/local',
    'http://feeds.marketwatch.com/marketwatch/topstories/',
    'https://www.theguardian.com/world/rss'
    # 'https://www.seattletimes.com/seattle-news/feed/'
]


for u in urls:
    file_name = create_filename(u)
    response = get_rss(u)
    data = get_headlines(response)
    save_json(data, file_name)