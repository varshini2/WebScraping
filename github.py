# Data Source: https://github.com/
# Dependencies: BeautifulSoup
import re
import requests
from bs4 import BeautifulSoup


class GithubUser:
    start_url = 'https://github.com/'

    def __init__(self, username):
        self.username = username
        self.url = ''.join([self.start_url, self.username])
        self._page = BeautifulSoup(
            requests.get(self.url).content, 'html.parser'
        )
        self.profile_info = self.get_profile_info()
        self.activity_info = self.get_activity_info()
        self.repos_info = self.get_repos_info()
        self.stars_info = self.get_stars_info()

    def get_profile_info(self):
        return {

            'Username': self.username,

            'Name': self._page.find(
                'span', itemprop='name'
            ).text,

            'Bio': self._page.find(
                'div', class_='user-profile-bio'
            ).text,

            'Followers': self._page.find(
                'a', href='/alisoltanirad?tab=followers'
            ).find('span').text,

            'Following': self._page.find(
                'a', href='/alisoltanirad?tab=following'
            ).find('span').text,

            'URL': self.url,

        }

    def get_activity_info(self):
        last_month = re.sub(
            r'\s+|\n',
            ' ',
            self._page.find(
                'div', class_='TimelineItem-body'
            ).find('summary').text.strip()
        )


        return {
            'Last-Year': re.sub(
                r'\s+|\n',
                ' ',
                self._page.find(
                    'div', class_='js-yearly-contributions'
                ).find('h2').text.strip()
            ),

            'Last-Month': last_month
        }

    def get_repos_info(self):
        page = self._get_tab('repositories')

        repos = list()
        for repo in page.find_all('li', class_='public'):
            repos.append({

                'Title': repo.find(
                    'a', itemprop='name codeRepository'
                ).text.strip(),

                'Description': repo.find(
                    'p', itemprop='description'
                ).text.strip() if repo.find(
                    'p', itemprop='description'
                ).text.strip() is not None else 'None',

                'Language': repo.find(
                    'span', itemprop='programmingLanguage'
                ).text.strip() if repo.find(
                    'span', itemprop='programmingLanguage'
                ) is not None else 'None',
                
                'Updated': repo.find(
                    'relative-time'
                ).text.strip(),

                'Tags': ', '.join(
                    tag.text.strip() for tag in repo.find_all(
                        'a', class_='topic-tag'
                    )
                ) if repo.find_all('a', class_='topic-tag') != [] else 'None',

                'URL': ''.join([
                    self.start_url,
                    repo.find(
                    'a', itemprop='name codeRepository'
                    ).get('href')[1:]
                ]),

            })

        return repos

    def get_stars_info(self):
        page = self._get_tab('stars')

        stars = list()

        for repository in page.find_all('div', class_='py-4'):

            link = repository.find('a')
            text = link.text.split()
            owner, title = text[0], text[-1]

            stars.append({
                'Category': 'Repository',
                'Title': title,
                'Owner': owner,
                'URL': ''.join([self.start_url, link.get('href')[1:]]),
            })

        for topic in page.find_all('article', class_='my-3'):

            link = topic.find('a')

            stars.append({
                'Category': 'Topic',
                'Title': link.find('h1').text,
                'URL': ''.join([self.start_url, link.get('href')[1:]]),
            })

        return stars

    def _get_tab(self, name):
        url = ''.join([self.url, '?tab=', name])
        return BeautifulSoup(
            requests.get(url).content, 'html.parser'
        )


if __name__ == '__main__':
    user = GithubUser('alisoltanirad')

    print('\n\tProfile:\n')
    for key, value in user.profile_info.items():
        print('{key}: {value}'.format(key=key, value=value))

    print('\n\tActivity:\n')
    for key, value in user.activity_info.items():
        print('{key}: {value}'.format(key=key, value=value))

    print('\n\tRepositories:\n')
    for repo in user.repos_info:
        for key, value in repo.items():
            print('{key}: {value}'.format(key=key, value=value))
        print()

    print('\n\tStars:\n')
    for star in user.stars_info:
        for key, value in star.items():
            print('{key}: {value}'.format(key=key, value=value))
        print()
