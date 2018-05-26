from model import *


def add_news():
    return "hey"


def get_all_news(l=10, s=10, lang='en', tags=[], fields=[]):
    if tags is not None:
        if len(tags) > 0:
            news = News.objects(tags__in=tags).only(*fields).order_by('created_when').skip(s).limit(l)
        else:
            news = None
    else:
        news = News.objects.order_by('created_when').only(*fields).skip(s).limit(l)
    return news


def get_news(news_id):
    return News.objects(id=news_id).first()


def add_news(news_json):
    news = News(**news_json)
    news.save()
    return {'news_id': str(news.id)}


def update_news(news_id, news_json):
    news = News.objects(id=news_id)
    return news.update(**news_json)

def delete_news(news_id):
    news = News(id=news_id)
    return news.delete()
