from bs4 import BeautifulSoup
import tldextract


def extract_all(data, tag, parent=None, option=None, search_field=None):
    soup = BeautifulSoup(data, 'lxml')
    result = ""
    if parent is not None:
        if option is not None:
            for r in soup.find_all(tag, {option: search_field}):
                result += str(r.previousSibling).strip() + " "
        else:
            for r in soup.find_all(tag):
                result += str(r.previousSibling).strip() + " "
    else:
        if option is not None:
            for r in soup.find_all(tag, {option: search_field}):
                result += str(r.text).strip() + " "
        else:
            for r in soup.find_all(tag):
                result += str(r.text).strip() + " "
    return result


def extract_single(data, tag, parent=None, option=None, search_field=None):
    soup = BeautifulSoup(data, 'lxml')
    if parent is not None:
        if option is not None:
            r = soup.find(tag, {option: search_field})
            result = str(r.previousSibling).strip()
        else:
            r = soup.find(tag)
            result = str(r.previousSibling).strip()
    else:
        if option is not None:
            r = soup.find(tag, {option: search_field})
            result = str(r.text).strip()
        else:
            r = soup.find(tag)
            result = str(r.text).strip()
    return result


def extract_domain(url):
    ext = tldextract.extract(url)
    return ext.domain


def extract_html_property(data, property, tag, option=None, search_body=None):
    soup = BeautifulSoup(data, 'lxml')
    attr = soup.find(tag, {option: {search_body}})
    return attr(property)
