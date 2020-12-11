from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import string
import threading
import logging
from datetime import date

import urllib3
import newspaper
from extract_info import *
from mongo import Mongo

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/google-chrome-unstable"
options.headless = True
driver = webdriver.Chrome(options=options)

http = urllib3.PoolManager()


def get_html(url, js=False):
    if js is True:
        driver.get(url)
        html = driver.execute_script('return document.body.innerHTML;')
        time.sleep(3)
        soup = BeautifulSoup(html, 'lxml')
    else:
        article = newspaper.Article(url)
        article.download()
        soup = BeautifulSoup(article.html, 'lxml')
    return soup


class Scrapper:
    def __init__(self, symbols, make_search_url, fields, params):
        self.symbols = symbols
        self.base_url = params['base_url']
        self.make_search_url = params['make_search_url']
        # self.mongo_client = Mongo(params['mongoURI'])
        self.params = params
        self.fields = fields
        self.js = params['js']

    def fetch_article_links(self, security):
        search_url = self.make_search_url(self.base_url, security)
        soup = get_html(search_url, self.js)
        pages = 1
        if self.params['search'].get('pagination') is True:
            filter = self.params['search']['pages']
            if filter.get('custom') is None:
                endpage = extract_html_property(soup, filter['html_property'],
                                                filter['tag'], filter['options'])
                pages = int(endpage)

            else:
                get_pages = self.params['search']['pages']['custom']
                pages = get_pages(soup)
        pages = 1
        links_container = []
        filter = self.params['search']['container']
        for page in range(1, pages + 1):
            soup = get_html(search_url + '/' + str(page), self.js)
            if page == 1:
                soup = get_html(search_url)
            for container in soup.find_all(filter['tag'], filter.get('options')):
                links_container.append(container)
        filter = self.params['search']['links']
        # print(links_container)
        links = []
        for link in links_container:
            for card in link.find_all(filter['tag'], filter['options']):
                links.append(card.get(filter['property']))
        # print(links)
        return links

    def fetch_articles(self, security):
        links = self.fetch_article_links(security)
        cards = []
        filter = self.params['article_container']
        for link in links:
            url = self.base_url + link
            soup = get_html(url, self.js)
            # print(soup)
            # print(soup.find('div', {'class': '_3lvqr clearfix'}))
            if filter.get('single') is not True:
                for t in soup.find_all(filter['tag'], filter.get('options')):
                    if t is not None:
                        cards.append(t)
            else:
                t = soup.find(filter['tag'], filter.get('options'))

                if t is not None:
                    cards.append(t)

        # print(cards)
        articles = []

        for card in cards:
            details = {}
            details['security'] = self.symbols[security]
            details['current_date'] = date.today()
            details['category'] = 'news'
            for field in self.fields:
                result = ""
                if self.params[field].get('single') is not None:
                    if self.params[field].get('html_property') is not None:
                        result = extract_html_property(card, self.params[field].get('html_property'), self.params[field]['tag'],
                                                       self.params[field].get('options'))
                    else:
                        result = extract_single(
                            card, self.params[field]['tag'], self.params[field].get('parent'), self.params[field].get('options'))
                    if self.params[field].get('is_domain') is not None:
                        result = extract_domain(result)
                else:
                    result = extract_all(
                        card, self.params[field]['tag'], self.params[field].get('parent'), self.params[field].get('options'))
                if self.params[field].get('filter') is not None:
                    filter = self.params[field]['filter']
                    result = filter(result)
                if field == 'story_time':
                    result = extract_time(result)
                elif field == 'story_date':
                    result = extract_date(result)
                elif field == 'body':
                    result = result.replace("\xa0", "")
                details[field] = result

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
        for security, symbol in self.symbols.items():
            articles = self.fetch_articles(security)
            print(articles)
            # threading.Thread(target=self.upload_to_mongo,
            #                  args=(articles,)).start()
        driver.quit()
