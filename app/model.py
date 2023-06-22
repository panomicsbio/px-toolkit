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
