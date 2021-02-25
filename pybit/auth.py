import requests
import json
import base64
import datetime


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
            lscope = [i.lower() for i in scope]
            if set(lscope).issubset(set(self.full_scope)):
                self.scope = lscope
            else:
                raise ValueError('Scope: %s is invalid' % scope)
        self.access_token = access_token
        self.expires_dt = expires_dt
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri

        # if any of access_token, expires_in, and refresh_token is None, then this is not a pre-authorized user.
        if not all([self.access_token, self.refresh_token, self.expires_dt]):
            # set authorized to false
            self.is_authorized = False
        else:
            self.is_authorized = True

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
        header = {'Authorization': 'Basic %s' % str(base64.b64encode(concat.encode('ascii')), 'utf-8'),
                  'Content-Type': 'application/x-www-form-urlencoded'}

        if not auth_code:
            # No auth code, check if authorized, if not raise error
            if not self.is_authorized:
                raise PermissionError('Not authorized and no authorization code. Call generate_auth_url to generate a '
                                      'URL for the user to authorize the app')

            data = {'client_id': self.client_id,
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri,
                    'code': auth_code}
        # else refresh
        else:
            data = {'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token}

        pass

    def revoke_access(self):
        # Call API to revoke token and deauthorize user
        self.is_authorized = False

    def _call(self, **kwargs):
        pass



