from bs4 import BeautifulSoup
import tldextract
import validators
import dateutil.parser as dparser


def decod(string):
    return str(string)


def extract_all(soup, tag, parent=None, options=None):
    # soup = BeautifulSoup(soup, 'lxml')
    result = ""
    if parent is not None:
        if options is not None:
            for r in soup.find_all(tag, options):
                result += decod(r.previousSibling) + " "
        else:
            for r in soup.find_all(tag):
                result += decod(r.previousSibling) + " "
    else:
        if options is not None:
            for r in soup.find_all(tag, options):
                result += decod(r.text) + " "
        else:
            for r in soup.find_all(tag):
                result += decod(r.text) + " "
    return result


def extract_single(soup, tag, parent=None, options=None):
    # soup = BeautifulSoup(soup, 'lxml')
    if parent is not None:
        if options is not None:
            r = soup.find(tag, options)
            result = decod(r.previousSibling)
        else:
            r = soup.find(tag)
            result = decod(r.previousSibling)
    else:
        if options is not None:
            r = soup.find(tag, options)
            result = decod(r.text)
        else:
            r = soup.find(tag)
            result = decod(r.text)
    return result


def extract_domain(url):
    if(validators.url(url) == False):
        return url

    ext = tldextract.extract(url)
    return ext.domain


def extract_html_property(soup, property, tag, options):
    # soup = BeautifulSoup(soup, 'lxml')
    attr = soup.find(tag, options)
    if attr is None:
        return ""
    if attr.get(property) in (None, ''):
        return attr.get('alt')
    return attr.get(property)


def extract_date(string):
    t = dparser.parse(string, fuzzy=True)
    return t.date()


def extract_time(string):
    t = dparser.parse(string, fuzzy=True)
    return t.time()
