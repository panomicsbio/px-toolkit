import os
from pathlib import Path

import click

from app.model import AuthConfig


def login(host: str, key: str):
    conf_dir = os.path.join(Path.home(), ".panomics")
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
    auth_conf = AuthConfig(api_key=key, host=host)
    auth_conf_file = os.path.join(conf_dir, "auth")
    with open(auth_conf_file, 'wt', encoding='utf-8') as f:
        f.write(auth_conf.to_json())
    click.echo(f"credentials stored in {auth_conf_file}")
