# Data Source: https://instagram.com
# Dependencies: BeautifulSoup
import requests
import re
import json
from bs4 import BeautifulSoup


class InstagramUser:
    start_url = 'https://instagram.com/'

    def __init__(self, username):
        self.username = username
        self.url = ''.join([self.start_url, self.username])
        self._page = BeautifulSoup(
            requests.get(self.url).content, 'html.parser'
        )
        self._profile = self._get_profile_data()
        self._posts = self._profile['edge_owner_to_timeline_media']['edges']

    def get_info(self):
        user_information = {
            'Name': self._profile['full_name'],
            'Username': self.username,
            'Page-URL': self.url,
            'Profile-Picture-URL': self._profile['profile_pic_url_hd'],
            'Biography': self._profile['biography'],
            'Website': self._profile['external_url'],
            'Followers': self._profile['edge_followed_by']['count'],
            'Following': self._profile['edge_follow']['count'],
            'Is-Private': self._profile['is_private'],
            'Is_Verified': self._profile['is_verified'],
            'Is-Business-Account': self._profile['is_business_account'],
            'Page-Category': self._profile['category_enum'],
            'Is-Joined-Recently': self._profile['is_joined_recently'],
        }
        return user_information

    def get_recent_posts_info(self):
        recent_posts_info = []
        for post in self._posts:
            post_data = post['node']
            post_info = {
                'Display-URL': post_data['display_url'],
                'Is-Video': post_data['is_video'],
                'Likes': post_data['edge_liked_by']['count'],
                'Comments': post_data['edge_media_to_comment']['count'],
            }
            recent_posts_info.append(post_info)
        return recent_posts_info

    def get_engagement_rate(self):
        interactions_sum = 0
        for post in self._posts:
            interactions_sum += post['node']['edge_liked_by']['count'] + \
                                post['node']['edge_media_to_comment']['count']
        engagement_rate = interactions_sum / \
                          (self._profile['edge_followed_by']['count'] *
                           len(self._posts))
        return engagement_rate

    def _get_profile_data(self):
        shared_data = self._page.find(
            'script', text=re.compile('window\._sharedData')
        ).string.partition('=')[-1].strip(' ;')

        return json.loads(shared_data)['entry_data']['ProfilePage'][0]['graphql']['user']


class InstagramTag:
    start_url = 'https://instagram.com/explore/tags/'

    def __init__(self, name):
        self.name = name
        self.url = ''.join([self.start_url, self.name])
        self._page = BeautifulSoup(
            requests.get(self.url).content, 'html.parser'
        )
    

if __name__ == '__main__':
    user = InstagramUser('highcod3r')
    for key, value in user.get_info().items():
        print('{key:>25}:  {value}'.format(key=key, value=value))
