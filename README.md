# PyBit
**Version:** 0.1  
**Description:** A private Python module for abstracting the Fitbit Web API  
**Author:** Emanuel Lucban

**Note:** I currently have no plans on publishing this module on PyPI or Conda
___

## Installation
* pip
    ```    
    pip install /path/pybit.tar.gz
    ```
____

## Classes

### FitbitAuth

```
from pybit.auth import FitbitAuth
```

**FitbitAuth** is a class for facilitating Fitbit user authorization and access token management 
using OAUTH2 Authorization Code Grant

#### Constructor
```
fbauth = FitBitAuth(client_id, client_secret, redirect_uri, scope=None, user_id=None, access_token=None,
                 expires_dt=None, refresh_token=None)
```
**params**  
  * **client_id:** client id for Fitbit app  
  * **client_secret:** secret key for Fitbit app  
  * **redirect_url:** redirect url specified in Fitbit app for Fitbit authorization callback  
  * **scope:** list of data collection scope specified here https://dev.fitbit.com/build/reference/web-api/oauth2/#scope  
  * **user_id:** if user already authorized, Fitbit returns a encoded user_id, None otherwise.  
  * **access_token:** OAUTH2 access token, if user is already authorized. None otherwise.  
  * **expires_dt:** datetime object of access token expiration.  
  * **refresh_token:** OAUTH2 refresh token, if user is already authorized. None otherwise.  

#### Methods
**generate_auth_url(state, prompt=None)**  
returns a Fitbit authorization URL for the Fitbit user to authorize your app.  

**params**
  * **state:** a parameter to return from Fitbit authorization callback. Fitbit recommends a CSRF token.
  * **prompt:** string, None for default prompt type. Prompt types specified here https://dev.fitbit.com/build/reference/web-api/oauth2/#authorization-page 

**authorize(auth_code)**  
returns None. Exchanges Fitbit authorization code for OAUTH2 access token and refresh token

**params**
  * **auth_code:** string, The authorization code provided by Fitbit on authorization callback.

**get_access_token()**  
returns the OAUTH2 access token. User must be authorized first. Calling this method will also perform
an automatic token refresh.

**revoke_access()**  
will deauthorize user and revoke access/refresh token on Fitbit


