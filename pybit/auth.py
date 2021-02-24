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

    def __init__(self, client_id, client_secret, scope=None, access_token=None, expires_dt=None, refresh_token=None,
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
        self.expires_dt = expires_dt
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri

        # if any of access_token, expires_in, and refresh_token is None, then this is not a pre-authorized user.
        # will have to return the authorization uri, with the requested scope
        if not all([self.access_token, self.refresh_token, self.expires_dt]):
            # Generate authorization URI
            pass

    def generate_auth_url(self):
        # Authorization code is returned on callback per OAUTH2 spec. auth code must be exchanged within 1 hour
        uri = self.auth_uri
        uri = uri + '?response_type=code&client_id=%s' % self.client_id
        uri = uri + '&redirect_uri=%s' % self.redirect_uri.replace(':', '%3A').replace('/', '%2F')
        uri = uri + '&scope=%s' % '%20'.join(self.scope)
        return uri

    def get_access_token(self, auth_code=None):
        # If no auth_code and have refresh_token, then refresh
        concat = '%s:%s' % (self.client_id, self.client_secret)
        header = {'Authorization': 'Basic ' + str(base64.b64encode(concat.encode('ascii')), 'utf-8'),
                  'Content-Type': 'application/x-www-form-urlencoded'}

        if not auth_code:
            body = {'client_id': self.client_id,
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri,
                    'code': auth_code}
        # else refresh
        else:
            body = {'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token}

        pass

    def revoke_access(self):
        pass

    def _call(self, **kwargs):
        pass



