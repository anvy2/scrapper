import pandas as pd
import scrapper

data = pd.read_pickle('symbols.pickle')
symbols = list(data['symbol'])
# symbols = ['AAPL']


def make_search_url(base_url, security):
    return base_url+'/quote/'+security+'?p='+security


fields = ['title', 'body', 'story_date', 'author', 'source']

YahooOptions = {
    'mongoURI': 'sondoins',
    'base_url': 'http://in.finance.yahoo.com',
    'title': {
        'tag': 'h1',
        'options': {
            'data-test-locator': 'headline'
        },
        'single': True
    },
    'body': {
        'tag': 'div',
        'options': {
            'class': 'caas-body'
        }
    },
    'story_date': {
        'tag': 'time'
    },
    'author': {
        'tag': 'div',
        'options': {
            'class': 'caas-attr-meta'
        }
    },
    'source': {
        'tag': 'a',
        'options': {
            'class': 'link rapid-noclick-resp caas-attr-provider-logo'
        },
        'html_property': 'href',
        'is_domain': True
    }
}

mongoURI = "sjdbibs"


YahooFinanceScrapper = scrapper(
    mongoURI, symbols, make_search_url, fields, YahooOptions)
