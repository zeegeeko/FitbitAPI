from auth import FitbitAuth

import requests
import json
import datetime
import pandas as pd


class Fitbit(object):
    api_uri = 'https://api.fitbit.com'

    def __init__(self, fitbit_auth):
        # check that FitbitAuth instance is valid
        if not isinstance(fitbit_auth, FitbitAuth):
            raise TypeError('Constructor needs a valid FitbitAuth instance')
        self.fitbit_auth = fitbit_auth

    def activity(self):
        pass

    def heartrate(self):
        pass

    def location(self):
        pass

    def nutrition(self):
        pass

    def profile(self):
        pass

    def settings(self):
        pass

    def sleep(self):
        pass

    def social(self):
        pass

    def weight(self):
        pass

    def _call(self, path, **kwargs):
        pass




