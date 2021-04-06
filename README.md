# PyBit
version 0.1  
A private Python module for abstracting the Fitbit Web API  

Author: Emanuel Lucban

**Note:** I currently have no plans on publishing this module on PyPI or Conda
___

## Installation
* Conda
    ```    
    conda install /path/pybit.tar.gz
    ```
  
* PIP
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

Constructor
```
fbauth = FitBitAuth(client_id, client_secret, redirect_uri, scope=None, user_id=None, access_token=None,
                 expires_dt=None, refresh_token=None)
```