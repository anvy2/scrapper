from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import string
import threading
import logging
from datetime import date
from extract_info import *
from mongo import Mongo

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/google-chrome-unstable"
driver = webdriver.Chrome(options=options)


def make_search_url(base_url, security):
    return base_url+'/quote/'+security+'?p='+security


def get_html(url):
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    time.sleep(5)
    soup = BeautifulSoup(html, 'lxml')
    return soup


class YahooFinanaceCrawler:
    def __init__(self, symbol, mongoURI):
        self.symbols = symbol
        self.base_url = 'http://in.finance.yahoo.com'
        self.mongo_client = Mongo(mongoURI)

    def fetch_article_links(self, security):
        search_url = make_search_url(self.base_url, security)
        soup = get_html(search_url)
        css = re.compile('.*js-content-viewer.*')
        links = {security: [a.get('href')
                            for a in soup.find_all('a', {'class': css})]}
        return links

    def fetch_articles(self, security):
        links_map = self.fetch_article_links(security)
        cards = []
        for link in links_map:
            url = self.base_url+link
            soup = get_html(url)
            cards = [articles for articles in soup.find_all(
                'div', {'class': 'caas-container'})]
        articles = []

        for card in cards:
            details = {}
            details['title'] = extract_single(
                card, 'h1', 'data-test-locator', 'headline').strip()
            details['body'] = extract_all(
                card, 'div', 'class', 'caas-body').strip()
            details['story_date'] = extract_single(card, 'time').strip()
            details['security'] = security.strip()
            details['current_date'] = date.today()
            details['author'] = extract_single(
                card, 'div', True, 'class', 'caas-attr-meta')
            details['source'] = extract_domain(
                extract_html_property(
                    card, 'href', 'a', 'class', 'link rapid-noclick-resp caas-attr-provider-logo'))
            details['category'] = 'news'
            articles.append(details)
        return articles

    def upload_to_mongo(self, data):
        self.mongo_client.upload(data)

    def start(self):
        for symbol in self.symbols:
            articles = self.fetch_articles(symbol)
            threading.Thread(target=self.upload_to_mongo,
                             args=(articles,)).start()
