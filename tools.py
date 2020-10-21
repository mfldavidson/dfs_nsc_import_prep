from collections import OrderedDict

import pandas as pd
import numpy as np

def extract_record(d):
    '''
    Given an OrderedDict, extract the records and return a list of attributes and a list of columns.
    '''
    record = []
    cols = []
    for var in d:
        if var not in ['attributes', 'url']:  # Skip the unnecessary attributes and url data
            subitem = d.get(var)
            if type(subitem) == OrderedDict:
                for subvar in subitem:
                    if subvar not in ['attributes', 'url']:
                        record.append(subitem.get(subvar))
                        cols.append(f'{var} {subvar}')
            else:
                record.append((d.get(var)))
                cols.append(var)
    return record, cols

def salesforce_to_dataframe(response):
    '''
    Given an ordered dict returned from the Salesforce API, return a pandas data frame with the data.
    '''
    arr = []
    for item in response.get('records'): # Build a list containing the data for this individual record
        record, cols = extract_record(item)
        arr.append(record) # Append the list to the arr list
    # vars = response.get('records')[0].keys() # Get the keys for column names
    # vars = list(vars)
    # vars.remove('attributes')
    df = pd.DataFrame.from_records(arr, columns=cols)
    return df

def year_to_period(date):
    '''
    Given a date, return Fall, Winter, Summer, or NaN based on the month.
    Used to determine term/period of enrollment based on Enrollment Begin.
    NaN will be true for any rows that denote an earned degree.
    '''
    if date.month < 4:
        return 'Winter'
    elif date.month < 8:
        return 'Summer'
    elif date.month <= 12:
        return 'Fall'
    else:
        return np.nan

def degree_type(degree_title):
    '''
    Given a degree title (such as "Certificate of Completion" or "Bachelor of
    Applied Science"), return the type of degree from the list Certificate,
    Associate, Bachelor, Master, PhD, JD, MD.
    '''
    degrees = ['Certificate', 'Associate', 'Bachelor', 'Master', 'PhD', 'JD', 'MD']

    for degree in degrees:
        upper = degree.upper()
        if upper in degree_title:
            return degree
        elif upper + 'S' in degree_title:
            return degree
        else:
            if 'DOCTORATE' in degree_title:
                return 'PhD'
            elif 'PHILOSOPHY' in degree_title:
                return 'PhD'
            elif 'JURIS' in degree_title:
                return 'JD'
            elif 'MEDICAL' in degree_title:
                return 'MD'
            elif 'MEDICINE' in degree_title:
                return 'MD'
