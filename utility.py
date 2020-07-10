# Time
from datetime import datetime
from datetime import timedelta
from pytz import timezone

"""
Time
"""
# My Default Timezone
def default_timezone():
    _tz = timezone('Europe/Rome')
    return(_tz)
    
# Now Time with Formatter or not
def my_time_now(_what_format = False):
    _my_timezone = default_timezone()
    if not _what_format:
        _now = datetime.now(_my_timezone)
    else:
        _now = datetime.now(_my_timezone).strftime("%Y-%m-%d %H:%M:%S")
    return(_now)

# TimeStamp milliseconds Formatter
def timestamp_formatter(_date):
    _my_timezone    = default_timezone()
    _my_date        = datetime.fromtimestamp(_date/1000, _my_timezone).strftime('%Y-%m-%d %H:%M:%S')
    return(_my_date)

"""
Log
"""
def my_log(_type, _func, _inputs ,_msg):
    if _inputs is not None:
        _msg_error = f"{my_time_now(True)} {_type} on function {_func} with inputs {_inputs} {chr(10)}MESSAGE: {_msg} {chr(10)}"
    else:
        _msg_error = f"{my_time_now(True)} {_type} on function {_func} {chr(10)}MESSAGE: {_msg} {chr(10)}"
    return(_msg_error)
