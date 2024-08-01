from django.db.models import Func


class Epoch(Func):
    """
    For date and timestamp values, the number of seconds since 1970-01-01 00:00:00 UTC (can be negative);
    for interval values, the total number of seconds in the interval.
    """
    function = 'EXTRACT'
    template = '%(function)s(EPOCH FROM %(expressions)s)'
