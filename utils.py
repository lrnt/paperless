from datetime import datetime

def isoformat_to_datetime(isoformat):
    if not isoformat:
        return None
    return datetime.strptime(isoformat, '%Y-%m-%dT%H:%M:%S.%f')
