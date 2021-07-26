# Data Source: https://w3schools.com
# Dependencies: BeautifulSoup
import requests
from bs4 import BeautifulSoup


class W3Schools:
    start_url = 'https://w3schools.com'

    def __init__(self):
        self._page = BeautifulSoup(
            requests.get(self.start_url).content, 'html.parser'
        )
        self.tutorials = self._get_nav_links('tutorials')
        self.references = self._get_nav_links('references')
        self.examples = self._get_nav_links('examples')
        self.exercises = self._get_nav_links('exercises')

    def _get_nav_links(self, category):
        links = []
        nav = self._page.find(id=('nav_' + category))
        elements = nav.find_all('a')
        for element in elements:
            link = {
                'Title': element.text.strip(),
                'URL': self.start_url + element.get('href')
            }
            links.append(link)
        return links


if __name__ == '__main__':

    w3 = W3Schools()

    for tutorial in w3.tutorials:
        print('\t Title: ', tutorial['Title'])
        print('\t URL: ', tutorial['URL'])
        print()
