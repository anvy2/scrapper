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
options.headless = True
driver = webdriver.Chrome(options=options)


def get_html(url):
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    time.sleep(3)
    soup = BeautifulSoup(html, 'lxml')
    return soup


class Scrapper:
    def __init__(self, mongoURI, symbol, make_search_url, fields, params):
        self.symbols = symbol
        self.base_url = params['base_url']
        self.make_search_url = make_search_url
        # self.mongo_client = Mongo(params['mongoURI'])
        self.params = params
        self.fields = fields

    def fetch_article_links(self, security):
        search_url = self.make_search_url(self.base_url, security)
        soup = get_html(search_url)
        # css = re.compile('.*js-content-viewer.*')
        links = [a.get(self.params['search']['property'])
                 for a in soup.find_all(self.params['search']['tag'], self.params['search']['options'])]
        # print(links)
        return links

    def fetch_articles(self, security):
        links = self.fetch_article_links(security)
        cards = []
        for link in links:
            url = self.base_url+link
            soup = get_html(url)
            # print(soup)
            for t in soup.find_all(self.params['article_container']['tag'], self.params['article_container'].get('options')):
                cards.append(t)

        # print(cards)
        articles = []

        for card in cards:
            details = {}
            details['security'] = security
            details['current_date'] = date.today()
            details['category'] = 'news'
            for field in self.fields:
                result = ""
                if self.params[field].get('single') is not None:
                    if self.params[field].get('html_property') is not None:
                        result = extract_html_property(card, self.params[field].get('html_property'), self.params[field]['tag'],
                                                       self.params[field].get('options'))
                        if self.params[field].get('is_domain') is not None:
                            result = extract_domain(result)
                    else:
                        result = extract_single(
                            card, self.params[field]['tag'], self.params[field].get('parent'), self.params[field].get('options'))
                else:
                    result = extract_all(
                        card, self.params[field]['tag'], self.params[field].get('parent'), self.params[field].get('options'))
                details[field] = result
            details['body'] = details['body'].replace("\xa0", "")
            articles.append(details)

        # for card in cards:
        #     details = {}
        #     details['title'] = extract_single(
        #         card, self.params['title']['tag'], None, self.params['title']['options'])
        #     body = extract_all(
        #         card, self.params['body']['tag'], None, 'class', 'caas-body')
        #     details['body'] = body.replace("\xa0", "")
        #     details['story_date'] = extract_single(card, 'time')
        #     details['security'] = security
        #     details['current_date'] = date.today()
        #     details['author'] = extract_single(
        #         card, 'div', None, 'class', 'caas-attr-meta')
        #     details['source'] = extract_domain(
        #         extract_html_property(
        #             card, 'href', 'a', 'class', 'link rapid-noclick-resp caas-attr-provider-logo'))
        #     details['category'] = 'news'
        #     articles.append(details)
        #     print(articles)
        return articles

    def upload_to_mongo(self, data):
        self.mongo_client.upload(data)

    def start(self):
        for symbol in self.symbols:
            articles = self.fetch_articles(symbol)
            print(articles)
            # threading.Thread(target=self.upload_to_mongo,
            #                  args=(articles,)).start()
        driver.quit()
