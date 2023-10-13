import requests

from app.exception import GetGeneModelsException, GetAssembliesException
from app.model import AuthConfig, GetGeneModelsResponse, GeneModel, GetAssembliesResponse


def list_gene_models(auth_config: AuthConfig) -> list[GeneModel]:
    headers = {'Authorization': f'Bearer {auth_config.token}'}
    resp = requests.get(f"{auth_config.url}/private/gene-model/list-all", headers=headers)
    if resp.status_code != 200:
        raise GetGeneModelsException(f'response code = {resp.status_code}')
    ggmr: GetGeneModelsResponse = GetGeneModelsResponse.from_dict(resp.json())
    return ggmr.geneModels


def list_assemblies(auth_config: AuthConfig) -> list[str]:
    headers = {'Authorization': f'Bearer {auth_config.token}'}
    resp = requests.get(f"{auth_config.url}/private/assembly/list-all", headers=headers)
    if resp.status_code != 200:
        raise GetAssembliesException(f'response code = {resp.status_code}')
    gar: GetAssembliesResponse = GetAssembliesResponse.from_dict(resp.json())
    return gar.assemblies
