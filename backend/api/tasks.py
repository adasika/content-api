# from __future__ import absolute_import, unicode_literals
from asyncore import write
from random import betavariate
from celery import shared_task, app
from django import test
import pandas as pd
from .models import News
import requests
from bs4 import BeautifulSoup
import json
from datetime import date, timedelta
from celery.schedules import crontab
from djqscsv import write_csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
current_time = date.today()
previous = current_time - timedelta(days=5)


# save function
@shared_task(serializer=json)
def save_function(article_list):
    # logger.info("hello")
    new_count = 0
    #ideally we want to delete conditionally
    News.objects.all().delete()
    print("Delete successful")
    #checking current articles published time
    save_to_csv()
    for article in article_list:
        polarity = sentiment_analyzer(article)
        News.objects.create(
        title = article['title'],
        url = article['url'],
        published = article['published'],
        source = article['source'],
        score = polarity
        )

        new_count += 1
    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')

#save to csv function
@shared_task
def save_to_csv():
    qs = News.objects.all().values()
    with open('nlp.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return print("saved file to csv")

# scraping function
@shared_task
def get_google_news():
    logger.info("Hi")
    article_list = []
    print(current_time)
    url = 'https://newsapi.org/v2/everything?q=JohnnyDepp&from={previous}&to={today}&language=en&sortBy=id&apiKey=89097cab82c34c139bf248bd3990ee7d'.format(previous=previous, today= current_time)
    
    try:
        r = requests.get(url)
        # logger.info(r.request.headers)
        # logger.info(r.content)
        # soup = BeautifulSoup(r.content, "html.parser")
        # logger.debug(r.content)
        my_dict = r.json()
        articles = my_dict['articles']
        # logger.info(articles)
        # print(articles)
        # for each "item" I want, parse it into a list
        for a in articles:
            title = a['title']
            url = a['url']
            published = a['publishedAt']
            description = a['description']
            source = a['source']['name']
            

            # create an "article" object with the data
            article = {
                'title': title,
                'url': url,
                'published': published,
                'description': description,
                'source': source
            }

            article_list.append(article)
        
        print('Finished scraping the articles')

        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


@shared_task
def sentiment_analyzer(article):
    sentiment_check = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment_check.polarity_scores(article['description'])
    print(sentiment_dict)
    polarity = max(sentiment_dict['neg'], sentiment_dict['pos'])
    if sentiment_dict['neg'] == sentiment_dict['pos']:
        return "neutral"
    elif polarity == sentiment_dict['pos']:
        return "positive"
    else:
        return "negative"

