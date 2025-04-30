# e-kreta-hunor-2.0

e-kreta-hunor-2.0 is an api wrapper for the e-kreta system

## installation

now available on [PyPI](https://pypi.org/project/e-kreta-hun0r/)

```bash
py -m pip install e-kreta-hun0r
```

## Usage

quick example

```python
import os

from kreta.mobile import endpoints, models
from kreta.idp import Auth_Session

username = os.getenv("username")
pwd = os.getenv("pwd")
institiute_code = os.getenv("institute_code")

with Auth_Session.login(username, pwd, institiute_code) as session:
    response = endpoints.get_notes(session)
    print(response)

    session.refresh() # it's automatically done when needed
  
    response = endpoints.get_device_state(session)
    print(response)
  
    session.invalidate() # invalidates the refresh token so remove if login is saved


```

Reccomended to use `with` context maneger to properly close the connection.

Reccomended to use `session.invalidate()` if the refresh token wont be saved as it is required in the process to revoke it.

`sessiion.refresh()` refreshes the access token. Usually not required as it done automatically when needed.

Important is that for the `institute_code` parameter the second code of the school is needed. 
check your schools id [here](https://intezmenykereso.e-kreta.hu/)

![login_code](https://github.com/hun0r/e-kreta-hun0r-2.0/blob/main/image/README/login_code.png?raw=true)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

tests would be appreaciated

## License

[MIT](https://choosealicense.com/licenses/mit/)
