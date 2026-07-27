class OpenPCBDBError(Exception):
    """Base exception for OpenPCBDB API errors."""


class ReferenceError(OpenPCBDBError):
    """Raised when an OpenPCBDB reference cannot be resolved."""


class ValidationError(OpenPCBDBError):
    """Raised when validation has blocking errors."""
