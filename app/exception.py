class ApiException(Exception):
    """Raised when the API returns a non-200 status code"""
    pass


class AuthenticationFailedException(Exception):
    """Raised when authentication fails"""
    pass


class SampleUploadFailedException(Exception):
    """Raised when sample upload fails"""
    pass


class NoActiveRuntimeException(Exception):
    """Raised when an active runtime is missing"""
    pass


class RuntimeStatusCheckException(Exception):
    """Raised when cannot check the runtime status"""
    pass


class GetGeneModelsException(Exception):
    """Raised if the gene models cannot be retrieved"""
    pass


class GetAssembliesException(Exception):
    """Raised if the assemblies cannot be retrieved"""
    pass


class InvalidOutputFileException(Exception):
    """Raised if an output file is not a valid location"""
    pass


class MissingAttributesException(Exception):
    """Raised if an input is missing certain attributes"""
    pass
