import pandas as pd


def clean_311(df):
    """Use to clean up 311 call data from SF Open data"""
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

