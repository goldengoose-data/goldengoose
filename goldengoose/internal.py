#!/usr/bin/env python

import datetime
import news
import pydaos

#
# Goldengoose Objects
#

#
# Stocks
class ggStocks(pydaos.DCont):
    """
    The global stocks database object. With this object you will be able to access all of
    goldengoose data's stock data.
    """

    def __init__(self):
        super().__init__("goldengoose", "assets")

class ggStock(pydaos.DDict):
    def dump(self, start: str = "", stop: str = "", resolution: str = ""):
        """
        Dump all data for this stock.

        :param start:
        :param stop:
        :resolution:
        """

        return super().dump(start=start, stop=stop, resolution=resolution)

#
# Options
class ggOptions(pydaos.DCont):
    """
    The global options database object. With this object you will be able to access all of
    goldengoose data's option data.
    """

    def __init__(self):
        super().__init__("goldengoose", "options")

class ggOptionChain(pydaos.DDict):
    def dump(self, start: str = "", stop: str = "", resolution: str = ""):
        """
        Dump all data for this option.

        :param start:
        :param stop:
        :resolution:
        """

        return super().dump(start=start, stop=stop, resolution=resolution)

class ggOption(pydaos.DDict):
    def dump(self, start: str = "", stop: str = "", resolution: str = ""):
        """
        Dump all data for this option.

        :param start:
        :param stop:
        :resolution:
        """

        return super().dump(start=start, stop=stop, resolution=resolution)

#
# Catalogs
class ggCatalogs(pydaos.DCont):
    """
    The global catalogs database object. With this object you will be able to access
    all of goldengoose data's catalog data. These catalogs contain the constituents
    of etf's, inverse pairs, indecies, etc.
    """

    def __init__(self):
        super().__init__("goldengoose", "catalogs")

class ggCatalog(pydaos.DDict):
    def dump(self):
        """
        Dump all data for this catalog.
        """

        return super().dump()

#
# News
class ggNews(pydaos.DCont):
    """
    The global stocks database object. With this object you will be able to access all of
    goldengoose data's stock data.
    """

    def __init__(self):
        super().__init__("goldengoose", "news")

class ggCalendar(pydaos.DDict):
    def dump(self, start: str = "", stop: str = ""):
        """
        Dump all data for this stock.

        :param start:
        :param stop:
        """

        return super().dump(start=start, stop=stop)

#
# Internal
#
def corporateHoliday(today):
    """
    Lookup given date to see if it's a market holiday.

    :param date: date given to be check
    """

    strdate = today.strftime("%Y-%m-%d")
    today = today.strptime(strdate, "%Y-%m-%d")

    if today in news.calendar:
        print (news.calendar[today])
        return True

    return False


#
# clock_forwarder: Use this to add market days to clock
#
def clock_forwarder(
    date: datetime.date,
    days: int,
    set_to_before_market: bool = False,
    set_to_after_market: bool = False
) -> datetime.date:
    """
    Forward the given date by N market days.

    :param date: Starting date
    :param days: Days to forward
    :param set_to_before_market: Sets the datetime to 11:30:00 UTC
    :param set_to_after_market: Sets the datetime to 23:59:00
    """

    if set_to_before_market:
        date = date.replace(hour=11, minute=30, second=0, microsecond=0)
    if set_to_after_market:
        date = date.replace(hour=23, minute=59, second=0, microsecond=0)

    if corporateHoliday(date):
        date = date + datetime.timedelta(days=1)
        date = clock_forwarder(date,days)
        return date

    weekday = date.strftime("%a")
    if weekday == "Sun":
        date = date + datetime.timedelta(days=1)
        date = clock_forwarder(date,days)
        return date
    if weekday == "Sat":
        date = date + datetime.timedelta(days=2)
        date = clock_forwarder(date,days)
        return date

    if days == 0:
        return date

    # Special case used to detect weekends and holidays as input
    if days == -1:
        return date

    date = date + datetime.timedelta(days=1)
    days = days - 1
    date = clock_forwarder(date, days)
    return date


