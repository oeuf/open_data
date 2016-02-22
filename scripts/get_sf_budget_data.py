import os
import yaml

from socrata import grabber


if __name__ == '__main__':
    url = 'data.sfgov.org'
    budgets_id = 'xdgd-c79v'
    secrets_file = '../secrets.yaml'
    if os.path.isfile(secrets_file):
        with open(secrets_file, 'rb') as f:
            params = yaml.load(f)
        app_token = params['app_token']
    else:
        app_token = None
    client = grabber.get_client(url, app_token)
    budget_data = grabber.get_data(client, budgets_id)
