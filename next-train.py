#!/usr/bin/env python

import re
import csv
import datetime
import math
from contextlib import contextmanager
from os import getenv

COLORS = {
    'WARNING': '\033[31m',
    'OK': '\033[32m',
    'END': '\033[0m'
}

# Constants
BASE_DIR = getenv('HOME') + '/bin/metros/ATX/'
NOW = datetime.datetime.now()
WALKING_MINUTES = 18

ROUTE_ID = '550'
DIRECTION = 'S'
SERVICE_IDS = ['110-13301', '110-14701', '110-13401', '110-14801', '110-14601', '110-14304', '110-20804', '110-15504', '110-20805']
KRAMER_STATION_STOP_ID = '5539'

active_service_ids = set()
train_trip_ids = []
next_train = None

@contextmanager
def openCSVDict(filename):
    with open(filename, 'rU') as opened_file:
        file_csv = csv.DictReader(opened_file)
        yield file_csv

def formatTime(time):
    return time.strftime('%I:%M:%S %p')


# Get the right service ID for today
with openCSVDict(BASE_DIR + 'calendar_dates.txt') as dates:
    for row in dates:
        service_id = row['service_id']
        date = row['date']
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])

        if ((service_id in SERVICE_IDS) and ((year, month, day) == (NOW.year, NOW.month, NOW.day))):
            active_service_ids.add(service_id)

# Get trip IDs for train routes today
with openCSVDict(BASE_DIR + 'trips.txt') as trips:
    for row in trips:
        # Add row trip ID to trip ids if it is the rail route southbound for today's service
        if (row['route_id'] == ROUTE_ID) and (row['dir_abbr'] == DIRECTION) and (row['service_id'] in active_service_ids):
            train_trip_ids.append(row['trip_id'])


with openCSVDict(BASE_DIR + 'stop_times.txt') as stop_times:
    for row in stop_times:
        if row['trip_id'] in train_trip_ids and row['stop_id'] == KRAMER_STATION_STOP_ID:
            departure_time = row['departure_time'].split(':')
            hour = int(departure_time[0]) if departure_time[0] != '24' else 0
            minute = int(departure_time[1])
            departure_time = datetime.datetime(NOW.year, NOW.month, NOW.day, hour, minute)

            if departure_time > NOW:
                if not next_train:
                    next_train = departure_time
                else:
                    next_train = departure_time if next_train > departure_time else next_train

if next_train:
    time_delta = next_train - NOW
    minutes_until_next_train = int(math.floor(time_delta.seconds / 60))
    minute_string = 'minutes' if minutes_until_next_train > 1 else 'minute'
    should_walk_to_train = minutes_until_next_train > WALKING_MINUTES
    advice_color = COLORS['OK'] if should_walk_to_train else COLORS['WARNING']
    advice_message = 'OK to take' if should_walk_to_train else 'Wait for next train'

    print 'Next Departure: %s' % formatTime(next_train)
    print '%s%s: You have %d %s to get to station %s' % (advice_color, advice_message, minutes_until_next_train, minute_string, COLORS['END'])
else:
    print '%sSorry, the train does not run today anymore%s' % (COLORS['WARNING'], COLORS['END'])
