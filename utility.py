from dateutil.parser import parse
from dateutil import tz
from datetime import *
import timeago
from dateutil.relativedelta import *
import os
import sys

#example: '2020-10-28T06:14:11.2469379+00:00'
def tolocalTimeString(dateString):
    dt = parse(dateString)
    new_ts = dt.astimezone(tz.tzlocal())
    #print(new_ts.tzname()) #Show time zone
    #print(relativedelta(datetime.now(tz.tzlocal()), new_ts))
    timeAgoStr = timeago.format(new_ts, datetime.now(tz.tzlocal()))
    return timeAgoStr + ' · ' + str(new_ts.date().isoformat()) + ' ' + str(new_ts.time().strftime('%H:%M'))

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