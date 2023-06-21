import requests

from app.exception import AuthenticationFailedException
from app.model import LoginResponse


def api_login(url: str, key: str) -> LoginResponse:
    payload = {"key": key}
    resp = requests.post(f"{url}/api/login", json=payload)
    if resp.status_code != 200:
        raise AuthenticationFailedException(f"response code = {resp.status_code}")
    return LoginResponse.from_dict(resp.json())
