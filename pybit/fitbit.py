from auth import FitbitAuth

import requests
import json
from datetime import datetime, timedelta
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

    def heartrate(self, start_date, end_date, detail='1min', data_format='df', **df_kwargs):
        """
        Fetches intraday time-series heartrate data from Fitbit API.

        :param start_date: Start date yyyy-MM-dd or datetime object
        :param end_date: End date yyyy-MM-dd or datetime object, if blank it will return data from start_date to today
        :param detail: string 1min or 1sec intervals (1min default)
        :param data_format: 'df' for Pandas DataFrame or 'json'
        :param **df_kwargs: keyworded arguments to pass to Pandas DataFrame
        :return: json or dataframe of time-series heartrate data
        """
        # check detail
        if detail != '1min' and detail != '1sec':
            raise ValueError('detail must be either 1min or 1sec')

        # check data_format
        if data_format != 'df' and data_format != 'json':
            raise ValueError('data_format must be df or json')

        s_date, e_date = None, None
        # check start/end date
        if start_date is None or start_date == '':
            raise ValueError('start_date cannot be None or empty')
        if start_date is type(datetime):
            s_date = start_date.date()
        else:
            try:
                s_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except Exception as e:
                raise ValueError('Error start_date processing string to date: %s' % e)

        # End date can be None or blank
        if end_date is not None and end_date != '':
            if end_date is type(datetime):
                e_date = end_date.date()
            else:
                try:
                    e_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                except Exception as e:
                    raise ValueError('Error end_date processing string to date: %s' % e)
        else:
            e_date = datetime.utcnow().date()

        # Note example of REST API call for heartrate data (intraday)
        # GET https://api.fitbit.com/1/user/-/activities/heart/date/[date]/1d/[detail-level].json`

        # Since the API only allows intraday data calls for 1 day per call we have to iterate and join multiple calls
        user_uri = '/1/user/%s'
        num_of_days = (s_date - e_date).dt.days

        ret_df = pd.DataFrame()
        for i in range(num_of_days):
            cur_date = s_date + timedelta(days=i)
            activity_uri = '/activities/heart/date/%s/1d/%s.json' % (cur_date, detail)
            resp = self._call(user_uri + activity_uri)
            resp_df = pd.DataFrame(resp['activities-heart-intraday']['dataset'])
            # append date to time
            resp_df['datetime'] = pd.to_datetime(str(cur_date) + ' ' + resp_df['time'])
            resp_df.drop(['time'], inplace=True)
            resp_df.rename({'value': 'hr'})
            ret_df = pd.concat([ret_df, resp_df], axis=0)

        if data_format == 'json':
            return ret_df.to_json(orient='records')
        return ret_df

    def nutrition(self):
        pass

    def profile(self):
        """
        Get user profile data (Does not include badges)

        :return: Pandas dataframe of user
        """
        path = '/1/user/%s/profile.json'
        return pd.DataFrame(self._call(path))

    def settings(self):
        pass

    def sleep(self):
        pass

    def social(self):
        pass

    def weight(self):
        pass

    def devices(self):
        """
        Get a list of Fitbit devices and device details, from user, includes (id, type, battery level, and sync date)

        :return: Pandas dataframe of devices
        """
        path = '/1/user/%s/devices.json'
        return pd.DataFrame(self._call(path))

    def _call(self, path):
        # 'Private' method to handle http requests
        user_id = self.fitbit_auth.user_id
        call_path = path % user_id
        # get access token for user, will refresh automatically on call
        try:
            # TODO: Need to somehow hook the refresh calls so updated tokens can be persisted somewhere
            access_token = self.fitbit_auth.get_access_token()
        except (ValueError, PermissionError) as e:
            raise ValueError('Error with access token %s' % e)

        header = {'Authorization': 'Bearer %s' % access_token}
        api_req = requests.get(self.api_uri + call_path, headers=header)

        # API Exception Handling
        if api_req.status_code != 200:
            raise ValueError('Error fetching data from %s. Response Code: %d Error: %s' % (path, api_req.status_code,
                                                                                           api_req.json()['errors']))
        return api_req.json()




