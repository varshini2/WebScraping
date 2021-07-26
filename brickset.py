# Data Source: https://brickset.com/
# Dependencies: BeautifulSoup
import requests
from bs4 import BeautifulSoup

class Brickset:
    start_url = 'https://brickset.com/'

    def __init__(self):
        self.sets = self._get_sets()

    def _get_sets(self):
        sets_url = ''.join([self.start_url, 'sets/year-2020/'])
        sets_pages = [
            BeautifulSoup(requests.get(
                ''.join([sets_url, 'page-', str(page)])
            ).content, 'html.parser')
            for page in range(1, 35)
        ]

        set_divs = list()
        for page in sets_pages:
            set_divs += page.find_all(class_='set')

        sets = list()

        for div in set_divs:
            try:
                sets.append({
                    'Title': div.find('h1').text,
                    'Price': div.find(
                        'dt', text='RRP'
                    ).findNext('dd').text.split('|')[0].strip(),
                    'Pieces': div.find('dt', text='Pieces').findNext('dd').text,
                    'Picture-URL': div.find('a').get('href'),
                })
            except AttributeError:
                pass

        return sets


if __name__ == '__main__':
    brickset = Brickset()
    print(len(brickset.sets))
    for set in brickset.sets:
        for key, value in set.items():
            print('{key}: {value}'.format(key=key, value=value))
        print()
