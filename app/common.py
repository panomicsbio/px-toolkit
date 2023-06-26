import requests

from app.exception import RuntimeStatusCheckException
from app.model import AuthConfig, HasActiveRuntimeResponse


def has_active_runtime(auth_config: AuthConfig) -> bool:
    headers = {'Authorization': f'Bearer {auth_config.token}'}
    resp = requests.get(f"{auth_config.url}/private/user/has-active-runtime", headers=headers)
    if resp.status_code != 200:
        raise RuntimeStatusCheckException(f'response code = {resp.status_code}')
    harr: HasActiveRuntimeResponse = HasActiveRuntimeResponse.from_dict(resp.json())
    return harr.has
