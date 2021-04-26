"""
Resource Data and Set classes
"""
import pandas as pd
import json
import datetime


class Resource(object):
    def __init__(self, raw_json):
        self.raw_json = raw_json


# A set of Fitbit Data objects date range queries from API
class ResourceSet(object):
    r_dict = {}

    def __init__(self):
        pass

    def sort(self, asc=True):
        """
        Sort records by date
        :param asc: Default True, False for Descending
        """
        pass

