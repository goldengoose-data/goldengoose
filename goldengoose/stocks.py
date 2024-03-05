#!/usr/bin/env python

"""
Endpoints for connecting to all assets available from goldengoose-data.
"""

__version__ = "0.1.0"

# Connect to back-end
import internal
stocks = internal.ggStocks()

def get(stock):
    """
    Return a data object for a given symbol.

    :param stock: Ticker Symbol. E.g. "MSFT"
    :type stock: str
    :return: goldengoose stock object
    :rtype: ggStock
    """

    return stocks.get(stock)

def list():
    """
    Return a list of all stock symbols available from goldengoose-data.
    :return: List of strings
    :rtype: list[str]
    """

    return stocks['asset-list'].dump()
