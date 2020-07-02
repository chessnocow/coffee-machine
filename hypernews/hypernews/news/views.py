from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import HttpResponseRedirect
import json
import time
import datetime

news_list = []


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        #return render(request, 'news/welcome.html')
        return HttpResponseRedirect('/news/')


class ArticleView(View):
    def get(self, request, link, *args, **kwargs):
        article = find_article(link)
        return render(request, 'news/news_page.html', {
            'article': article
        })


class NewsView(View):
    def get(self, request, *args, **kwargs):
        deserialize_news()
        for news in news_list:
            news["created"] = news["created"][:10]
        sorted_news = sorted(news_list, key=lambda k: time.strptime(k["created"], '%Y-%m-%d'), reverse = True)
        sorted_news = [news for news in sorted_news if request.GET.get('q', '') in news['title']]

        return render(request, 'news/news.html', {
            'news': sorted_news,
            'search': request.GET.get('q', '')
        })


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        self.add(request.POST.get('news_text'), request.POST.get('title'))
        return HttpResponseRedirect('/news/')

    def add(self, text, title):
        deserialize_news()

        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            now = datetime.datetime.now()
            created = now.strftime('%Y-%m-%d %H:%M:%S')
            link = now.strftime('%Y%m%d%H%M%S')  # %f
            news_list.append({'created': created, 'text': text, 'title': title, 'link': int(link)})
            json.dump(news_list, json_file)



def deserialize_news():
    global news_list
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        news_list = json.load(json_file)


def find_article(article_id):
    deserialize_news()
    for article in news_list:
        if article.get('link') == int(article_id):
            return article
