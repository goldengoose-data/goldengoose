#!/usr/bin/env python

import pydaos
indices = pydaos.DCont('goldengoose', 'indices')

def get(index):
    return indices.get(index)
