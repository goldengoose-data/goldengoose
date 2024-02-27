#!/usr/bin/env python

import datetime
import time
import internal

def set_api_key(key):
    try:
        with open('/etc/daos/api.key', 'w+') as f:
            f.write(key)
    except Exception as e:
        print ("ERROR: failed to set API key: ", e)

def _convert_resolution_to_interval(resolution):
    if resolution == '5min':
        return 5
    if resolution == '1min':
        return 1

    # Default to 5min
    return 5

def get_current_epoch(resolution: str = '5min'):
    interval = _convert_resolution_to_interval(resolution)
    current_epoch = datetime.datetime.now()
    current_epoch = current_epoch.replace(minute=(current_epoch.minute // interval) * interval, second=0, microsecond=0)
    return current_epoch.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_next_epoch(epoch: str = "", resolution: str = '5min'):
    interval = _convert_resolution_to_interval(resolution)
    if epoch:
        next_epoch = datetime.datetime.strptime(epoch, '%Y-%m-%dT%H:%M:%SZ')
    else:
        next_epoch = datetime.datetime.now()

    next_minute = (next_epoch.minute // interval + 1) * interval
    if next_minute == 60:
        next_hour = next_epoch.hour + 1
        if next_hour == 24:
            next_epoch = internal.clock_forwarder(next_epoch, 1, set_to_before_market=True)
        else:
            next_epoch = next_epoch.replace(hour=next_hour, minute=0, second=0, microsecond=0)
    else:
        next_epoch = next_epoch.replace(minute=next_minute, second=0, microsecond=0)

    return next_epoch.strftime("%Y-%m-%dT%H:%M:%SZ")

def wait_till_next_epoch(resolution: str = '5min'):
    interval = _convert_resolution_to_interval(resolution)
    current_time = datetime.datetime.now()
    next_epoch = datetime.datetime.now()
    next_epoch = next_epoch.replace(minute=(next_epoch.minute // interval + 1) * interval, second=0, microsecond=0)
    sleep_time = (next_epoch - current_time).total_seconds()
    time.sleep(sleep_time)
