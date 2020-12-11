from bs4 import BeautifulSoup
import tldextract
import validators


def extract_all(soup, tag, parent=None, options):
    # soup = BeautifulSoup(soup, 'lxml')
    result = ""
    if parent is not None:
        if options is not None:
            for r in soup.find_all(tag, options):
                result += str(r.previousSibling) + " "
        else:
            for r in soup.find_all(tag):
                result += str(r.previousSibling) + " "
    else:
        if options is not None:
            for r in soup.find_all(tag, options):
                result += str(r.text) + " "
        else:
            for r in soup.find_all(tag):
                result += str(r.text) + " "
    return result


def extract_single(soup, tag, parent=None, options=None):
    # soup = BeautifulSoup(soup, 'lxml')
    if parent is not None:
        if options is not None:
            r = soup.find(tag, options)
            result = str(r.previousSibling)
        else:
            r = soup.find(tag)
            result = str(r.previousSibling)
    else:
        if options is not None:
            r = soup.find(tag, options)
            result = str(r.text)
        else:
            r = soup.find(tag)
            result = str(r.text)
    return result


def extract_domain(url):
    if(validators.url(url) == False):
        return url

    ext = tldextract.extract(url)
    return ext.domain


def extract_html_property(soup, property, tag, options):
    # soup = BeautifulSoup(soup, 'lxml')
    attr = soup.find(tag, options)
    if(attr is None):
        return ""
    if attr(property) in (None, ''):
        return attr('alt')
    return attr(property)
