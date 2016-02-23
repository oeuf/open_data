import os

import numpy as np
import pandas as pd
import yaml

from socrata import grabber


def writeData(data_dict, filename):
    pd.DataFrame.from_dict(data_dict).to_csv(filename, index=False, encoding='utf-8')


def clean311(df):
    """Use to clean up 311 call data """
    df['opened'] = pd.to_datetime(df['opened'])
    df['closed'] = pd.to_datetime(df['closed'])
    # exclude incidents where opened occurs after closed
    df = df[df['closed'] > df['opened']]
    # Remove duplicates.
    df = df.sort_index(by=['case_id', 'opened'])
    df = df.drop_duplicates(subset=['case_id'], keep='last')
    # Measure lag as # of days
    df['lag'] = (df['closed'] - df['opened']) / np.timedelta64(1, 'D')
    return df


if __name__ == '__main__':
    url = 'data.sfgov.org'
    budgets_id = 'xdgd-c79v'
    spending_id = 'bpnb-jwfb'
    vendor_id = 'p5r5-fd7g'
    voucher_id = 'n9pm-xkyq'
    eviction_id = '5cei-gny5'
    whats_the_311_id = 'vw6y-z8j6'
    crime_id = 'gxxq-x39z'
    pd_id = 'tmnf-yvry'
    secrets_file = '../secrets.yaml'
    if os.path.isfile(secrets_file):
        with open(secrets_file, 'rb') as f:
            params = yaml.load(f)
        app_token = params['app_token']
    else:
        app_token = None
    client = grabber.get_client(url, app_token)
    #--example that writes eviction data to a CSV
    eviction_data = writeData(grabber.page_through_data(client, eviction_id), 'eviction_data.csv')
    df = clean311(pd.read_csv('311_data.csv'))
