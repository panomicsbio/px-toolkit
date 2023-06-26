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
