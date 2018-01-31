# -*- coding: utf-8 -*-
'''
common.py
'''
def extract_site(url):
    ''' split out the domain of a url '''
    try:
        parts = url.split('//', 1)
        final = 'http://'+parts[1].split('/', 1)[0]
    except IndexError:
        final = None
    return final

def decision(prb):
    ''' return true with probability '''
    import random
    return random.random() < prb

def pick_from(a_list, by_probaility_dist, skip):
    ''' pick from a list with by a probability distribution '''
    import logging
    import coloredlogs

    import numpy as np

    # Setup logging
    coloredlogs.install()
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    # Remove if url already visited
    list_never_been = [u for u in list(a_list) if u not in skip]

    # If there's nothing left after filtering, start revisiting.
    if len(list_never_been) == 0:
        log.info('Everything is already visited. Revisiting...') 
        return np.random.choice(a_list, 1, p=by_probaility_dist)[0]

    # Otherwise renormalize so it sums to one
    by_probaility_dist = np.array([p for u, p in zip(list_never_been, by_probaility_dist) if u not in skip])
    by_probaility_dist /= by_probaility_dist.sum()

    # And sample from that
    return np.random.choice(list_never_been, 1, p=by_probaility_dist)[0]