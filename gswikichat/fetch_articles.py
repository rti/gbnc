import os
import re
import json
import requests
import configparser

from bs4 import BeautifulSoup

from .logger import get_logger
logger = get_logger(__name__)

WIKI_USER = os.environ.get('WIKI_USER')
WIKI_PW = os.environ.get('WIKI_PW')

HTML_FILTERS  = {
    'div': ['navbox','navbox-styles','spoken-wikipedia', 'noprint', 'hatnote', 'rt-tooltip', 'reflist'],
    'span': ['mw-ext-cite-error'],
    'table': ['noprint','ombox'],
    'ol': ['breadcrumb-nav-container', 'references'],
    'sup': ['reference']
}
SECTION_FILTERS = [ 'Siehe auch', 'See also', 'Weblinks', 'Anmerkungen', 'Notes' ]
REGEX_FILTERS = {
    'p': '→.*ersion'
}

def filterHtml(soup):
    for figure in soup.find_all('figure'):
        figure.decompose()

    for tag, classes in HTML_FILTERS.items():
        for className in classes:
            for div in soup.find_all(tag, {'class': className}):
                div.decompose()

    for tag, regex in REGEX_FILTERS.items():
        for element in soup.find_all(tag):
            if(re.search(regex, str(element)) != None):
                element.decompose()

    return soup

def fetchFromWiki(url, titles, loginRequired):
    if(loginRequired == True):
        session = loginToWiki(url)
    else:
        session = requests.Session()

    articles = {}
    for title in titles:
        sections = fetchSections(url, title, session.cookies)
        print("fetching {} sections for article {}".format(len(sections), title), file=sys.stderr)
        for section in [ { 'index' : 0, 'line': 'Intro', 'linkAnchor' : '', 'anchor' : '' } ] + sections :
            if section['index'] == '' or section['line'] in SECTION_FILTERS:
                continue

            query = {
                'action': 'parse',
                'page': title,
                'format': 'json',
                'prop':'text',
                'disabletoc': True,
                'disablelimitreport': True,
                'disableeditsection': True,
                'section': section['index']
            }
            section_html = requests.get(url,params=query,cookies=session.cookies).json()['parse']['text']['*']
            section_soup = BeautifulSoup(section_html, 'lxml')
            articles[title + '#' + section['anchor']] = filterHtml(section_soup).get_text()

    return articles


def fetchSections(url, title, cookies=None):
    query = {
        'action':'parse',
        'page':title,
        'format':'json',
        'prop':'sections'
    }
    sectionsResponse = requests.get(url,params=query, cookies=cookies)
    toplevelSections = [ section for section in sectionsResponse.json()['parse']['sections'] if section['toclevel'] == 1 ]
    return toplevelSections

def loginToWiki(url):
    session = requests.Session()

    tokenQuery = { 'action': 'query', 'meta': 'tokens', 'type': 'login', 'format': 'json' }
    token = session.get(url, params=tokenQuery).json()['query']['tokens']['logintoken']
    loginData = {
        'lgname': WIKI_USER,
        'lgpassword': WIKI_PW,
        'lgtoken': token,
        'action': 'login',
        'format': 'json'
    }
    response = session.post(url, data=loginData, headers={ 'Content-Type' : 'application/x-www-form-urlencoded' })
    #TODO: error handling in case of login failure
    return session

def fetch_articles(toc):
    articles = []
    for wiki in toc:
        url = wiki['host'] + wiki['api_path']
        wikiArticles = fetchFromWiki(url, wiki['titles'], wiki['login'])

        articles.append( {
            'wiki': wiki['name'],
            'url': wiki['host'],
            'lang': wiki['lang'],
            'articles': wikiArticles
            } )

    return articles

def transform_articles(articles):
    output = {}
    for wiki in articles:
        url = wiki.get("url") + "/wiki/"
        articles = wiki.get("articles")
        for name, content in articles.items():
            output[url+name] = content
    return output

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        file = sys.argv[1]
        with open(file) as f:
            data = json.load(f)

        articles = fetch_articles(data)
        print(json.dumps(transform_articles(articles), indent=4))

    else:
        logger.error(
            """Provide JSON file with the following structure as first parameter
    [
        {
            "name": "Name of the wiki",
            "host": "https://somewiki.org",
            "api_path": "/w/api.php",
            "lang": "en",
            "login": false,
            "titles" : [
                "Namespace:Page1",
                "Namespace:Page2"
            ]
        },
        {
            "name": "Name of the another wiki",
            "host": "https://someotherwiki.org",
            "api_path": "/w/api.php",
            "lang": "de",
            "login": false,
            "titles" : [
                "Namespace:SeiteEins",
                "Namespace:SeiteZwei"
            ]
        }
    ]
            """
        )
        sys.exit(1)
