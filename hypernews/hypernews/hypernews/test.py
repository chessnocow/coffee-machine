import os
import json
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEWS_JSON_PATH = os.path.join(os.path.dirname(BASE_DIR), 'news.json')

with open(NEWS_JSON_PATH, "r") as json_file:
    news_dict = json.load(json_file)

news_link = "1"

print(news_dict)
for news in news_dict:
    if str(news['link']) == news_link:
        print(news)
