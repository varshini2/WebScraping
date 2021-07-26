# Data Source: https://dev.to
# Dependencies: Selenium, BeautifulSoup
import time
import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


class DevBlog:
    start_url = 'https://dev.to'

    def __init__(self):
        self._driver = webdriver.Firefox()
        self._get_page_source()
        self._page = BeautifulSoup(self._driver.page_source, 'lxml')
        self.posts = self._get_posts()
        self.top_tags = self._get_top_tags()

    def _get_posts(self):
        posts = []
        post_elements = self._page.find_all(
            class_='crayons-story__hidden-navigation-link'
        )
        for post_element in post_elements:
            post = {
                'Title': post_element.text.strip(),
                'URL': self.start_url + post_element.get('href'),
            }
            posts.append(post)
        return posts

    def _get_top_tags(self):
        url = self.start_url + '/tags'
        page = BeautifulSoup(requests.get(url).content, 'html.parser')
        tags = []
        tag_elements = page.find_all(class_='tag-card')
        for tag_element in tag_elements:
            tag = {
                'Name': re.sub(r'#', '', tag_element.find('a').text.strip()),
                'URL': self.start_url + tag_element.find('a').get('href'),
                'Posts': tag_element.find(class_='mb-3').text.strip().split()[0],
            }
            tags.append(tag)
        return tags

    def _get_page_source(self):
        self._driver.get(self.start_url)

        SCROLL_PAUSE_TIME = 1
        MAX_WAITING_TIME = 2
        waiting_time = 0
        last_height = self._driver.execute_script(
            'return document.body.scrollHeight'
        )

        while True:
            self._driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);'
            )
            time.sleep(SCROLL_PAUSE_TIME)
            waiting_time += SCROLL_PAUSE_TIME

            current_height = self._driver.execute_script(
                'return document.body.scrollHeight'
            )

            if current_height == last_height:
                break
            elif waiting_time >= MAX_WAITING_TIME:
                break
            last_height = current_height


if __name__ == '__main__':
    dev = DevBlog()

    for post in dev.posts:
        print('\t Title: ', post['Title'])
        print('\t URL: ', post['URL'])
        print()