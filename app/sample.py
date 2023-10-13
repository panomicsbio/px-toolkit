import os.path
import uuid
from pathlib import Path

import pandas as pd
import requests

from app import UploadSampleResponse
from app.exception import SampleUploadFailedException, InvalidOutputFileException, MissingAttributesException
from app.model import AuthConfig, organism_mapping


def generate_sample_sheet(organism: str, assembly: str, gene_model: str, sample_type: str,
                          gene_col: str, raw_count_col: str, tpm_count_col: str, fpkm_count_col: str,
                          files: list[Path], output_file: str):
    sample_sheet = pd.DataFrame(columns=['file', 'sample_name'])
    for f in files:
        sample_sheet.loc[len(sample_sheet)] = [f, os.path.basename(f).split(".")[0]]

    sample_sheet['organism'] = organism
    sample_sheet['assembly'] = assembly
    sample_sheet['gene_model'] = gene_model
    sample_sheet['sample_type'] = sample_type
    if sample_type == 'RNA-seq':
        if not gene_col or not raw_count_col:
            raise MissingAttributesException('gene_col and raw_count_col are mandatory for RNA-seq samples')
        sample_sheet['gene_col'] = gene_col
        sample_sheet['raw_count_col'] = raw_count_col
        sample_sheet['tpm_count_col'] = tpm_count_col
        sample_sheet['fpkm_count_col'] = fpkm_count_col

    if output_file:
        try:
            sample_sheet.to_csv(output_file, index=False)
        except:
            raise InvalidOutputFileException(output_file)
    else:
        sample_sheet.to_csv("./sample_sheet.csv", index=False)


def upload_sample(auth_config: AuthConfig, entry, project_id: int):
    files = {'file': open(entry['file'], 'rb')}
    data = {'sampleName': entry['sample_name'],
            'sampleType': entry['sample_type'],
            'organism': organism_mapping[entry['organism']],
            'genomeAssembly': entry['assembly'],
            'geneCol': entry['gene_col'] if 'gene_col' in entry else '',
            'rawCountCol': entry['raw_count_col'] if 'raw_count_col' in entry else '',
            'tpmCountCol': entry['tpm_count_col'] if 'tpm_count_col' in entry else '',
            'fpkmCountCol': entry['fpkm_count_col'] if 'fpkm_count_col' in entry else '',
            'projectId': project_id,
            'requestId': str(uuid.uuid4())}
    headers = {'Authorization': f'Bearer {auth_config.token}'}
    resp = requests.post(f"{auth_config.url}/private/sample/upload", data=data, files=files, headers=headers)
    if resp.status_code != 200:
        raise SampleUploadFailedException(f'response code = {resp.status_code}')
    usr: UploadSampleResponse = UploadSampleResponse.from_dict(resp.json())
    if usr.error:
        raise SampleUploadFailedException(usr.errorMessage)
