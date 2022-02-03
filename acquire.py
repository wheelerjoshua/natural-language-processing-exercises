import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


####### get codeup blog posts
def get_blog_articles(link):
    response = requests.get(link, headers={'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    title = soup.title.string
    content = soup.select('.entry-content')[0].text
    return {
        'title': title, 'content': content
    }


####### get codeup blog posts df
def acquire_blogs():
    if os.path.isfile('codeup_blogs.csv'):
        df = pd.read_csv('codeup_blogs.csv')
    else:
        response = requests.get('https://codeup.com/blog/', headers={'user-agent': 'Codeup DS Hopper'})
        soup = BeautifulSoup(response.text)
        urls = []
        for link in soup.find_all('a', class_='more-link'):
            urls.append(link.get('href'))
        df = pd.DataFrame([get_blog_articles(link) for link in urls])
        df.to_csv('codeup_blogs.csv', index=False)
    return df


####### get inshorts articles
def get_news_info(link):
    response = requests.get(link, headers={'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    articles = soup.find_all('div',class_='news-card')
    titles = []
    authors = []
    contents = []
    for article in articles:
        # title
        titles.append(article.find('span',itemprop='headline').text)
        # author  
        authors.append(article.find('span',class_='author').text)
        # content
        contents.append(article.find('div',itemprop='articleBody').text)
    return pd.DataFrame({'title':titles,'author':authors,'content':contents,'category':link[29:]})


####### combine inshorts articles to one dataframe
def acquire_news():
    if os.path.isfile('inshorts_articles.csv'):
        df = pd.read_csv('inshorts_articles.csv')
    else:
        links = ['https://inshorts.com/en/read/business','https://inshorts.com/en/read/sports','https://inshorts.com/en/read/entertainment','https://inshorts.com/en/read/technology']
        business, sports, entertainment, tech = [get_news_info(link) for link in links]
        df = business.append(sports).append(entertainment).append(tech)
        df.to_csv('inshorts_articles.csv', index=False)
    return df
