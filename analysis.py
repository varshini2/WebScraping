# Dependencies: BeautifulSoup
import re
from collections import Counter
import requests
from bs4 import BeautifulSoup


def get_words(page):
    assert type(page) == BeautifulSoup

    def split(text):
        return re.findall(r"\w+(?:['.]\w+)*", text.lower())

    words = []
    for i in page.find_all():
        words += split(i.text)

    return words


def most_frequent_words(page, n=1):
    assert type(page) == BeautifulSoup
    assert type(n) == int

    dist = Counter()

    for word in get_words(page):
        if word in dist:
            dist[word] += 1
        else:
            dist[word] = 1

    return dist.most_common(n)


if __name__ == '__main__':
    bs = BeautifulSoup(
        requests.get('https://w3schools.com').content, 'html.parser'
    )
    for i in most_frequent_words(bs, 20):
        print(i)