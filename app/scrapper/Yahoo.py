import scrapper
import map
import re


def make_search_url(base_url, query):
    return base_url+'/quote/'+query+'?p='+query


def filter_author(string):
    t = string.split(',')
    if len(t[0]) > 3:
        return t[0:-4]
    else:
        return None


fields = ['title', 'body', 'story_date', 'author', 'source', 'story_time']

YahooOptions = {
    'upload_to_mongo': True,
    'make_search_url': make_search_url,
    'base_url': 'http://in.finance.yahoo.com',
    'search': {
        'container': {
            'tag': 'li',
            'class': 'js-stream-content Pos(r)'
        },
        'links': {
            'property': 'href',
            'tag': 'a',
            'options': {
                'class': re.compile('.*js-content-viewer.*')
            }
        }
    },
    'article_container': {
        'tag': 'article',
        'options': {
            'class': 'caas-container'
        }
    },
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
        'tag': 'time',
        'single': True
    },
    'story_time': {
        'tag': 'time',
        'single': True
    },
    'author': {
        'tag': 'div',
        'options': {
            'class': 'caas-attr-meta'
        },
        'filter': filter_author
    },
    'source': {
        'tag': 'a',
        'options': {
            'class': 'link rapid-noclick-resp caas-attr-provider-logo'
        },
        'html_property': 'href',
        'is_domain': True,
        'single': True
    },
    'js': True
}


def init(symbols, column, destination):
    symbols = map.get_map(symbols, column)
    YahooFinanceScrapper = scrapper.Scrapper(
        symbols, fields, YahooOptions, destination)
    YahooFinanceScrapper.start()


# symbols = {'AAPL': 'AAPL'}
# YahooFinanceScrapper = scrapper.Scrapper(
#     symbols, make_search_url, fields, YahooOptions)
# YahooFinanceScrapper.start()
