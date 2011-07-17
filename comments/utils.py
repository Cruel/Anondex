from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.encoding import smart_unicode

def get_fancy_time(d, display_full_version = False):
    """Returns a user friendly date format
    d: some datetime instance in the past
    display_second_unit: True/False
    """
    #some helpers lambda's
    plural = lambda x: 's' if x > 1 else ''
    singular = lambda x: x[:-1]
    #convert plural (years) --> to singular (year)
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

def md5_file(filename):
    import hashlib
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(8192), ''):
             md5.update(chunk)
    return md5.hexdigest()

# For use with video timestamps in comments
def GetInHMS(seconds):
    seconds = float(seconds)
    minutes = int(seconds / 60)
    seconds -= 60*minutes
    return "%01d:%02d" % (minutes, seconds)