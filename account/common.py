from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from pytz import timezone
from datetime import datetime
from functools import wraps

import calendar
import django.utils
import pytz
import json

LOCAL = timezone('Europe/Stockholm')
UTC = pytz.utc


def http_badrequest(message):
    return HttpResponseBadRequest(json.dumps({'status': 'failed', 'message': message}), content_type='application/json')


def http_forbidden(message):
    if message is None or message == '':
        message = 'Request was made with bad parameters.'
    return HttpResponseForbidden(json.dumps({'status': 'failed', 'message': message}), content_type='application/json')


def http_json_response(json_response):
    return HttpResponse(json.dumps(json_response), content_type='application/json')


def http_success():
    return HttpResponse(json.dumps({'status:': 'success'}), mimetype='application/json')


def ensure_post(f):
    '''Decorator used to ensure that a view is called by POST.'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.method != 'POST':
            return http_badrequest('Request was not POST.')
        return f(*args, **kwargs)
    return wrapper


def to_timestamp(datetime):
    """
    Takes a datetime and converts it into a POSIX timestamp in UTC timezone.
    """
    return calendar.timegm(as_utc_time(datetime).timetuple())


def from_timestamp(timestamp):
    """
    Takes a timestamp, assumed to be in UTC timezone, and returns
    a datetime in UTC timezone.
    """
    return UTC.localize(datetime.utcfromtimestamp(timestamp))


def as_local_time(time):
    return LOCAL.normalize(time.astimezone(LOCAL))


def as_utc_time(time):
    return UTC.normalize(time.astimezone(UTC))


def utc_now():
    return django.utils.timezone.now()
    # now = datetime.datetime.utcnow().replace(tzinfo=UTC)
    # return now
