from dateutil.parser import parse
from dateutil import tz
from datetime import *
from dateutil.relativedelta import *
import os
import sys


#example: '2020-10-28T06:14:11.2469379+00:00'
def toLocalTimeString(dateString, isTimeAgo=False):
    dt = parse(dateString)
    new_ts = dt.astimezone(tz.tzlocal())
    #print(new_ts.tzname()) #Show time zone
    #print(relativedelta(datetime.now(tz.tzlocal()), new_ts))
    #timeAgoStr = timeago.format(new_ts, datetime.now(tz.tzlocal()))
    timeAgoStr = time_ago(new_ts)
    if isTimeAgo:
        return timeAgoStr
    return timeAgoStr + ' · ' + str(new_ts.date().isoformat()) + ' ' + str(
        new_ts.time().strftime('%H:%M'))


#print(tolocalTimeString('2020-10-28T06:14:11.2469379+00:00'))


def getFactionString(factions):
    allFactions = ''
    for faction in factions:
        line_word = faction.split('_')
        allFactions += line_word[1] + ' '
    return allFactions


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        #base_path = os.path.abspath(".")
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def time_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Modified from: http://stackoverflow.com/a/1551394/141084
    """
    now = datetime.now(tz.tzlocal())
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    else:
        raise ValueError('invalFid date %s of type %s' % (time, type(time)))
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "Just now"
        if second_diff < 60:
            return str(int(second_diff)) + " sec ago"
        if second_diff < 120:
            return "1 min ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " min ago"
        if second_diff < 7200:
            return "1 hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(int(day_diff)) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"
