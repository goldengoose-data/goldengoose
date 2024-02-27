# Goldengoose Data

Welcome! This is a financial assets API based on the Intel DAOS filesystem. It is designed to be used in conjunction with AI/ML trading algorithms, but can behave like regular REST/Websockt API's. Data is continusly updated and segmented into 'epochs'. The 'resolution' of the epoch, determines the interval between each heart beat. There is support for all three major United States stock market indecies (Dow, S&P500, Nasdaq-100), as well as gold & bitcoin.

Here's how it works. A goldengoose object is defined at the start of your program, this object contains all past & present OHCL datapoints for all supported assets. An epoch is defined by the following key/pair format: epoch/data. The epoch key is the timestamp of the desired epoch, such as 2022-10-01T10:00:00. The time zone is UTC and all datapoints are interpolated, if not present, to gaurantee data availability. This means that if there was a gap in the available data (due to errors or downtime), the last recorded data point is forward copied across all subsequent epochs till the next available data point. This will gaurantee ease of operations on the database.

## What's in this Repo

This repo represents the public pythonic API function to accesses that data. The goldengoose python library gets installed along side the required daos libraries when installing the goldengoose debian package as described below.

## Installation

Unlike REST & Websocket API's the goldengoose API does require a lightweight client side application to be running. This may be a deal breaker for some, but it is part of the fundamental design of the DAOS filesystem and enables end users to achieve high speed access to their data. Luckily we have simplified this into a easy to install debian package:

To install please run our installer (requires root):

```bash
echo "deb [trusted=yes] https://ezthinking.org/Debian_12/ ./" > /etc/apt/sources.list.d/goldengoose.list
apt update
apt install goldengoose
```

### Setting the API Key
To set the api key. This only needs to be run one time. A free API is already installed and this step is only necessary if subscribed to extra market data.

```python
import goldengoose
goldengoose.set_api_key("api_key")
```
