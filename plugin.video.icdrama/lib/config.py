import os.path
from urlparse import urljoin
from lib.common import diritem, action_url, profile_dir

base_url = 'http://icdrama.se'
domains = ['icdrama.se', 'icdrama.to']
cache_file = os.path.join(profile_dir, 'cache.pickle')
store_file = os.path.join(profile_dir, 'store.pickle')

# the trailing forward slashes are necessary
# without it, page urls will be wrong (icdrama bug)
search_url = urljoin(base_url, '/search/%s/')
index_items = [
    diritem(33006, action_url('shows', url=urljoin(base_url, '/korean-drama/'))),
    diritem(33007, action_url('shows', url=urljoin(base_url, '/korean-show/'))),
    diritem(33009, action_url('shows', url=urljoin(base_url, '/movies/'))),
    diritem(33018, action_url('shows', url=urljoin(base_url, '/genre/25-animation.html'))),
    diritem(33010, action_url('search'))
]
