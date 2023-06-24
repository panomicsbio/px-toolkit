import os.path
import uuid
from pathlib import Path
from typing import Literal

import requests

from app import UploadSampleResponse
from app.exception import SampleUploadFailedException
from app.model import AuthConfig, organism_mapping


def upload_sample(auth_config: AuthConfig, filename: Path, organism: Literal['human', 'mouse'],
                  sample_type: Literal['RNA-seq', 'scRNA-seq'],
                  gene_id_col: str, gene_symbol_col: str, raw_count_col: str):
    files = {'file': open(filename, 'rb')}
    data = {'sampleName': os.path.basename(filename).split(".")[0],
            'sampleType': sample_type,
            'organism': organism_mapping[organism],
            'geneIdCol': gene_id_col,
            'geneSymbolCol': gene_symbol_col,
            'rawCountCol': raw_count_col,
            'requestId': str(uuid.uuid4())}
    headers = {'Authorization': f'Bearer {auth_config.token}'}
    resp = requests.post(f"{auth_config.url}/private/sample/upload", data=data, files=files, headers=headers)
    if resp.status_code != 200:
        raise SampleUploadFailedException(f'response code = {resp.status_code}')
    usr: UploadSampleResponse = UploadSampleResponse.from_dict(resp.json())
    if usr.error:
        raise SampleUploadFailedException(usr.errorMessage)
