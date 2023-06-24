import os
from pathlib import Path

import click
import requests

from app import LoginResponse
from app.exception import AuthenticationFailedException
from app.model import AuthConfig


def login(url: str, key: str):
    conf_dir = os.path.join(Path.home(), ".panomics")

    payload = {"key": key}
    resp = requests.post(f"{url}/api/login", json=payload)
    if resp.status_code != 200:
        raise AuthenticationFailedException(f"response code = {resp.status_code}")
    login_resp = LoginResponse.from_dict(resp.json())

    auth_conf = AuthConfig(token=login_resp.token, url=url)
    auth_conf_file = os.path.join(conf_dir, "auth")
    with open(auth_conf_file, 'wt', encoding='utf-8') as f:
        f.write(auth_conf.to_json())
    click.echo(f"credentials stored in {auth_conf_file}")


def get_auth() -> AuthConfig | None:
    try:
        with open(os.path.join(Path.home(), '.panomics', 'auth'), 'rt') as f:
            return AuthConfig.from_json(f.read())
    except:
        return None
