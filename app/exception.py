class ApiException(Exception):
    """Raised when the API returns a non-200 status code"""
    pass


class AuthenticationFailedException(Exception):
    """Raised when authentication fails"""
    pass
