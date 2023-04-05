# NLP-BeautifulSoup-NewsScraper

This code performs web scraping of news websites (Fox News, HuffPost, and CNN) to extract URLs of their latest articles, 
and then uses OpenAI's GPT-3 language model to generate summaries of each article. The summaries, along with other relevant information 
(such as title, author, and publication date), are then stored in a PostgreSQL database.

The code starts by importing the required libraries - openai, BeautifulSoup, requests, pandas, urllib.parse, time, and psycopg2. 
It then sets up a connection to the PostgreSQL database, creates a table (if it doesn't exist already) to store the extracted article information, 
and defines functions to extract article URLs from the news websites and to generate article summaries using GPT-3.

The create_table() function creates a table called "articles" in the database with columns for article ID (automatically generated), 
title, author, publication date, article content, summary, URL, and source. This function is called only once, to set up the table.

The get_foxlinks(), get_huffpostlinks(), and get_cnnpostlinks() functions extract URLs of the latest articles from Fox News, HuffPost, 
and CNN, respectively. These functions use requests and BeautifulSoup to scrape the news websites and extract URLs of the articles. 
The URLs are then joined with the base URL of the news website using urllib.parse.

The summarize_foxarticle(), summarize_huffpostarticle(), and summarize_cnnarticle() functions generate summaries of the articles using 
OpenAI's GPT-3 language model. These functions use requests and BeautifulSoup to scrape the article pages and extract the article title, 
author, publication date, and content. They then use the GPT-3 language model to generate a summary of the article content. 
The summary, along with other relevant information, is returned as a tuple.

The extracted information (title, author, publication date, content, summary, URL, and source) is then inserted into the "articles" table 
in the PostgreSQL database using psycopg2.


# How to run

Note: it can only run in localhost for the meantime

Prerequisites: 
install postgreSQL, flask, psycopg2 and npm

1. open postgreSQL
2. call python postgres-sertup-v2.py
3. run the flask app by calling python server.py
4. run the react app by calling npm start
