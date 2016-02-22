from gevent import monkey
monkey.patch_all()

import itertools

import gevent.pool
import sodapy


def get_client(url, app_token):
    return sodapy.Socrata(url, app_token)


def _get_data(client, dataset_id, offset, limit, order_by=':id'):
    tmp = client.get(dataset_id, offset=offset, limit=limit, order=order_by)
    if len(tmp):
        return tmp


def get_data(client, dataset_id, min_offset=0, max_offset=1000000, limit=50000, pool_size=20):
    offsets = xrange(min_offset, max_offset, limit)
    pool = gevent.pool.Pool(pool_size)
    threads = [pool.spawn(_get_data, client, dataset_id, offset, limit) for offset in offsets]
    pool.join()
    return list(itertools.chain.from_iterable([thread.value for thread in threads if thread.value]))
