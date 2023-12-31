from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AuthConfig:
    token: str
    url: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LoginResponse:
    token: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UploadSampleResponse:
    error: bool
    errorMessage: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HasActiveRuntimeResponse:
    has: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GeneModel:
    name: str
    assembly: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GetGeneModelsResponse:
    geneModels: list[GeneModel]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GetAssembliesResponse:
    assemblies: list[str]


organism_mapping = {
    'human': 'NCBITaxon_9606',
    'mouse': 'NCBITaxon_10090',
    'rat': 'NCBITaxon_10116'
}
