#!/usr/bin/env python

import pydaos
assets = pydaos.DCont('goldengoose', 'assets')

def get(asset):
    return assets.get(asset)

def list():
    return assets['asset-list'].dump()
