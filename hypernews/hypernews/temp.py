import json
import os
import datetime
import time

news_list = []
NEWS_JSON_PATH = '../news.json'
NEWS_JSON_PATH = os.environ.get('NEWS_JSON_PATH') or NEWS_JSON_PATH  # DO NOT MODIFY THIS LINE


def deserialize_news():
    global news_list
    with open(NEWS_JSON_PATH, 'r') as json_file:
        news_list = json.load(json_file)


def date_only(str):
    return str[:10]


def find_last_date(news_lst):
    last_date = time.gmtime(0)
    for news in news_lst:
        if time.strptime(news["created"], '%Y-%m-%d %H:%M:%S') > last_date:
            last_date = time.strptime(date_only(news["created"]), '%Y-%m-%d')
    return f"{last_date.tm_year}-{'0' if last_date.tm_mon < 10 else ''}{last_date.tm_mon}-{'0' if last_date.tm_mday < 10 else ''}{last_date.tm_mday}"


def sort_news(news_lst):
    temp_lst = news_list.copy()
    res_lst = {}
    for _ in news_lst:
        cur_date = find_last_date(temp_lst)
        for cur_news in temp_lst:
            if date_only(cur_news["created"]) == cur_date:
                if cur_date in res_lst:
                    res_lst[cur_date] = res_lst[cur_date].append(cur_news)
                else:
                    res_lst[cur_date] = [cur_news, ]
                #del temp_lst[cur_date]
    return res_lst


deserialize_news()

print(sorted(news_list, key = lambda k: time.strptime(k["created"], '%Y-%m-%d %H:%M:%S'), reverse = True))
