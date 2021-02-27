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

    def heartrate(self, start_date, end_date, data_format, df_kwargs):
        """
        Fetches intraday time-series heartrate data from Fitbit API.

        :param start_date: Start date yyyy-MM-dd
        :param end_date: End date yyyy-MM-dd
        :return: json or dataframe of heartrate data
        """
        # Note example of REST API call for heartrate data (intraday)
        # GET https://api.fitbit.com/1/user/[user-id]/activities/heart/date/[date]/[period].json
        # GET https://api.fitbit.com/1/user/[user-id]/activities/heart/date/[base-date]/[end-date].json
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/[end-date]/[detail-level].json
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/[end-date]/[detail-level]/time/[start-time]/[end-time].json
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/1d/[detail-level].json`
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/1d/[detail-level]/time/[start-time]/[end-time].json

        base_uri = '/1/user/%s/activities/heart/date/%s%s.json'
        resp = self._call(base_uri)


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

    def _call(self, path):

        user_id = self.fitbit_auth.user_id
        access_token = self.fitbit_auth.get_access_token()
        header = {'Authorization': 'Bearer %s' % access_token}
        api_req = requests.get(self.api_uri + path, header=header)

        # API Exception Handling
        if api_req.status_code != 200:
            raise ValueError('Error fetching data from %s. Response Code: %d Error: %s' % (path, api_req.status_code,
                                                                                           api_req.json()['errors']))




