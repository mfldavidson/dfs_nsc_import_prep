import numpy as np

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
