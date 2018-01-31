'''
LinkSpider.py
'''

import random
import time

from grab.error import DataNotFound
from grab.spider import Spider, Task

from config import blacklist


class LinkSpider(Spider):
    '''
    crawling `initial_urls` for a good sample of its sub-links
    '''

    def __init__(
            self, urls=None, scale=1.0,
            thread_number=20, network_try_limit=10):

        super(self.__class__, self).__init__(
            thread_number=thread_number,
            network_try_limit=network_try_limit
        )

        self.initial_urls = urls
        self.scale = scale
        self.urls_found = []
        self.start_time = time.time()
        self.setup_queue(backend='redis', db=1, port=6379)
        self.run()

    def ok_url(self, url):
        ''' check if an url is all good '''
        if not any(e in url for e in blacklist):
            return True

    def get_all_links(self, grab):
        '''' find all links on page '''
        urls = []
        for elem in grab.doc('//a'):
            try:
                url = grab.make_url_absolute(elem.attr('href'))
                if self.ok_url(url):
                    urls.append(url)
            except DataNotFound:
                pass      
        return urls

    def random_sample(self, a_list, k):
        ''' get k random from list '''
        if len(a_list) < k:
            return a_list
        else:
            return random.sample(a_list, k)

    def task_initial(self, grab, task):
        ''' get all links and sample k '''
        urls = self.get_all_links(grab)
        for url in self.random_sample(urls, 30*self.scale):
            self.urls_found += [url]
            yield Task('lvl1', url=url)

    def shutdown(self):
        self.urls_found = list(set(self.urls_found))

    def task_lvl1(self, grab, task):
        ''' happends on every link found on level 1 '''
        urls = self.get_all_links(grab)
        for url in self.random_sample(urls, 10*self.scale):
            self.urls_found += [url]
