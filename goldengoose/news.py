#!/usr/bin/env python

import pydaos

news = pydaos.DCont('goldengoose', 'news')
calendar = news.get('calendar')

def get(item):
    return news.get(item)
