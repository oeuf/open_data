"""Example script for downloading police and crime report info from SF Open Data."""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import yaml

from open_data import grabber


def write_data(data_dict, filename):
    pd.DataFrame.from_dict(data_dict).to_csv(filename, index=False, encoding='utf-8')


def clean_311(df):
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


def main():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-s', '--secrets', help='Path to secrets.yaml file')
    args = parser.parse_args()
    url = 'data.sfgov.org'
    crime_id = 'gxxq-x39z'
    police_id = 'tmnf-yvry'
    if os.path.isfile(args.secrets):
        with open(args.secrets, 'rb') as f:
            params = yaml.load(f)
        app_token = params['app_token']
    else:
        app_token = None
    client = grabber.get_client(url, app_token)
    #--example that writes eviction data to a CSV
    grabber.to_csv(client, crime_id, 'crime_data.csv')
    grabber.to_csv(client, police_id, 'police_data.csv')


if __name__ == '__main__':
    sys.exit(main())
