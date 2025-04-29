from typing import Literal, Self

import requests

from .auth_token import Auth_Token
from .login import login


class Auth_Session(requests.Session):
    def __init__(self, token: Auth_Token, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.token = token
        self.headers.update(
            {
                "Authorization": str(self.token),
                "User-Agent": "hu.ekreta.tanulo/1.0.5/Android/0/0",
                "apiKey": "21ff6c25-d1da-4a68-a811-c881a6057463",
            },
        )

    def __enter__(self) -> Self:
        return super().__enter__()

    def __exit__(self, *args, **kwargs) -> None:
        super().__exit__(*args, **kwargs)

    def close(self) -> None:
        try:
            super().close()
            self.invalidate()
        except Exception:
            pass
        super().close()

    def invalidate(self) -> None:
        self.token.revoke_refresh_token()
        self.token = None
        self.headers.pop("Authorization")

    @classmethod
    def login(cls, username: str, password: str, institute_code: str) -> Self:
        r = login(username, password, institute_code)
        token = Auth_Token(**r)
        return cls(token)

    def request(
        self,
        method: Literal[
            "CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"
        ],
        url: str,
        *args,
        **kwargs
    ) -> requests.Response:
        # fill the institute code in the url
        if "{institute_code}" in url:
            url = url.format(institute_code=self.token.body.kreta_institute_code)
        # refresh the token if needed
        if self.token.body.is_expired():
            self.token.refresh()
            self.headers.update({"Authorization": str(self.token)})
        # make request
        response = super().request(method, url, *args, **kwargs)
        # raise errors with the messages sent by kreta
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if (
                response.headers.get("Content-Type", "")
                .lower()
                .startswith("application/json")
            ):
                json: dict = response.json()
                e.add_note(
                    json.get("Message", json.get("error", "unknown error")),
                )
            else:
                e.add_note(
                    response.text,
                )
            raise e

        return response

    def refresh(self) -> None:
        self.token.refresh()
        self.headers.update({"Authorization": str(self.token)})
