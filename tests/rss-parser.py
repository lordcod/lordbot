import time
from pprint import pprint

import feedparser
from rss_parser import RSSParser
from requests import get

rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + \
    "UCPCTEN8OWHdJGxfMggbyGGg"
# rss_url = "https://rssexport.rbc.ru/rbcnews/news/20/full.rss"
# rss_url = "https://habr.com/ru/rss/news/?fl=ru"
print(rss_url)
response = get(rss_url)

rss = feedparser.parse(response.text)

pprint(rss.feed)


# habr_title = []

# while True:
#     if len(habr_title) >= 20:
#         habr_title = []
#     rss_url = "https://habr.com/ru/rss/news/?fl=ru"
#     xml = get(rss_url)

#     print(xml.content.decode())

#     feed = RSSParser.parse(xml.content)

#     for item in reversed(feed.feed):
#         if item.title not in habr_title:
#             habr_title.append(item.title)
#             print(f'{item.publish_date}\n{item.title, item.link}\n')
#     time.sleep(1800)
