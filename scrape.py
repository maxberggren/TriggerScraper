# -*- coding: utf-8 -*-

import logging
import coloredlogs

import pandas as pd

from common import extract_site, pick_from
from config import seed_url, scale
from ContentSpider import ContentSpider
from LinkSpider import LinkSpider

# Setup logging
coloredlogs.install()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

url = seed_url
been_at_already = []
df = pd.DataFrame()

while True:

    log.info('Going to: %s', url)

    # Map out site by sampling a good chunk of its external urls
    ext_url_sample = LinkSpider([url], scale=scale)
    log.info('%s urls found', len(ext_url_sample.urls_found))
    log.debug('Been at: %s', been_at_already)

    # Take a look at those urls for trigger words
    found_triggers = ContentSpider(ext_url_sample.urls_found)

    df = (
        df
        # Add latest scrape data
        .append(found_triggers.data)
        .groupby('domain')
        .agg({
            'triggered': 'sum', 
            'n_links': 'sum',
        })
        .reset_index()
        # Recalculate ratios with latest data
        .assign(
            ratio=lambda r: (1+r['triggered']
                / r['n_links'].astype(float)
            )
        )
        # Turn ratios to prob to be picked
        .pipe(
            lambda d: d.assign(
                prob=lambda r: r['ratio']
                / r['ratio'].sum()
            )
        )
        .sort_values('prob', ascending=False)
    )

    been_at_already.append(url)

    # A finding is only saved if it's been properly visited
    # i.e. more than X links have been processed.
    current_findings = (
        df
        .query('n_links >= 10')
        .head(30)
        [['domain', 'ratio', 'triggered', 'n_links']]
    )

    log.info('Current top candidates for trigger sites: \n\n%s\n' % current_findings)

    # Keep current findings at file
    current_findings.to_csv('current_findings.csv')

    # Sample next url to visit from trigger sites
    url = extract_site(
        pick_from(
            df.domain.values, 
            by_probaility_dist=df.prob.values,
            skip=been_at_already)
    )
    # Cleanup
    del ext_url_sample
    del found_triggers
