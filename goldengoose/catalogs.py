#!/usr/bin/env python

import pydaos
catalogs = pydaos.DCont('goldengoose', 'catalogs')

def get(catalog):
    return catalogs.get(catalog)
