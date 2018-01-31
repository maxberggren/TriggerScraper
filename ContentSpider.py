'''
ContentSpider.py
'''

import re as newre
import time

import pandas as pd

from grab.spider import Spider
from common import extract_site
from config import triggerwords


class ContentSpider(Spider):
    '''
    crawling `initial_urls` for how many triggerwords found
    '''

    def __init__(
            self, urls=None, restrict_to=None,
            thread_number=20, network_try_limit=10):

        super(self.__class__, self).__init__(
            thread_number=thread_number,
            network_try_limit=network_try_limit
        )

        self.initial_urls = urls
        self.urls_found = []
        self.start_time = time.time()
        self.restrict_to = restrict_to or ''
        self.data = {}
        self.setup_queue(backend='redis', db=1, port=6379)
        self.run()

    def count_triggers(self, doc):
        ''' see how many times triggerwords are found '''
        text = ''
        for elem in doc.doc("//body"):
            text += ' ' + elem.text().lower()

        return len(
            newre.findall(
                ur'({})(\.|\,|\:|\;|)'.format(
                    '|'.join(triggerwords)
                ),
                text,
                newre.IGNORECASE
            )
        )

    def task_initial(self, grab, task):
        ''' do initially '''
        self.data[task.url] = self.count_triggers(grab)

    def parse(self, trigger_data):
        ''' take data dict and make nice DataFrame '''
        if len(trigger_data) > 0:
            return (
                pd.DataFrame.from_dict(trigger_data, orient='index')
                .rename(columns={0: 'triggers'})
                .reset_index()
                .assign(domain=lambda r: r['index'].apply(extract_site))
                .groupby('domain')
                .agg({
                    'triggers': {
                        'triggered': 'sum', 
                        'n_links': 'count'
                    }, 
                })
                .xs('triggers', axis=1, drop_level=True)
                .reset_index()
                .query('triggered > 0')
            )
        else:
            return pd.DataFrame()

    def shutdown(self):
        self.data = self.parse(self.data)
