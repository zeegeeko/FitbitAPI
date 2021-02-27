import requests
import json
import base64
import datetime


class FitbitAuth(object):

    api_uri = 'https://api.fitbit.com/oauth2'
    auth_uri = 'https://www.fitbit.com/oauth2/authorize'
    full_scope = ['activity', 'heartrate', 'location', 'nutrition', 'profile', 'settings', 'sleep', 'social', 'weight']

    def __init__(self, client_id, client_secret, redirect_uri, scope=None, user_id=None, access_token=None,
                 expires_dt=None, refresh_token=None):
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

        if not redirect_uri or redirect_uri == '':
            raise ValueError('Redirect_uri cannot be None or blank')

        self.redirect_uri = redirect_uri
        self.user_id = user_id

        # if any of user_id, access_token, expires_in, and refresh_token is None, then this is not a pre-authorized user
        if not all([self.user_id, self.access_token, self.refresh_token, self.expires_dt]):
            # set authorized to false
            self.is_authorized = False
        else:
            self.is_authorized = True

    def generate_auth_url(self):
        """
        Generates a Fitbit user authorization page. Fitbit API sends the authorization code on callback to the
        redirect_uri.

        :return: Authorization URL to send to user
        """
        # Authorization code is returned on callback per OAUTH2 spec. auth code must be exchanged within 1 hour
        uri = self.auth_uri
        uri = uri + '?response_type=code&client_id=%s' % self.client_id
        uri = uri + '&redirect_uri=%s' % self.redirect_uri.replace(':', '%3A').replace('/', '%2F')
        uri = uri + '&scope=%s' % '%20'.join(self.scope)
        return uri

    def authorize(self, auth_code):
        """
        Requests OAUTH access token and refresh token, exchanging authorization code. Updates the access_token,
        refresh_token and expires_dt

        :param auth_code: authorization code from fibit authorization callback
        """
        # Check if already authorized
        if self.is_authorized:
            return
        if not auth_code or auth_code == '':
            raise ValueError('Authorization code cannot be blank or None')

        try:
            resp = self._call('/token',
                              client_id=self.client_id,
                              grant_type='authorization_code',
                              redirect_uri=self.redirect_uri,
                              code=auth_code)
            print('User is authorized. Call get_access_token() for OAUTH access token needed for API calls')
        except ValueError as e:
            self.is_authorized = False
            raise ValueError('Failed to authorize. %s' % e)

        # Update vars
        self.access_token = resp['access_token']
        self.refresh_token = resp['refresh_token']
        self.user_id = resp['user_id']
        self.expires_dt = datetime.datetime.now() + datetime.timedelta(seconds=resp['expires_in'])
        self.is_authorized = True

    def get_access_token(self):
        """
        Retrieves the most current access token. Will automatically request token refresh if access token is expired.

        :return: access token
        """
        if not self.is_authorized:
            raise PermissionError('Currently not authorized, call get_auth_url() to generate a Fitbit user '
                                  'authorization page, then call authorize() with access code from the callback')

        # Check token expiry
        if not isinstance(self.expires_dt, datetime.datetime):
            raise ValueError('expires_dt is not a valid datetime object')
        if self.expires_dt < datetime.datetime.now():
            # Expired, call token refresh.
            try:
                self._refresh_token()
            except ValueError as e:
                raise ValueError(e)
        return self.access_token

    def revoke_access(self):
        # Call API to revoke token and deauthorize user
        try:
            resp = self._call('/revoke', access_token=self.access_token)
        except ValueError as e:
            raise ValueError('Failed to revoke token: %s' % e)
        self.is_authorized = False
        self.access_token = None
        self.refresh_token = None
        self.expires_dt = None

    def _refresh_token(self):
        # Update access_token, refresh_token and expires_dt
        try:
            resp = self._call('/token', grant_type='refresh_token', refresh_token=self.refresh_token)
        except ValueError as e:
            raise ValueError('Failed to refresh expired token: %s' % e)

        # Update vars
        self.access_token = resp['access_token']
        self.refresh_token = resp['refresh_token']
        self.expires_dt = datetime.datetime.now() + datetime.timedelta(seconds=resp['expires_in'])

    def _call(self, path, **kwargs):
        concat = '%s:%s' % (self.client_id, self.client_secret)
        header = {'Authorization': 'Basic %s' % str(base64.b64encode(concat.encode('ascii')), 'utf-8'),
                  'Content-Type': 'application/x-www-form-urlencoded'}

        api_req = requests.post(self.api_uri + path, headers=header, data=kwargs)

        # Fitbit API Exception Handling
        if api_req.status_code != 200:
            # Raise Error
            raise ValueError('Response Status: %d. Fitbit API Error %s' % (api_req.status_code,
                                                                           api_req.json()['errors']))
        return api_req.json()




