from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_fancy_time(d, display_full_version = False):
    """Returns a user friendly date format
    d: some datetime instance in the past
    display_second_unit: True/False
    """
    #some helpers lambda's
    plural = lambda x: 's' if x > 1 else ''
    singular = lambda x: x[:-1]
    #convert pluran (years) --> to singular (year)
    display_unit = lambda unit, name: '%s %s%s'%(unit, name, plural(unit)) if unit > 0 else ''

    #time units we are interested in descending order of significance
    tm_units = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

    rdelta = relativedelta(datetime.now(), d) #capture the date difference
    for idx, tm_unit in enumerate(tm_units):
        first_unit_val = getattr(rdelta, tm_unit)
        if first_unit_val > 0:
            primary_unit = display_unit(first_unit_val, singular(tm_unit))
            if display_full_version and idx < len(tm_units)-1:
                next_unit = tm_units[idx + 1]
                second_unit_val = getattr(rdelta, next_unit)
                if second_unit_val > 0:
                    secondary_unit = display_unit(second_unit_val, singular(next_unit))
                    return primary_unit + ', '  + secondary_unit + ' ago'
            return primary_unit + ' ago'
    return None
