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

    def heartrate(self, start_date, end_date, data_format='df', *df_kwargs):
        """
        Fetches intraday time-series heartrate data from Fitbit API.

        :param start_date: Start date yyyy-MM-dd
        :param end_date: End date yyyy-MM-dd
        :param data_format: 'df' for Pandas DataFrame or 'json'
        :return: json or dataframe of heartrate data
        """
        # Note example of REST API call for heartrate data (intraday)
        # GET https://api.fitbit.com/1/user/[user-id]/activities/heart/date/[date]/[period].json
        # GET https://api.fitbit.com/1/user/[user-id]/activities/heart/date/[base-date]/[end-date].json
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/[end-date]/[detail-level].json
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/[end-date]/[detail-level]/time/[start-time]/[end-time].json
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/1d/[detail-level].json`
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/1d/[detail-level]/time/[start-time]/[end-time].json

        # check data_format
        if data_format != 'df' or data_format != 'json':
            raise ValueError('data_format must be df or json')

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
        # 'Private' method to handle http requests
        user_id = self.fitbit_auth.user_id

        # get access token for user, will refresh automatically on call
        try:
            # TODO: Need to somehow hook the refresh calls so updated tokens can be persisted somewhere
            access_token = self.fitbit_auth.get_access_token()
        except (ValueError, PermissionError) as e:
            raise ValueError('Error with access token %s' % e)

        header = {'Authorization': 'Bearer %s' % access_token}
        api_req = requests.get(self.api_uri + path, headers=header)

        # API Exception Handling
        if api_req.status_code != 200:
            raise ValueError('Error fetching data from %s. Response Code: %d Error: %s' % (path, api_req.status_code,
                                                                                           api_req.json()['errors']))
        return api_req.json()




