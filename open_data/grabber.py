import unicodecsv as csv

import sodapy


def get_client(url, app_token):
    """Creates an instance of sodapy.Socrata for interacting with the open data API."""
    return sodapy.Socrata(url, app_token)


def _get_data(client, dataset_id, offset, limit, order_by=':id'):
    """Pulls a subset of data from the specified dataset_id

    Args:
        client: an instance of sodapy.Socrata (see get_client())
        dataset_id: String identifier for dataset. (see https://data.sfgov.org/)
        offset: Int offset parameter for query
        limit: Int number of records to fetch from query (max 50000 per Socrata)
        order_by: sort key for query

    Returns:
        list of API objects
    """

    tmp = client.get(dataset_id, offset=offset, limit=limit, order=order_by)
    if len(tmp):
        return tmp


class DataGrabber(object):
    def __init__(self, client, dataset_id, offset=0, add_header=True):
        """Class to page through API data and write to CSV.

        Args:
            client: an instance of sodapy.Socrata (see get_client())
            dataset_id: String identifier for dataset. (see https://data.sfgov.org/)
            offset: Int offset parameter for query
            add_header: Boolean indicating whether or not to add a header line to outputfil
        """

        self.client = client
        self.dataset_id = dataset_id
        self.offset = offset
        self.add_header = add_header

    def to_csv(self, filename, limit=50000):
        with open(filename, 'a') as f:
            while True:
                result = _get_data(self.client, self.dataset_id, self.offset, limit)
                if result is None:
                    return
                keys = result[0].keys()
                # ugly hacks to deal with inconsistent field names in API data.Sigh.
                if self.dataset_id == 'vw6y-z8j6':  # 311 data
                    keys.extend(['media_url', 'status_notes'])
                elif self.dataset_id == '5cei-gny5':  # vendor data
                    keys.append('constraints_date')
                elif self.dataset_id == 'yitu-d5am':  # vendor data
                    keys.extend(['distributor', 'fun_facts'])
                writer = csv.DictWriter(f, keys)
                if self.add_header:
                    writer.writeheader()
                    self.add_header = False
                writer.writerows(result)
                self.offset += limit
