import scrapper
import re
import map
import dateutil.parser as dparser


def make_search_url(base_url, query):
    return base_url + '/topic/' + query


fields = ['title', 'body', 'story_date', 'source', 'story_time', 'author']


def filter_author(string):
    t = string.split('|')
    if len(t) == 3:
        return t[0]
    else:
        return None


def filter_source(string):
    t = string.split('|')
    if len(t) == 3:
        return t[1]
    elif len(t) == 2:
        return t[0]
    else:
        return None


TOIOptions = {
    'upload_to_mongo': True,
    'base_url': 'https://timesofindia.indiatimes.com',
    'make_search_url': make_search_url,
    'search': {
        'container': {
            'tag': 'div',
            'options': {
                'class': 'content'
            }
        },
        'links': {
            'tag': 'a',
            'property': 'href',
            'options': {
                'target': '_blank'
            }
        },
        'pagination': True,
        'pages': {
            'tag': 'div',
            'options': {
                'class': 'pagination'
            },
            'html_property': 'endpage'
        }
    },
    'article_container': {
        'tag': 'div',
        'options': {
            'class': '_3lvqr clearfix'
        },
        'single': True
    },
    'title': {
        'tag': 'h1',
        'options': {
            'class': '_23498'
        }
    },
    'body': {
        'tag': 'div',
        'options': {
            'class': 'ga-headlines'
        }
    },
    'source': {
        'tag': 'div',
        'options': {
            'class': '_3Mkg- byline'
        },
        'filter': filter_source
    },
    'story_date': {
        'tag': 'div',
        'options': {
            'class': '_3Mkg- byline'
        },
    },
    'story_time': {
        'tag': 'div',
        'options': {
            'class': '_3Mkg- byline'
        },
    },
    'author': {
        'tag': 'div',
        'options': {
            'class': '_3Mkg- byline'
        },
        'filter': filter_author
    },
    'js': False
}


def init(symbols, column, destination):
    symbols = map.get_map(symbols, column)
    symbols = {'Apple': 'AAPL'}
    TOIScrapper = scrapper.Scrapper(
        symbols, fields, TOIOptions, destination)
    TOIScrapper.start()


# symbols = {'Apple': 'AAPL'}
# TOIScrapper = scrapper.Scrapper(symbols, make_search_url, fields, TOIOptions)
# TOIScrapper.start()
