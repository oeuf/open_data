from gevent import monkey
monkey.patch_all()

import gevent.pool

import itertools
import unicodecsv as csv

import retrying
import sodapy


def get_client(url, app_token):
    return sodapy.Socrata(url, app_token)


@retrying.retry(stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def _get_data(client, dataset_id, offset, limit, order_by=':id'):
    tmp = client.get(dataset_id, offset=offset, limit=limit, order=order_by)
    if len(tmp):
        return tmp


def get_data(client, dataset_id, min_offset=0, max_offset=1000000, limit=50000, pool_size=5):
    offsets = xrange(min_offset, max_offset, limit)
    pool = gevent.pool.Pool(pool_size)
    threads = [pool.spawn(_get_data, client, dataset_id, offset, limit) for offset in offsets]
    pool.join()
    return list(itertools.chain.from_iterable([thread.value for thread in threads if thread.value]))


def to_csv(client, dataset_id, filename, limit=50000):
    offset = 0
    with open(filename, 'wb') as f:
        while True:
            result = _get_data(client, dataset_id, offset, limit)
            if result is None:
                break
            if offset == 0:
                keys = result[0].keys()
                writer = csv.DictWriter(f, keys)
                writer.writeheader()
            writer.writerows(result)
            offset += limit
