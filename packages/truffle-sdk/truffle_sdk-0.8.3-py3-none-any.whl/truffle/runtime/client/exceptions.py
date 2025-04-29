"""
Essential error types for the Truffle client.
"""

class TruffleClientError(Exception):
    """Base exception for all Truffle client errors."""
    pass

class ConnectionError(TruffleClientError):
    """Raised when there are connection issues with the Truffle service."""
    pass

class ConfigurationError(TruffleClientError):
    """Raised when client configuration is invalid."""
    pass

class OperationError(TruffleClientError):
    """Raised when a client operation fails."""
    pass

# Add specific operation errors moved from core.py
class TruffleSearchError(TruffleClientError):
    """Search operation errors"""
    pass

class TruffleInferenceError(TruffleClientError):
    """Inference operation errors"""
    pass

class TruffleEmbeddingError(TruffleClientError):
    """Embedding operation errors"""
    pass 