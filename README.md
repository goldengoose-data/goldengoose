# Goldengoose Data

Welcome! This is a financial assets API based on the Intel DAOS filesystem. It is designed to be used in conjunction with AI/ML trading algorithms, but can behave like regular REST/Websockt API's. Data is continusly updated and segmented into 'epochs'. The 'resolution' of the epoch, determines the interval between each heart beat. There is support for all three major United States stock market indecies (Dow, S&P500, Nasdaq-100), as well as gold & bitcoin.

Here's how it works. A goldengoose object is defined at the start of your program, this object contains all past & present ohcl datapoints for all supported assets. An epoch is defined by the following key/pair format: epoch/data. The epoch key is the timestamp of the desired epoch, such as [2022-10-01T10:00]. The time zone is Eastern Standard Time and all datapoints are interpolated, if not present, to gaurantee data availability. This means that if there was a gap in the available data (due to errors or downtime), the last recorded data point is forward copied across all subsequent epochs till the next available data point.

## Installation

Unlike REST & Websocket API's the goldengoose API does require a client side application to be running. This may be a deal breaker for some, but it is part of the fundamental design of the DAOS filesystem and enables end users to achieve high speed access to their data. Luckily we have simplified this into a single debian package:

To install please add our debian repo (requires root):

> **_NOTE:_** Only Debian 12 is supported at the moment.

```bash
wget https://ezthinking.org:9999/debian/Release.gpg -O /usr/share/keyrings/goldengoose.gpg
# echo 'deb [signed-by=/usr/share/keyrings/goldengoose.gpg] https://ezthinking.org:9999/debian /' > /etc/apt/sources.list.d/goldengoose.list
# Signing not available yet
echo 'deb [trusted=yes] https://ezthinking.org:9999/debian /' > /etc/apt/sources.list.d/goldengoose.list
apt update
apt install goldengoose
```

### Setting the API Key
To set the api key. This only needs to be run one time.
```python
import goldengoose
goldengoose.set_api_key("api_key")
```

## Examples

### List all assets available
```python
import goldengoose

assets = goldengoose.assets.list()
for asset in assets:
    print (asset)
```

### Get data for an asset
```python
#!/usr/bin/env python
# Get data for an asset

import goldengoose
import datetime

asset_data = goldengoose.assets.get('ADBE')

# Get data start time...
start_date = asset_data['start']
start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')

while start_date < datetime.datetime.now():
    key = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = asset_data[key]
    print (key, data)
    start_date += datetime.timedelta(minutes=5)
```

### Example for aggregated live asset data
```python
#!/usr/bin/env python
# Example for aggregated live asset data

import goldengoose
import datetime

asset_data = goldengoose.assets.get('ADBE')
epoch = goldengoose.get_current_epoch()

while True:
    if epoch not in asset_data:
        goldengoose.wait_till_next_epoch()
    print (asset_data[epoch])
```

### Download all data for an asset
```python
#!/usr/bin/env python

import goldengoose

asset_data = goldengoose.assets.get('ADBE')
local_json = asset_data.dump() # Careful, may take several minutes depending on your connection.
```

### Download a date range for an asset
```python
import goldengoose

asset_data = goldengoose.assets.get('ADBE')
start = '2020-01-02T00:00:00Z'
stop = '2023-11-01T00:00:00Z' # May be ommited to download data till last entry
local_json = asset_data.get_range(start, stop) # Careful, may take several minutes depending on your connection and size of date range.
```