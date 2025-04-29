"""
Truffle client module for interacting with the Truffle service.
"""

from .core import TruffleClient
from .builders import ConversationBuilder
from .responses import SearchResponse, InferenceResponse, EmbeddingResponse
from .exceptions import TruffleClientError, ConnectionError

__all__ = [
    'TruffleClient',
    'ConversationBuilder',
    'SearchResponse',
    'InferenceResponse',
    'EmbeddingResponse',
    'TruffleClientError',
    'ConnectionError',
] 