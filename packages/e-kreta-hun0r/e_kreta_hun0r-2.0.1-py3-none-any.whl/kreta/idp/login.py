from time import sleep
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup as bs
from requests import Session


def login(UserName: str, Password: str, InstituteCode: str) -> dict:
    try:
        with Session() as session:

            url = "https://idp.e-kreta.hu/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fprompt%3Dlogin%26nonce%3DwylCrqT4oN6PPgQn2yQB0euKei9nJeZ6_ffJ-VpSKZU%26response_type%3Dcode%26code_challenge_method%3DS256%26scope%3Dopenid%2520email%2520offline_access%2520kreta-ellenorzo-webapi.public%2520kreta-eugyintezes-webapi.public%2520kreta-fileservice-webapi.public%2520kreta-mobile-global-webapi.public%2520kreta-dkt-webapi.public%2520kreta-ier-webapi.public%26code_challenge%3DHByZRRnPGb-Ko_wTI7ibIba1HQ6lor0ws4bcgReuYSQ%26redirect_uri%3Dhttps%253A%252F%252Fmobil.e-kreta.hu%252Fellenorzo-student%252Fprod%252Foauthredirect%26client_id%3Dkreta-ellenorzo-student-mobile-ios%26state%3Dkreten_student_mobile%26suppressed_prompt%3Dlogin"

            response = session.request("GET", url)

            # rvt token
            soup = bs(response.text, "html.parser")
            rvt = soup.find("input", {"name": "__RequestVerificationToken"})["value"]

            # login form
            payload = {
                "ReturnUrl": "/connect/authorize/callback?prompt=login&nonce=wylCrqT4oN6PPgQn2yQB0euKei9nJeZ6_ffJ-VpSKZU&response_type=code&code_challenge_method=S256&scope=openid%20email%20offline_access%20kreta-ellenorzo-webapi.public%20kreta-eugyintezes-webapi.public%20kreta-fileservice-webapi.public%20kreta-mobile-global-webapi.public%20kreta-dkt-webapi.public%20kreta-ier-webapi.public&code_challenge=HByZRRnPGb-Ko_wTI7ibIba1HQ6lor0ws4bcgReuYSQ&redirect_uri=https%3A%2F%2Fmobil.e-kreta.hu%2Fellenorzo-student%2Fprod%2Foauthredirect&client_id=kreta-ellenorzo-student-mobile-ios&state=kreten_student_mobile&suppressed_prompt=login",
                "IsTemporaryLogin": False,
                "UserName": UserName,
                "Password": Password,
                "InstituteCode": InstituteCode,
                "loginType": "InstituteLogin",
                "__RequestVerificationToken": rvt,
            }

            url = "https://idp.e-kreta.hu/account/login"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            sleep(0.5)
            response = session.request(
                "POST", url, headers=headers, data=payload, allow_redirects=False
            )
            if response.status_code != 200:
                raise Exception("Login failed check your credentials")

            # get the code
            response = session.request(
                "GET",
                "https://idp.e-kreta.hu/connect/authorize/callback?prompt=login&nonce=wylCrqT4oN6PPgQn2yQB0euKei9nJeZ6_ffJ-VpSKZU&response_type=code&code_challenge_method=S256&scope=openid%20email%20offline_access%20kreta-ellenorzo-webapi.public%20kreta-eugyintezes-webapi.public%20kreta-fileservice-webapi.public%20kreta-mobile-global-webapi.public%20kreta-dkt-webapi.public%20kreta-ier-webapi.public&code_challenge=HByZRRnPGb-Ko_wTI7ibIba1HQ6lor0ws4bcgReuYSQ&redirect_uri=https%3A%2F%2Fmobil.e-kreta.hu%2Fellenorzo-student%2Fprod%2Foauthredirect&client_id=kreta-ellenorzo-student-mobile-ios&state=kreten_student_mobile&suppressed_prompt=login",
                allow_redirects=False,
            )
            url = urlparse(response.headers["location"])
            code = parse_qs(url.query)["code"][0]

            # get the token
            data = {
                "code": code,
                "code_verifier": "DSpuqj_HhDX4wzQIbtn8lr8NLE5wEi1iVLMtMK0jY6c",
                "redirect_uri": "https://mobil.e-kreta.hu/ellenorzo-student/prod/oauthredirect",
                "client_id": "kreta-ellenorzo-student-mobile-ios",
                "grant_type": "authorization_code",
            }
            response = session.request(
                "POST", "https://idp.e-kreta.hu/connect/token", data=data
            )

        return response.json()
    except Exception:
        raise Exception(
            "Login failed check your credentials and try again. Make sure to use the longer code"
        )
