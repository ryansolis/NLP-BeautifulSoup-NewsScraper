import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse
import time
import psycopg2

# Set up database connection
#This code imports required modules and establishes a connection to a PostgreSQL database using the psycopg2 library.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="&aV83022RMS99"
)
cur = conn.cursor()

#create_table() function creates a table named 'articles' in the PostgreSQL database 
#   with 8 columns: id, title, author, pubdate, content, summary, url, and source.
def create_table():
    # create table
    cur.execute("""CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        title TEXT,
        author TEXT,
        pubdate TEXT,
        content TEXT,
        summary TEXT,
        url TEXT,
        source TEXT)
    """)
    conn.commit()

#get_***links() functions returns a list of URLs for the news articles on the News website homepage.
#It uses the requests library to get the HTML content of the News website homepage and the BeautifulSoup library to 
# parse the HTML content and extract the URLs of news articles.
#The URLs are constructed using the urllib.parse library to join the base URL with the extracted URLs.   
    

def get_foxlinks():
    website = 'https://www.foxnews.com/'
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_container = soup.find_all('div', {'class': 'info'})
    url_part_1 = 'https://www.foxnews.com/'
    url_part_2 = []
    for item in result_container:
        for link in item.find_all('header', {'class':'info-header'}):
            if link.find('a').has_attr('data-omtr-intcmp'):
                url_part_2.append(link.find('a').get('href'))
    url_joined = []
    for link_2 in url_part_2:
        url_joined.append(urllib.parse.urljoin(url_part_1, link_2))
    return url_joined

def get_huffpostlinks():
    website = 'https://www.huffpost.com/'
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_container = soup.find_all('div', {'data-vars-unit-name':'main'})
    url_part_1 = 'https://www.huffpost.com/'
    url_part_2 = []
    for item in result_container:
        for link in item.find_all('div', {'class':'card__headlines'}):
            url_part_2.append(link.find('a').get('href'))
    url_joined = []
    for link_2 in url_part_2:
        url_joined.append(urllib.parse.urljoin(url_part_1, link_2))
    return url_joined

def get_cnnpostlinks():
    website = 'https://edition.cnn.com/world'
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_container = soup.find_all('div', {'class':'card container__item container__item--type-section container_lead-plus-headlines__item container_lead-plus-headlines__item--type-section'})
    url_part_1 = 'https://edition.cnn.com/world'
    url_part_2 = []
    for item in result_container:
        url_part_2.append(item.find('a').get('href'))
    url_joined = []
    for link_2 in url_part_2:
        url_joined.append(urllib.parse.urljoin(url_part_1, link_2))
    return url_joined

#the following summarize_***article functions retrieves the title, published date, author and content of the articles
#then summarizes the content using openai
def summarize_foxarticle(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        title = soup.find('h1', {'class': 'headline'}).get_text()
    except:
        title = ''
    try:
        author = soup.find('div', {'class': 'author-byline'}).findNext('a').get_text()
    except:
        author = ''
    try:
        pubdate = soup.find('div', {'class': 'article-date'}).findNext('time').get_text()
    except:
        pubdate = ''
    try:
        content = soup.find('p', {'class': 'speakable'}).get_text()
    except:
        content = ''
    prompt = "Please summarize the following article:\n" + content
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        timeout=10,
        frequency_penalty=0,
        presence_penalty=0
    )
    summary = response.choices[0].text.strip()
    return (title, author, pubdate, content, summary, link)

def summarize_huffpostarticle(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        title = soup.find('h1', {'class':'headline'}).get_text()
    except:
        title = ''
    try:
        author = soup.find('div', {'class':'entry__byline__author'}).findNext('a').get_text()
    except:
        author = ''
    try:
        pubdate = soup.find('div', {'class':'timestamp'}).findNext('span').get_text()
    except:
        pubdate = 'Apr 3, 2023, 01:23 AM EDT'
    try:
        content = soup.find('div', {'class':'primary-cli cli cli-text'}).get_text()
    except:
        content = ''
    prompt = "Please summarize the following article:\n" + content
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        timeout=10,
        frequency_penalty=0,
        presence_penalty=0
    )
    summary = response.choices[0].text.strip()
    return (title, author, pubdate, content, summary, link)

def summarize_cnnarticle(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        title = soup.find('h1', {'class':'headline__text inline-placeholder'}).get_text()
    except:
        title = ''
    try:
        author = soup.find('span', {'class':'byline__name'}).get_text()
    except:
        author = ''
    try:
        pubdate = soup.find('div', {'class':'timestamp'}).get_text()
    except:
        pubdate = ''
    try:
        content = soup.find('p', {'class':'paragraph inline-placeholder'}).get_text()
    except:
        content = ''
    prompt = "Please summarize the following article:\n" + content
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        timeout=10,
        frequency_penalty=0,
        presence_penalty=0
    )
    summary = response.choices[0].text.strip()
    return (title, author, pubdate, content, summary, link)

#inserts data into the database
def insert_article(article):
    cur.execute("INSERT INTO articles (title, author, pubdate, content, summary, url) VALUES (%s, %s, %s, %s, %s, %s)", article)
    conn.commit()

#queries the database
def get_all_articles():
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles")
    rows = cur.fetchall()
    return rows

#calls the functions
def main():
    summary_cache = {}
    create_table()
    url_joined1 = get_foxlinks() 
    url_joined2 = get_huffpostlinks()
    url_joined3 = get_cnnpostlinks()
    for link in url_joined1:
        article = summarize_foxarticle(link) 
        insert_article(article)
    for link in url_joined2:
        article = summarize_huffpostarticle(link) 
        insert_article(article)
    for link in url_joined3:
        article = summarize_cnnpostarticle(link) 
        insert_article(article)
    rows = get_all_articles()
    #df = pd.DataFrame(rows, columns=['id', 'title', 'author', 'pubdate', 'content', 'summary'])
    #print(df)

#runs main
if __name__ == '__main__':
    # Set up OpenAI API
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    temperature = 0.5
    max_tokens = 1000
    summary_cache = {}
    main()



# In[ ]:




