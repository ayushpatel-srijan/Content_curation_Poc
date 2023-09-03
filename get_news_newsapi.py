import pprint
import requests
import json

def get_news_old(topic):
    # Define the endpoint
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': topic,  # query phrase
        'pageSize': 5,  # maximum is 100
        'apiKey': '91729bb51a1e4b89b2b2cf55905510bc'  ,
        # your own API key
    }

    response = requests.get(url, params=parameters)
    response_json = response.json()

    articles = response_json["articles"]
    result = []
    for article in articles:
        content = article["content"]
        description = article["description"]
        result.append({"content": content, "description": description})

    # geting description
    desc = [i['description'] for i in result]
    return desc

######################
from gnews import GNews
import pandas as pd
from newspaper import Article
import newspaper


def get_text(url):
    url_i = newspaper.Article(url="%s" % (url), language='en')
    url_i.download()
    try:
        url_i.parse()
        return url_i.text
    except:
        pass
    return 'unable_to_extract'
 
def get_news(topic):
    google_news = GNews(language='en', country='IN',max_results=10)
    news=pd.DataFrame(google_news.get_news(topic),) #input a topic say wimbeldon
    news['text']=news['url'].apply(get_text) # gets the full article
    #news['images']=news['url'].apply(get_images) # gets the images in the article
    news['news'] = news['description']+ ". "+news['text'].str.replace('\n','')
    print(news.shape)
    news_list = news.news.values
    return news_list

