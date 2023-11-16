#!/usr/bin/env python

import datetime
import time

def set_api_key(key):
    try:
        with open('/etc/daos/api.key', 'w+') as f:
            f.write(key)
    except Exception as e:
        print ("ERROR: failed to set API key: ", e)

def get_current_epoch(resolution: str = '5min'):
    current_epoch = datetime.datetime.now()
    current_epoch = current_epoch.replace(minute=(current_epoch.minute // 5) * 5, second=0, microsecond=0)
    return current_epoch.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_next_epoch(resoltuion: str = '5min'):
    next_epoch = datetime.datetime.now()
    next_epoch = next_epoch.replace(minute=(next_epoch.minute // 5 + 1) * 5, second=0, microsecond=0)
    return next_epoch.strftime("%Y-%m-%dT%H:%M:%SZ")

def wait_till_next_epoch(resolution: str = '5min'):
    current_time = datetime.datetime.now()
    next_epoch = datetime.datetime.now()
    next_epoch = next_epoch.replace(minute=(next_epoch.minute // 5 + 1) * 5, second=0, microsecond=0)
    sleep_time = (next_epoch - current_time).total_seconds()
    time.sleep(sleep_time)
