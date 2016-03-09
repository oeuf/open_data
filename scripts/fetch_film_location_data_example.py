"""Example script for downloading police and crime report info from SF Open Data."""
import argparse
import os
import sys

import yaml

from open_data import grabber


def main():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-s', '--secrets', help='Path to secrets.yaml file containing app token')
    parser.add_argument('-f', '--filename', help='filename for saving data')
    args = parser.parse_args()
    url = 'data.sfgov.org'
    # yitu-d5am is for film location data, from https://data.sfggv.org
    dataset_id = 'yitu-d5am'
    if os.path.isfile(args.secrets):
        with open(args.secrets, 'rb') as f:
            params = yaml.load(f)
        app_token = params['app_token']
    else:
        app_token = None
    client = grabber.get_client(url, app_token)
    # example that writes police data to a CSV
    offset = 0
    data_grabber = grabber.DataGrabber(client, dataset_id, offset, add_header=True)
    data_grabber.to_csv(args.filename)


if __name__ == '__main__':
    sys.exit(main())
