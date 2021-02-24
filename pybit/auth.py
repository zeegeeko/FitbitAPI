import requests
import json
import base64


"""
concat = client['id'] + ':' + client['secret']
    header = {'Authorization': 'Basic ' + str(base64.b64encode(concat.encode('ascii')), 'utf-8'),
              'Content-Type': 'application/x-www-form-urlencoded'}

    body = {'client_id': client['id'],
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://fitbit.inferre.com/',
            'code': auth_code}

    acg = requests.post(url, headers=header, data=body)
    # TODO: Exception handling here
    oauth_token.access_token = acg.json()['access_token']
    oauth_token.refresh_token = acg.json()['refresh_token']
    oauth_token.generated_date = datetime.datetime.now()
"""


class FitbitAuth(object):

    api_uri = 'https://api.fitbit.com/oauth2'
    auth_uri = 'https://www.fitbit.com/oauth2/authorize'
    full_scope = ['activity', 'heartrate', 'location', 'nutrition', 'profile', 'settings', 'sleep', 'social', 'weight']

    def __init__(self, client_id, client_secret, scope=None, access_token=None, expires_in=None, refresh_token=None,
                 redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        # Check if scope is correct, if empty or None, use full scope. Raise ValueError if invalid scope
        if not scope:
            self.scope = self.full_scope
        else:
            if set(scope).issubset(set(self.full_scope)):
                self.scope = scope
            else:
                raise ValueError('Scope: %s is invalid' % scope)
        self.access_token = access_token
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri

        # if any of access_token, expires_in, and refresh_token is None, then this is not a pre-authorized user.
        # will have to return the authorization uri, with the requested scope
        if not all([self.access_token, self.refresh_token, self.expires_in]):
            # Generate authorization URI
            pass

    def _call(self, **kwargs):
        pass



