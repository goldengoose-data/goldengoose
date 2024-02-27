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

### Stream live data
```python
#!/usr/bin/env python
# Example for aggregated live asset data

import goldengoose
import datetime

asset_data = goldengoose.assets.get('ADBE')

while True:
    epoch = goldengoose.get_next_epoch()
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

### Find x percent gainers/losers since yesterday
```python
import goldengoose
import datetime

today = datetime.now().date()
yesterday = today - timedelta(days=1)

assets = goldengoose.assets.list()
for asset in assets:

    asset_data = goldengoose.assets.get(asset)
    yesterdays_close = yesterday.strftime("%Y-%m-%d") + "T21:00:00Z"
    datapoint = asset_data[yesterdays_close]
    close_price = datapoint['close_price']

    todays_open = today.strftime("%Y-%m-%d") + "T13:30:00Z"
    if todays_open not in asset_data:
        print ("Todays open has not been written yet")
        continue

    datapoint = asset_data[todays_open]
    open_price = datapont['open_price']

    percent_change = ((open_price - close_price) / close_price) * 100
    if percent_change > 1.75:
        print ("Increase found: ", asset)
```
