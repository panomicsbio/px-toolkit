import os.path
import uuid
from typing import Literal

import requests

from app.exception import AuthenticationFailedException, SampleUploadFailedException
from app.model import LoginResponse, AuthConfig, UploadSampleResponse


def api_login(url: str, key: str) -> LoginResponse:
    payload = {"key": key}
    resp = requests.post(f"{url}/api/login", json=payload)
    if resp.status_code != 200:
        raise AuthenticationFailedException(f"response code = {resp.status_code}")
    return LoginResponse.from_dict(resp.json())


def api_upload_sample(auth_config: AuthConfig, filename: str,
                      sample_type: Literal['RNA-seq', 'scRNA-seq']):
    files = {'file': open(filename, 'rb')}
    data = {'sampleName': os.path.basename(filename).split(".")[0],
            'sampleType': sample_type,
            'requestId': str(uuid.uuid4())}
    headers = {'Authorization': f'Bearer {auth_config.token}'}
    resp = requests.post(f"{auth_config.url}/private/sample/upload", data=data, files=files, headers=headers)
    if resp.status_code != 200:
        raise SampleUploadFailedException(f'response code = {resp.status_code}')
    usr: UploadSampleResponse = UploadSampleResponse.from_dict(resp.json())
    if usr.error:
        raise SampleUploadFailedException(usr.errorMessage)
