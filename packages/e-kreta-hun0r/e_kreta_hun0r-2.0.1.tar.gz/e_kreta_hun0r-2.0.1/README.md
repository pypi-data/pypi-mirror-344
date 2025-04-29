# e-kreta-hunor-2.0

e-kreta-hunor-2.0 is an api wrapper for the e-kreta system

## installation

for now download the repo and install requirements.txt

```bash
py -m pip install -r requirements.txt
```

later i plan to add it on pypi

## Usage

```python
import os

from src.kreta.mobile import endpoints, models
from src.kreta.idp import Auth_Session

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

tests would be appreaciated

## License

[MIT](https://choosealicense.com/licenses/mit/)
